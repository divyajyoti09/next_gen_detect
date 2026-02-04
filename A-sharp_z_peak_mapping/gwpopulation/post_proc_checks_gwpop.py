# ## Calculate variance

# In[14]:

print("Importing packages")

import gwpopulation as gwpop
import os
gwpop.set_backend("jax")
from gwpopulation.experimental.jax import JittedLikelihood, NonCachingModel
import jax
import argparse
from glob import glob
import dill
from tqdm import tqdm
import pandas as pd
import pylab as plt
from bilby.core.prior import PriorDict, Uniform
import bilby
import numpy as np
import h5py

import psutil

psutil.Process().cpu_affinity(list(range(4)))

print("Done")

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
parser.add_argument("--out-dir", required=True,
                    help="Path to the directory where gwpopulation analysis results are")
parser.add_argument("--num-samples", type=int,
                    help="Number of samples to consider from posterior. If None, all samples are considered")

args = parser.parse_args()

xp = gwpop.utils.xp

#project_dir = '/home/divyajyoti/ACADEMIC/Projects/Cardiff_University/Next_gen_detectability/A-sharp-study/'
project_dir = '/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/'

print("Loading results")
result_file = glob(os.path.join(args.out_dir, '*result.hdf5'))[0]
result = bilby.result.read_in_result(filename=result_file)

with open(os.path.join(args.out_dir, 'README.txt'), 'r') as f:
    lines = [line.rstrip('\n').strip('\t') for line in f]
readme_dict = {}
for line in lines:
    words = line.split()
    if 'Posterior' in words:
#        readme_dict['posterior_file'] = words[-1].replace('divyajyoti.nln/', 'divyajyoti/ACADEMIC/Projects/')
        readme_dict['posterior_file'] = words[-1]
    elif 'Injections' in words:
#        readme_dict['injections_file'] = words[-1].replace('divyajyoti.nln/', 'divyajyoti/ACADEMIC/Projects/')
        readme_dict['injections_file'] = words[-1]

# ## Load posteriors
print("Loading posteriors")
posteriors = pd.read_pickle(readme_dict['posterior_file'])

# ## Load injections

print("Loading injections")
with open(readme_dict['injections_file'], "rb") as ff:
    injections = dill.load(ff)

print("Initialising the model")
z_max = float(readme_dict['posterior_file'].split('zmax_')[-1].split('_')[0])
model = NonCachingModel(
    model_functions=[gwpop.models.redshift.MadauDickinsonRedshift(cosmo_model="Planck18", z_max=z_max)],
)

print("Setting VT")
vt = gwpop.vt.ResamplingVT(model=model, data=injections, n_events=len(posteriors))

print("Defining likelihood")
likelihood = gwpop.hyperpe.HyperparameterLikelihood(
    posteriors=posteriors,
    hyper_prior=model,
    selection_function=vt,
)

print("Defining priors")
priors = PriorDict()
priors['gamma'] = Uniform(minimum=0, maximum=5, latex_label="$\\gamma$")
priors['kappa'] = Uniform(minimum=0, maximum=20, latex_label="$\\kappa$")
priors['z_peak'] = Uniform(minimum=0.5, maximum=4, latex_label="$z_{peak}$")

parameters = priors.sample()
likelihood.parameters.update(parameters)

func = jax.jit(likelihood.generate_extra_statistics)

if args.num_samples:
    full_posterior_list = [func(parameters) for parameters in tqdm(result.posterior.to_dict(orient="records")[:args.num_samples], desc='constructing full posterior')]
else:
    full_posterior_list = [func(parameters) for parameters in tqdm(result.posterior.to_dict(orient="records"), desc='constructing full posterior')]
print("Done")

sample_keys = full_posterior_list[0].keys()
keys_var = []
for k in sample_keys:
    if 'var_' in k:
        keys_var.append(k)
    elif 'ln_bf' not in k:
        keys_main = [k for k in sample_keys if 'ln_bf' not in k and 'var_' not in k]

data_main = np.empty((len(full_posterior_list), len(keys_main)), dtype=np.float32)

for i, d in tqdm(enumerate(full_posterior_list), total=len(full_posterior_list), desc='Building arrays'):
    data_main[i] = [d[k] for k in keys_main]

# Convert to dict of arrays
dict_main = {k: data_main[:, i] for i, k in tqdm(enumerate(keys_main), total=len(keys_main), desc='Converting to dict of arrays')}
print("Converting to pandas dataframe")
df_main = pd.DataFrame(dict_main)

print("Writing pandas DataFrame to .csv")
df_main.to_csv(os.path.join(args.out_dir, 'full_posterior_main.csv'))

print("Plotting the variance scatter matrix")
pd.plotting.scatter_matrix(
    df_main[["gamma", "kappa", "z_peak", "log_likelihood", "variance"]],
    alpha=0.5,
)
plt.tight_layout()
plt.savefig(os.path.join(args.out_dir, 'param_variance_matrix.png'), dpi=300)

"""
print("Number of events with var > 1 :", len(keys_high_var))
print("Number of events with var < 1 :", len(keys_var))
data_high_var = np.empty((len(full_posterior_list), len(keys_high_var)), dtype=np.float32)
data_low_var = np.empty((len(full_posterior_list), len(keys_var)), dtype=np.float32)

for i, d in tqdm(enumerate(full_posterior_list), total=len(full_posterior_list), desc='Building arrays for events with var>1'):
    if i < 5:
        data_high_var[i] = [d[k] for k in keys_high_var]
        data_low_var[i] = [d[k] for k in keys_var]

# Convert to dict of arrays
dict_high_var = {k: data_high_var[:, i] for i, k in tqdm(enumerate(keys_high_var), total=len(keys_high_var), desc='Converting to dict of arrays')}
dict_low_var = {k: data_low_var[:, i] for i, k in tqdm(enumerate(keys_var), total=len(keys_var), desc='Converting to dict of arrays')}
"""
dict_var = {'key':[], 'sample_0':[]}

for key in tqdm(keys_var, desc='getting event variances for sample 0'):
    dict_var['key'].append(key)
    dict_var['sample_0'].append(full_posterior_list[0][key])

print("Converting to pandas dataframe")
df_var = pd.DataFrame(dict_var)
print("Writing pandas DataFrame to .csv")
df_var.to_csv(os.path.join(args.out_dir, 'event_var_sample0.csv'))


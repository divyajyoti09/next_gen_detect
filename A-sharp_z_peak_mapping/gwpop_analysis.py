#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bilby as bb
import gwpopulation as gwpop
import jax
import matplotlib.pyplot as plt
import pandas as pd
from bilby.core.prior import PriorDict, Uniform
from gwpopulation.experimental.jax import JittedLikelihood, NonCachingModel
import os
import time

gwpop.set_backend("jax")

xp = gwpop.utils.xp


# In[2]:


#project_dir = '/home/divyajyoti/ACADEMIC/Projects/Cardiff_University/Next_gen_detectability/A-sharp-study/'
project_dir = '/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/'


# ## Load posteriors

# In[3]:


posteriors = pd.read_pickle(os.path.join(project_dir, 'gwpopulation', 'BBH', 'redshift_posteriors_499_events.pkl'))


# ## Load injections

# In[4]:


import dill

with open(os.path.join(project_dir, 'gwpopulation', 'BBH', 'detected_injections_mf_SNR.pkl'), "rb") as ff:
    injections = dill.load(ff)


# ## Define models and likelihood

# In[5]:


model = NonCachingModel(
    model_functions=[gwpop.models.redshift.MadauDickinsonRedshift(cosmo_model="Planck18", z_max=8)],
    #model_functions=[gwpop.models.redshift.PowerLawRedshift(z_max=8)],
)

vt = gwpop.vt.ResamplingVT(model=model, data=injections, n_events=len(posteriors))

likelihood = gwpop.hyperpe.HyperparameterLikelihood(
    posteriors=posteriors,
    hyper_prior=model,
    selection_function=vt,
)


# ## Define prior

# In[6]:


priors = PriorDict()
priors['gamma'] = Uniform(minimum=0, maximum=5, latex_label="$\\gamma$")
priors['kappa'] = Uniform(minimum=0, maximum=20, latex_label="$\\kappa$")
priors['z_peak'] = Uniform(minimum=0.5, maximum=4, latex_label="$z_{peak}$")
#priors['lamb'] = Uniform(minimum=0.5, maximum=4, latex_label="$\\lambda$")


# ## Just-in-time compile

# In[7]:


parameters = priors.sample()
likelihood.parameters.update(parameters)
likelihood.log_likelihood_ratio()

# Time non-JIT evaluation
start = time.time()
print(likelihood.log_likelihood_ratio())
print(f"Non-JIT time: {time.time() - start:.4f} seconds")

jit_likelihood = JittedLikelihood(likelihood)
jit_likelihood.parameters.update(parameters)

# First JIT evaluation (includes compilation time)
start = time.time()
print(jit_likelihood.log_likelihood_ratio())
print(f"JIT (compile + run) time: {time.time() - start:.4f} seconds")

# Second JIT evaluation (cached)
start = time.time()
print(jit_likelihood.log_likelihood_ratio())
print(f"JIT (cached) time: {time.time() - start:.4f} seconds")


# In[8]:


result = bb.run_sampler(
    likelihood=jit_likelihood,
    priors=priors,
    sampler="dynesty",
    nlive=1000,
    label="Asharp-study-gwpop",
    sample="acceptance-walk",
    naccept=20,
    save="hdf5",
    plot=True,
    outdir='/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/run01_mf_SNR_injections'
)


# In[ ]:

# ## Post-processing checks

#func = jax.jit(likelihood.generate_extra_statistics)
#
#full_posterior = pd.DataFrame(
#    [func(parameters) for parameters in result.posterior.to_dict(orient="records")]
#).astype(float)
#full_posterior.describe()
#
#full_posterior[result.search_parameter_keys + ["log_likelihood", "variance"]].corr()

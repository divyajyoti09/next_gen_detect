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
import argparse

gwpop.set_backend("jax")

xp = gwpop.utils.xp

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, allow_abbrev=False)
parser.add_argument("--posterior-file", required=True, 
                    help="Path to the pkl file containing the posterior samples for all events")
parser.add_argument("--out-dir",
                    help="Path to the directory where output files will be saved. If None, files will be saved in the current directory.")
parser.add_argument("--detected-injections-file", required=True,
                    help="path to the pkl file containing the injections which are detected")
parser.add_argument("--z-max", type=float, default=8,
                    help="z_max value to call the redshift model with")
parser.add_argument("--label", default="Asharp-study",
                    help="label for the gwpopulation analysis result files")

args = parser.parse_args()

# ## Load posteriors

# In[3]:


posteriors = pd.read_pickle(args.posterior_file)


# ## Load injections

# In[4]:


import dill

with open(args.detected_injections_file, "rb") as ff:
    injections = dill.load(ff)


# ## Define models and likelihood

# In[5]:


model = NonCachingModel(
    model_functions=[gwpop.models.redshift.MadauDickinsonRedshift(cosmo_model="Planck18", z_max=args.z_max)],
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
    label=args.label,
    sample="acceptance-walk",
    naccept=20,
    save="hdf5",
    plot=True,
    outdir=args.out_dir
)

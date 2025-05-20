#!/bin/bash
tar -xzf noise_curves.tar.gz
/cvmfs/software.igwn.org/conda/envs/igwn-py310/bin/python3 gen_WF_calc_SNR.py \
  --param-file 1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_part$1.h5 \
  --approximant IMRPhenomPv2 \
  --detectors-and-psds L1:ASharp H1:ASharp I1:ASharp \
  --f-low 10 \
  --out-dir SNR_output_files \
  --set-name LHI_SNR_1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_part$1 \
  --num-procs 16 \
  --max-worker-chunksize 10

#!/bin/bash
echo "== Contents of working dir =="
ls -lh

echo "== Trying to extract tar =="
tar -xzf noise_curves.tar.gz
/cvmfs/software.igwn.org/conda/envs/igwn-py310/bin/python3 gen_WF_calc_SNR.py \
  --param-file 2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_part$1.h5 \
  --approximant IMRPhenomPv2 \
  --detectors-and-psds C1:CE40 CE20:CE20 E1:ET10_CoBA E2:ET10_CoBA E3:ET10_CoBA \
  --f-low 5 \
  --out-dir SNR_output_files \
  --set-name CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_part$1 \
  --num-procs 16 \
  --max-worker-chunksize 10

#!/bin/bash
echo "== Contents of working dir =="
ls -lh

echo "== Trying to extract tar =="
POP_NAME="5_pop_PLP_spin_prec_fref_5_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td"

tar -xzf noise_curves.tar.gz
/cvmfs/software.igwn.org/conda/envs/igwn-py311/bin/python3 gen_WF_calc_SNR.py \
  --param-file ${POP_NAME}_part$1.h5 \
  --approximant IMRPhenomXPHM \
  --detectors-and-psds C1:CE40 CE20:CE20 E1:ET10_CoBA E2:ET10_CoBA E3:ET10_CoBA \
  --f-low 5 \
  --out-dir SNR_output_files_XPHM2/CE4020ET123_CoBA10_SNR_${POP_NAME} \
  --set-name CE4020ET123_CoBA10_SNR_${POP_NAME}_part$1 \
  --num-procs 16 \
  --max-worker-chunksize 20

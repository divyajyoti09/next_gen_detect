#!/bin/bash
echo "== Contents of working dir =="                                                     
ls -lh                                                                                   
echo "== Trying to extract tar =="
POP_NAME="2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_19"
tar -xzf noise_curves.tar.gz
/cvmfs/software.igwn.org/conda/envs/igwn-py311/bin/python3 gen_WF_calc_SNR.py \
  --param-file ${POP_NAME}_part$1.h5 \
  --approximant IMRPhenomXPHM \
  --detectors-and-psds L1:ASharp_postO5 H1:ASharp_postO5 V1:Virgo_postO5 \
  --f-low 10 \
  --out-dir SNR_output_files_XPHM/LHV_ASharp_SNR_${POP_NAME} \
  --set-name LHV_ASharp_SNR_${POP_NAME}_part$1 \
  --num-procs 16 \
  --max-worker-chunksize 20

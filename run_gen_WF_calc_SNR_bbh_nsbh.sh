#!/bin/bash

# Make sure all the child processes are killed if a kill signal is sent to the parent
#trap 'echo "Job terminated due to SIGTERM signal" > failure.out; kill -- -$$; exit' SIGTERM SIGINT
trap "kill 0" EXIT

#commenting out the text below
echo "Running BBH for LI, H1, V1 all at A# post O5 sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /home/divyajyoti.nln/Post-O5-study/data/population_analysis/input_population/2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_19_365_days.h5 \
        --approximant IMRPhenomXPHM \
        --detectors-and-psds \
		L1:ASharp_postO5 \
                H1:ASharp_postO5 \
                V1:Virgo_postO5 \
	--f-low 10 \
	--out-dir /home/divyajyoti.nln/Post-O5-study/data/population_analysis/SNR_output_files_XPHM \
        --set-name LHV_ASharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_19_365_days \
	--num-procs 16
echo "Run complete!"
printf "\n\n"

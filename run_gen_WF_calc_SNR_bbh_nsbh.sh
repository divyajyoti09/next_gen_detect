#!/bin/bash

# Make sure all the child processes are killed if a kill signal is sent to the parent
#trap 'echo "Job terminated due to SIGTERM signal" > failure.out; kill -- -$$; exit' SIGTERM SIGINT
trap "kill 0" EXIT

#commenting out the text below
echo "Running BBH for LI, H1, V1 for O5b sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /home/divyajyoti.nln/MMA/Project_with_Natalie/data/input_population/BBH/2_pop_PLP_spin_prec_fref_20_z_MD_zmax_10_lmrd_22_365_days_corrected_td.h5 \
        --approximant IMRPhenomXPHM \
        --detectors-and-psds \
		L1:O5b \
                H1:O5b \
                V1:AdvVirgo \
	--f-low 20 \
	--out-dir /home/divyajyoti.nln/MMA/Project_with_Natalie/data/SNR_output_files_XPHM \
        --set-name LHV_O5b_SNR_2_pop_PLP_spin_prec_fref_20_z_MD_zmax_10_lmrd_22_365_days_corrected_td \
	--num-procs 16
echo "Run complete!"
printf "\n\n"


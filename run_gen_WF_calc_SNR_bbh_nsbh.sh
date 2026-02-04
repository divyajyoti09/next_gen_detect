#!/bin/bash

# Make sure all the child processes are killed if a kill signal is sent to the parent
#trap 'echo "Job terminated due to SIGTERM signal" > failure.out; kill -- -$$; exit' SIGTERM SIGINT
trap "kill 0" EXIT

#commenting out the text below
echo "Running BBH for LI, H1, I1 all at A# sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/input_population/BBH/4_pop_set2_PLP_spin_prec_fref_10_z_MDhigh_zp_2.53_zmax_10_lmrd_22_365_days_corrected_td.h5 \
        --approximant IMRPhenomXPHM \
        --detectors-and-psds \
		L1:ASharp \
                H1:ASharp \
                I1:ASharp \
	--f-low 10 \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/SNR_output_files_XPHM/BBH \
        --set-name LHI_SNR_4_pop_set2_PLP_spin_prec_fref_10_z_MDhigh_zp_2.53_zmax_10_lmrd_22_365_days_corrected_td \
	--num-procs 16
echo "Run complete!"
printf "\n\n"

<<'COMMENT'
echo "Running NSBH part 1 for LI, H1, I1 all at A# sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/input_population/NSBH/1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part1.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:ASharp \
                H1:ASharp \
                I1:ASharp \
	--f-low 10 \
	--out-dir /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/SNR_output_files/NSBH \
        --set-name LHI_SNR_1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part1 \
	--num-procs 8
echo "Run complete!"
printf "\n\n"

echo "Running NSBH part 2 for LI, H1, I1 all at A# sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/input_population/NSBH/1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part2.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:ASharp \
                H1:ASharp \
                I1:ASharp \
	--f-low 10 \
	--out-dir /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/SNR_output_files/NSBH \
        --set-name LHI_SNR_1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part2 \
	--num-procs 8
echo "Run complete!"
printf "\n\n"

echo "Running NSBH part 3 for LI, H1, I1 all at A# sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/input_population/NSBH/1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part3.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:ASharp \
                H1:ASharp \
                I1:ASharp \
	--f-low 10 \
	--out-dir /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/SNR_output_files/NSBH \
        --set-name LHI_SNR_1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part3 \
	--num-procs 8
echo "Run complete!"
printf "\n\n"

echo "Running NSBH part 4 for LI, H1, I1 all at A# sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/input_population/NSBH/1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part4.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:ASharp \
                H1:ASharp \
                I1:ASharp \
	--f-low 10 \
	--out-dir /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/SNR_output_files/NSBH \
        --set-name LHI_SNR_1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part4 \
	--num-procs 8
echo "Run complete!"
printf "\n\n"

echo "Running NSBH part 5 for LI, H1, I1 all at A# sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/input_population/NSBH/1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part5.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:ASharp \
                H1:ASharp \
                I1:ASharp \
	--f-low 10 \
	--out-dir /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/SNR_output_files/NSBH \
        --set-name LHI_SNR_1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part5 \
	--num-procs 8
echo "Run complete!"
printf "\n\n"

echo "Running NSBH part 6 for LI, H1, I1 all at A# sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/input_population/NSBH/1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part6.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:ASharp \
                H1:ASharp \
                I1:ASharp \
	--f-low 10 \
	--out-dir /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/SNR_output_files/NSBH \
        --set-name LHI_SNR_1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part6 \
	--num-procs 8
echo "Run complete!"
printf "\n\n"

echo "Running NSBH part 7 for LI, H1, I1 all at A# sensitivty"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/input_population/NSBH/1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part7.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:ASharp \
                H1:ASharp \
                I1:ASharp \
	--f-low 10 \
	--out-dir /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/SNR_output_files/NSBH \
        --set-name LHI_SNR_1_pop_US_spin_prec_z_MD_zmax_2_lmrd_45_61_days_corrected_td_part7 \
	--num-procs 8
echo "Run complete!"
printf "\n\n"

echo "Running BBH for CE40, CE20, ET123"
printf "\n"
python gen_WF_calc_SNR.py \
	--param-file /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/input_population/BBH/3_pop_PLP_spin_aligned_fref_5_z_MD_zmax_10_lmrd_22_365_days_corrected_td.h5 \
        --approximant IMRPhenomXPHM \
        --detectors-and-psds \
		C1:CE40 \
                CE20:CE20 \
                E1:ET10_CoBA \
                E2:ET10_CoBA \
                E3:ET10_CoBA \
	--f-low 5 \
	--out-dir /nfshome/store04/users/divyajyoti.nln/Next_gen_detectability/A-sharp-study/SNR_output_files_XPHM/BBH \
        --set-name CE4020ET123_CoBA10_SNR_3_pop_PLP_spin_aligned_fref_5_z_MD_zmax_10_lmrd_22_365_days_corrected_td \
	--num-procs 16
echo "Run complete!"
printf "\n\n"
COMMENT

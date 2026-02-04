source activate gwpopulation
<<COMMENT
OUT_DIR1="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/run09_gwfish_mf_from_opt_SNR_injections_XPHM"

python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/LHI_Asharp_2_PLP_z_fref_10_MD_zmax_10_lmrd_22_no_spins_z_posteriors_10K_4057_events_pop_from_XPHM.pkl \
	--out-dir "${OUT_DIR1}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/LHI_Asharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_12M_points_XPHM.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR1}"

OUT_DIR2="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/run18_gwfish_MDhigh_mf_from_gaussian_SNR_injections_XPHM"

python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/LHI_Asharp_4_PLP_z_MDhigh_zp_2.53_zmax_10_lmrd_22_no_spins_z_posteriors_10K_4690_events_pop_from_XPHM_fm2_netw.pkl \
	--out-dir "${OUT_DIR2}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/LHI_Asharp_SNR_4_pop_PLP_spin_prec_fref_10_z_MDhigh_zp_2.53_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_24M_points_XPHM.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR2}"

COMMENT

OUT_DIR3="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/run19_gwfish_MDlow_mf_from_opt_SNR_injections_XPHM"

python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/LHI_Asharp_5_PLP_z_MDlow_zp_1.54_zmax_10_lmrd_22_no_spins_z_posteriors_10K_3667_events_pop_from_XPHM_fm2_netw.pkl \
	--out-dir "${OUT_DIR3}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/LHI_Asharp_SNR_5_pop_PLP_spin_prec_fref_10_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_24M_points_XPHM.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR3}"

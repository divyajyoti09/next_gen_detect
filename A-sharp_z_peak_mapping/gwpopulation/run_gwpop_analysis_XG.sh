source activate gwpopulation

OUT_DIR1="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/run14_gwfish_MDhigh_mf_from_opt_SNR_injections_XPHM"
echo "Running analysis"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/CE4020ET123_CoBA10_4_PLP_z_MDhigh_zp_2.53_zmax_10_lmrd_22_no_spins_z_posteriors_10K_6852_events_pop_from_XPHM.pkl \
	--out-dir "${OUT_DIR1}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/CE4020ET123_CoBA10_SNR_4_pop_PLP_spin_prec_fref_5_z_MDhigh_zp_2.53_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_4M_points_XPHM.pkl \
	--label CE4020ET123

echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "{OUT_DIR1}"

OUT_DIR2="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/run15_gwfish_MDlow_mf_from_opt_SNR_injections_XPHM"
echo "Running analysis"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/CE4020ET123_CoBA10_5_PLP_z_MDlow_zp_1.54_zmax_10_lmrd_22_no_spins_z_posteriors_10K_5106_events_pop_from_XPHM.pkl \
	--out-dir "${OUT_DIR2}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/CE4020ET123_CoBA10_SNR_5_pop_PLP_spin_prec_fref_5_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_4M_points_XPHM.pkl \
	--label CE4020ET123

echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "{OUT_DIR2}"

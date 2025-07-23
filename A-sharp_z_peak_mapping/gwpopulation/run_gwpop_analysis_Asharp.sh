source activate gwpopulation
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/LHI_Asharp_1_PLP_z_MD_zmax_6_lmrd_22_no_spins_all_events_365_days_z_posteriors_original_cov_4339_events_pop_from_XPHM2.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/run04_original_cov_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/LHI_Asharp_SNR_1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_4M_points_XPHM.pkl \
	--label Asharp


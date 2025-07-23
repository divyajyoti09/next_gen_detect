source activate gwpopulation
<<COMMENT
echo "Running for M < 40"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/mass_bands/LHI_Asharp_1_PLP_z_MD_zmax_6_lmrd_22_no_spins_all_events_365_days_z_posteriors_original_cov_2340_events_pop_from_XPHM_below_40.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/below_40/run01_original_cov_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_3405654_points_below_40.pkl \
	--label Asharp
echo " "

echo "Running for M in [40, 80]"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/mass_bands/LHI_Asharp_1_PLP_z_MD_zmax_6_lmrd_22_no_spins_all_events_365_days_z_posteriors_original_cov_1813_events_pop_from_XPHM_40-80.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/40-80/run01_original_cov_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_554599_points_40-80.pkl \
	--label Asharp
echo " "

COMMENT
echo "Running for M > 80"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/mass_bands/LHI_Asharp_1_PLP_z_MD_zmax_6_lmrd_22_no_spins_all_events_365_days_z_posteriors_10K_original_cov_186_events_pop_from_XPHM3_above_80.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/above_80/run03_original_cov_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_39743_points_above_80.pkl \
	--label Asharp
echo " "

<<COMMENT
echo "Running for M < 40"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_set3_z_posteriors_original_cov_3625_events_pop_from_XPHM_below_40.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/below_40/run01_original_cov_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_1703378_points_below_40.pkl \
	--label CE4020ET123
echo " "

echo "Running for M in [40, 80]"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_set3_z_posteriors_original_cov_670_events_pop_from_XPHM_40-80.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/40-80/run01_original_cov_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_276766_points_40-80.pkl \
	--label CE4020ET123
echo " "

echo "Running for M > 80"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_set3_z_posteriors_original_cov_49_events_pop_from_XPHM_above_80.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/above_80/run01_original_cov_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_19852_points_above_80.pkl \
	--label CE4020ET123
echo " "
COMMENT

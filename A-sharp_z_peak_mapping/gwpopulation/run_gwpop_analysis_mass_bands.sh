source activate gwpopulation
echo "Running for M < 40"
OUT_DIR="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/below_40/run03_gwfish_mf_from_opt_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_2_PLP_z_fref_10_MD_zmax_10_lmrd_22_no_spins_z_posteriors_10K_2000_events_pop_from_XPHM2_below_40.pkl \
	--out-dir "${OUT_DIR}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_3405394_points_below_40.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR}"
echo " "

<<COMMENT
echo "Running for M in [40, 80]"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_2_PLP_z_fref_10_MD_zmax_10_lmrd_22_no_spins_z_posteriors_10K_1872_events_pop_from_XPHM_40-80.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/40-80/run02_gwfish_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_554561_points_40-80.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/40-80/run02_gwfish_mf_from_opt_SNR_injections_XPHM 
echo " "

echo "Running for M > 80"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_2_PLP_z_fref_10_MD_zmax_10_lmrd_22_no_spins_z_posteriors_10K_205_events_pop_from_XPHM_above_80.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/above_80/run04_gwfish_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_40044_points_above_80.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/above_80/run04_gwfish_mf_from_opt_SNR_injections_XPHM 
echo " "

echo "Running for M < 40"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_z_posteriors_10K_4979_events_pop_from_XPHM2_below_40.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/below_40/run03_gwfish_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_1703378_points_below_40.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/below_40/run02_gwfish_mf_from_opt_SNR_injections_XPHM
echo " "
echo "Running for M in [40, 80]"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_z_posteriors_10K_835_events_pop_from_XPHM_40-80.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/40-80/run02_gwfish_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_276766_points_40-80.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/40-80/run02_gwfish_mf_from_opt_SNR_injections_XPHM
echo " "

echo "Running for M > 80"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_z_posteriors_10K_67_events_pop_from_XPHM_above_80.pkl \
	--out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/above_80/run02_gwfish_mf_from_opt_SNR_injections_XPHM \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_opt_SNR_19852_points_above_80.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/above_80/run02_gwfish_mf_from_opt_SNR_injections_XPHM
echo " "
COMMENT

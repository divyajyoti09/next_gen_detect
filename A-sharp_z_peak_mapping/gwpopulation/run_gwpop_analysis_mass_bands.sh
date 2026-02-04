source activate gwpopulation
echo "Running for M < 40"
<<COMMENT
OUT_DIR1="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/below_40/run06_gwfish_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_posteriors_10K_2015_events_pop_from_XPHM_fm2_netw_below_40.pkl \
	--out-dir "${OUT_DIR1}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_20436686_points_below_40.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR1}"
echo " "

OUT_DIR2="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/below_40/run09_gwfish_MDhigh_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_4_PLP_z_MDhigh_zp_2.53_zmax_10_lmrd_22_no_spins_posteriors_10K_2119_events_pop_from_XPHM_fm2_netw_below_40.pkl \
	--out-dir "${OUT_DIR2}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_4_pop_PLP_spin_prec_fref_10_z_MDhigh_zp_2.53_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_20437744_points_below_40.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR2}"
echo " "
COMMENT

OUT_DIR3="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/below_40/run10_gwfish_MDlow_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_5_PLP_z_MDlow_zp_1.54_zmax_10_lmrd_22_no_spins_posteriors_10K_1911_events_pop_from_XPHM_fm2_netw_below_40.pkl \
	--out-dir "${OUT_DIR3}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_5_pop_PLP_spin_prec_fref_10_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_20436009_points_below_40.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR3}"
echo " "

<<COMMENT

echo "Running for M: 40-80"
OUT_DIR4="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/40-80/run05_gwfish_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_posteriors_10K_1839_events_pop_from_XPHM_fm2_netw_40-80.pkl \
	--out-dir "${OUT_DIR4}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_3325292_points_40-80.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR4}"
echo " "


echo "Running for M: 40-80"
OUT_DIR5="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/40-80/run08_gwfish_MDhigh_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_4_PLP_z_MDhigh_zp_2.53_zmax_10_lmrd_22_no_spins_posteriors_10K_2258_events_pop_from_XPHM_fm2_netw_40-80.pkl \
	--out-dir "${OUT_DIR5}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_4_pop_PLP_spin_prec_fref_10_z_MDhigh_zp_2.53_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_3324272_points_40-80.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR5}"
echo " "
COMMENT

OUT_DIR6="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/40-80/run09_gwfish_MDlow_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_5_PLP_z_MDlow_zp_1.54_zmax_10_lmrd_22_no_spins_posteriors_10K_1554_events_pop_from_XPHM_fm2_netw_40-80.pkl \
	--out-dir "${OUT_DIR6}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_5_pop_PLP_spin_prec_fref_10_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_3325563_points_40-80.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR6}"
echo " "

<<COMMENT
echo "Running for M > 80"
OUT_DIR7="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/above_80/run07_gwfish_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_posteriors_10K_256_events_pop_from_XPHM_fm2_netw_above_80.pkl \
	--out-dir "${OUT_DIR7}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_238011_points_above_80.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR7}"
echo " "

echo "Running for M > 80"
OUT_DIR8="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/above_80/run10_gwfish_MDhigh_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_4_PLP_z_MDhigh_zp_2.53_zmax_10_lmrd_22_no_spins_posteriors_10K_313_events_pop_from_XPHM_fm2_netw_above_80.pkl \
	--out-dir "${OUT_DIR8}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_4_pop_PLP_spin_prec_fref_10_z_MDhigh_zp_2.53_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_237970_points_above_80.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR8}"
echo " "
COMMENT

OUT_DIR9="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp/mass_bands/above_80/run11_gwfish_MDlow_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/LHI_Asharp_5_PLP_z_MDlow_zp_1.54_zmax_10_lmrd_22_no_spins_posteriors_10K_202_events_pop_from_XPHM_fm2_netw_above_80.pkl \
	--out-dir "${OUT_DIR9}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/LHI_Asharp_SNR_5_pop_PLP_spin_prec_fref_10_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_238410_points_above_80.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
	--out-dir "${OUT_DIR9}"
echo " "

<<COMMENT
OUT_DIR1="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/below_40/run08_gwfish_mf_from_gaussian_SNR_injections_XPHM"
echo "Running for M < 40"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_posteriors_10K_4895_events_pop_from_XPHM_fm2_netw_below_40.pkl \
	--out-dir "${OUT_DIR1}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_3406035_points_below_40.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR1}" --num-samples 2000
echo " "

OUT_DIR2="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/below_40/run09_gwfish_MDhigh_mf_from_gaussian_SNR_injections_XPHM"
echo "Running for M < 40"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_4_PLP_z_MDhigh_zp_2.53_zmax_10_lmrd_22_no_spins_posteriors_10K_4138_events_pop_from_XPHM_fm2_netw_below_40.pkl \
	--out-dir "${OUT_DIR2}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_4_pop_PLP_spin_prec_fref_5_z_MDhigh_zp_2.53_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_3406184_points_below_40.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR2}" --num-samples 2000
echo " "

OUT_DIR3="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/below_40/run10_gwfish_MDlow_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_5_PLP_z_MDlow_zp_1.54_zmax_10_lmrd_22_no_spins_posteriors_10K_3316_events_pop_from_XPHM_fm2_netw_below_40.pkl \
	--out-dir "${OUT_DIR3}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_5_pop_PLP_spin_prec_fref_5_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_3405816_points_below_40.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR3}" --num-samples 2000
echo " "

echo "Running for M in [40, 80]"
OUT_DIR4="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/40-80/run06_gwfish_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_posteriors_10K_909_events_pop_from_XPHM_fm2_netw_40-80.pkl \
	--out-dir "${OUT_DIR4}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_554229_points_40-80.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR4}"

OUT_DIR5="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/40-80/run07_gwfish_MDhigh_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_4_PLP_z_MDhigh_zp_2.53_zmax_10_lmrd_22_no_spins_posteriors_10K_677_events_pop_from_XPHM_fm2_netw_40-80.pkl \
	--out-dir "${OUT_DIR5}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_4_pop_PLP_spin_prec_fref_5_z_MDhigh_zp_2.53_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_554178_points_40-80.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR5}"

OUT_DIR6="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/40-80/run08_gwfish_MDlow_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_5_PLP_z_MDlow_zp_1.54_zmax_10_lmrd_22_no_spins_posteriors_10K_575_events_pop_from_XPHM_fm2_netw_40-80.pkl \
	--out-dir "${OUT_DIR6}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_5_pop_PLP_spin_prec_fref_5_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_554444_points_40-80.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR6}"
echo " "
echo " "

echo "Running for M > 80"
OUT_DIR7="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/above_80/run06_gwfish_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_2_PLP_z_MD_zmax_10_lmrd_22_no_spins_posteriors_10K_56_events_pop_from_XPHM_fm2_netw_above_80.pkl \
	--out-dir "${OUT_DIR7}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_2_pop_PLP_spin_prec_z_MD_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_39729_points_above_80.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR7}"

OUT_DIR8="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/above_80/run07_gwfish_MDhigh_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_4_PLP_z_MDhigh_zp_2.53_zmax_10_lmrd_22_no_spins_posteriors_10K_46_events_pop_from_XPHM_fm2_netw_above_80.pkl \
	--out-dir "${OUT_DIR8}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_4_pop_PLP_spin_prec_fref_5_z_MDhigh_zp_2.53_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_39633_points_above_80.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR8}"

OUT_DIR9="/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/mass_bands/above_80/run08_gwfish_MDlow_mf_from_gaussian_SNR_injections_XPHM"
python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/posteriors_from_GWFish/mass_bands/CE4020ET123_CoBA10_5_PLP_z_MDlow_zp_1.54_zmax_10_lmrd_22_no_spins_posteriors_10K_40_events_pop_from_XPHM_fm2_netw_above_80.pkl \
	--out-dir "${OUT_DIR9}" \
	--detected-injections-file /home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/mass_bands/XPHM/CE4020ET123_CoBA10_SNR_5_pop_PLP_spin_prec_fref_5_z_MDlow_zp_1.54_zmax_10_lmrd_22_corrected_td_detected_injs_mf_from_gaussian_SNR_39732_points_above_80.pkl \
	--label CE4020ET123
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR9}"
echo " "
echo " "
COMMENT

source activate gwpopulation
OUT_DIR1="/home/divyajyoti.nln/Post-O5-study/data/population_analysis/gwpopulation/gwpop_analysis_results/Asharp/run01_gwfish_mf_from_gaussian"

python gwpop_analysis.py \
	--posterior-file /home/divyajyoti.nln/Post-O5-study/data/population_analysis/gwpopulation/posteriors_from_GWFish/LHV_ASharp_2_PLP_z_MD_zmax_10_lmrd_19_no_spins_z_posteriors_10K_1713_events_pop_from_XPHM_fm2_netw.pkl \
	--out-dir "${OUT_DIR1}" \
	--detected-injections-file /home/divyajyoti.nln/Post-O5-study/data/population_analysis/gwpopulation/injections/LHV_ASharp_SNR_2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_19_detected_injs_mf_from_gaussian_SNR_30M_points_XPHM.pkl \
	--label Asharp
echo " "
echo "Calcuting variance"
python post_proc_checks_gwpop.py \
        --out-dir "${OUT_DIR1}"

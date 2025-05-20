python gen_WF_calc_SNR.py \
	--param-file /home/divyajyoti/ACADEMIC/Projects/Cardiff_University/Next_gen_detectability/calc_SNR_next_gen/param_data_files/BBH/pop_PLP_prec_z_MD_zmax_10_1_day.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:aLIGOZeroDetHighPower \
                H1:aLIGOZeroDetHighPower \
                V1:AdvVirgo \
	--out-dir /home/divyajyoti/ACADEMIC/Projects/Cardiff_University/Next_gen_detectability/calc_SNR_next_gen/output_data/Test_data \
        --set-name 1_day_prec_z_10_local 

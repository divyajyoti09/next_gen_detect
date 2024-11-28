python gen_WF_calc_SNR.py \
	--param-file /Users/gravity/ACADEMIC/Projects/Cardiff_University/calc_SNR_next_gen/param_data_files/test_pop_day.h5 \
        --approximant IMRPhenomPv2 \
        --detectors-and-psds \
		L1:aLIGOZeroDetHighPower \
                H1:aLIGOZeroDetHighPower \
                V1:AdvVirgo \
	--out-dir /Users/gravity/ACADEMIC/Projects/Cardiff_University/calc_SNR_next_gen/output_data \
        --set-name 1_day_prec_z_10_local

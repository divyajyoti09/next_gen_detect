with open("job_args.txt", "w") as f:
    for i in range(2):
        f.write(f"/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/injections/input_files/1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_part{i}.h5, LHI_SNR_1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_part{i}, {i}\n")

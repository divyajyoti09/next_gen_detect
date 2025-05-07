with open("job_args.txt", "w") as f:
    for i in range(2):
        f.write(f"1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td_part{i}.h5, LHI_SNR_1_pop_PLP_spin_prec_z_MD_zmax_6_lmrd_22_corrected_td, {i}\n")

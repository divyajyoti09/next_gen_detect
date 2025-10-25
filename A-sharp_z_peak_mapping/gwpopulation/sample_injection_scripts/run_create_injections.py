import subprocess
import signal
import os
from tqdm import tqdm

pop_str = '2_pop_PLP_spin_prec_fref_10_z_MD_zmax_10_lmrd_22_corrected_td'
output_dir = f'input_files/{pop_str}'
os.makedirs(output_dir, exist_ok=True)

try:
    for i in tqdm(range(400, 1200), desc="Generating injections"):
        cmd = [
            "python", "create_injections.py",
            "--reference-frequency", "10",
            "--config", "bbh2.ini",
            "--output-file", f"{output_dir}/{pop_str}_part{i}.h5",
            "--save-config",
            "--source-type", "bbh",
            "--num-samples", "10000",
            "--z-prob-file", "2_z_samples_prob_z_zmax_10.dat",
            "--mass-prob-file", "m1_pm1_q_pq.dat",
            "--log-level", "error"
        ]
        proc = subprocess.Popen(cmd)
        proc.wait()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received — terminating current job...")
    try:
        proc.send_signal(signal.SIGINT)  # forward interrupt to child
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
    print("All remaining jobs aborted.")

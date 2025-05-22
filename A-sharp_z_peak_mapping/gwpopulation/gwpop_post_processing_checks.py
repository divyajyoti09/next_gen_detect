import bilby
from gwpopulation_pipe.post_plots import redshift_spectrum_plot
import argparse

result = bilby.result.read_in_result(filename='/home/divyajyoti/ACADEMIC/Projects/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/CE4020ET123/run01_mf_SNR_injections/CE4020ET123_result.hdf5')
#result.meta_data["models"] = {'redshift':'MadauDickinsonRedshift'}
result.meta_data["models"] = {}

parser = argparse.ArgumentParser()
parser.add_argument('--upper-limit', type=float)
parser.add_argument('--lower-limit', type=float)
parser.add_argument('--redshift-model')
parser.add_argument('--z_max', type=float)
args = parser.parse_args('--upper-limit 10'.split())

redshift_spectrum_plot([result], args)

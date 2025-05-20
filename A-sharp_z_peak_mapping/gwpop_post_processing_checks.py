import bilby
from gwpopulation_pipe.post_plots import redshift_spectrum_plot
import argparse

result = bilby.result.read_in_result(filename='/home/divyajyoti.nln/Cardiff_University/Next_gen_detectability/A-sharp-study/gwpopulation/BBH/gwpop_analysis_results/Asharp-study-gwpop_result.hdf5')
result.meta_data["models"] = {}

parser = argparse.ArgumentParser()
parser.add_argument('--upper-limit', type=float)
parser.add_argument('--lower-limit', type=float)
parser.add_argument('--redshift-model')
args = parser.parse_args('--lower-limit 0.0001 --upper-limit 8'.split())

redshift_spectrum_plot([result], args)

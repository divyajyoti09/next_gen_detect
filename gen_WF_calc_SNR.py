from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter,ArgumentError
import deepdish as dd
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from copy import deepcopy
from conversions import convert_pesummary_to_pycbc
from detectors import get_available_detectors_list, get_available_detectors_full_names
import logging
import numpy as np
from pycbc.waveform import get_fd_waveform, fd_waveform_params
import pandas as pd
from pycbc.detector import Detector
from pycbc.filter import sigma
from pycbc import psd
import time
from multiprocessing import Pool
import math
from pycbc import pnutils
from detector_psds import get_available_psds, generate_psd
import h5py
import random
from pycbc.types import FrequencySeries
from pycbc.filter.matchedfilter import matched_filter
from pycbc.noise import frequency_noise_from_psd
from scipy.stats import ncx2

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Check if GWForge package is installed

try:
    import GWForge
    gwforge_available = True
except ImportError:
    logging.warning("Unable to import GWForge. Will not be able to access the modules/detectors available in GWForge!")
    gwforge_available = False

start_time = time.time()

# Initial parser parses for arguments which are not required by the main script but are useful for the user

initial_parser = ArgumentParser(add_help=False, allow_abbrev=False)
initial_parser.add_argument("--available-detectors", action='store_true', 
                            help="Returns a list of the available detectors")
initial_parser.add_argument("--available-psd-models", action='store_true',
                            help="Returns a list of the available PSD models")
initial_args, remaining_args = initial_parser.parse_known_args()

req = not any(vars(initial_args).values())

available_detectors_full_names = get_available_detectors_full_names()
available_detectors = get_available_detectors_list()

available_psd_models = get_available_psds()

# Detector PSD validator class validates that the detectors and PSDs input by the user exist

class DetectorPSDValidator:
    def __init__(self, available_detectors, available_psd_models):
        """
        Validator for detectors and PSD models.

        Parameters:
        -----------
        available_detectors : list
            A list of valid detector names.
        available_psd_models : list
            A list of valid PSD model names.
        """
        self.available_detectors = available_detectors
        self.available_psd_models = available_psd_models

    def __call__(self, value):
        """
        Validates a detector and its PSD model provided as 'detector:PSD_model'.

        Parameters:
        -----------
        value : str
            Input string in the format 'detector:PSD_model'.

        Returns:
        --------
        tuple
            A tuple of (detector, PSD_model) if validation succeeds.

        Raises:
        -------
        ArgumentError
            If either the detector or PSD model is invalid.
        """
        try:
            detector, psd_model = value.strip().split(":")
        except ValueError:
            raise ArgumentError(None, f"Invalid format '{value}'. Expected 'detector:PSD_model'.")
        
        if detector not in self.available_detectors:
            raise ArgumentError(None, f"Detector '{detector}' not available. "
                                      f"Available detectors: {', '.join(self.available_detectors)}")
        
        if psd_model not in self.available_psd_models:
            logging.warning(f"PSD model {psd_model} not available. \nChecking if this is a file path..")
            if os.path.isfile(psd_model):
                print("File found")
            else:
                raise ArgumentError(None, f"{psd_model} path not found.")
        
        return detector, psd_model

# Main argument parser

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, allow_abbrev=False)
parser.add_argument("--param-file", required=req,
                   help="Path to the h5 file containing source parameters")
parser.add_argument("--num-samples", type=int,
                   help="Number of samples to be drawn randomly from the param-file")
parser.add_argument("--approximant", required=req,
                   help="LAL approximant for waveform generation")
parser.add_argument("--out-dir",
                   help="Path to the directory where output files will be saved. If None, files will be saved in the current directory.")
parser.add_argument("--input-param-names-format", choices={'PyCBC', 'PESummary', 'Bilby'}, default='PESummary',
                   help="The parameter names format in param-file Eg. mass_1 is Bilby/PESummary but mass1 is PyCBC")
parser.add_argument("--set-name", default="Test_Set",
                   help="Name which will be used in naming output files.")
parser.add_argument("--generate-only-waveforms", action="store_true",
                   help="If specified, generates waveforms for all sets of parameters in the param-file but doesn't calculate SNR.")
parser.add_argument("--calc-snr-from-waveforms", action="store_true",
                   help="If specified, looks for h_plus, h_cross keys in the --param-file and uses those to calculate SNR for different detectors. All waveforms should be of equal length because PSDs are not generated separately for each sample.")
parser.add_argument("--samples-key", 
                   help="Top level to look for parameters. Eg. --samples-key waveforms for data such as {'waveforms': {'param1':[...], 'param2':[...]}}. If None, it is assumed that the parameters are at the top level of the data file.")
parser.add_argument("--num-procs", type=int,
                   help="Number of processes to distribute task over, uses multiprocessing. If None, the process the carried out without multiprocessing.")
parser.add_argument("--delta-f", type=float, default=0.01,
                   help="The frequency step used to generate the waveform in frequency domain (in Hz)")
parser.add_argument("--delta-t", type=float, default=1/1024,
                   help="The time step used to generate the waveform (in s)")
parser.add_argument("--f-low", type=float, default=5,
                   help="Starting frequency for waveform generation and integration (in Hz)")
parser.add_argument("--f-high", type=float, default=1024,
                    help="Upper frequency cut-off for waveform generation and integration (in Hz)")
parser.add_argument("--available-detectors", action='store_true',
                   help="Returns a list of all available detectors along with full names (if specified in source).")
parser.add_argument("--available-psd-models", action='store_true', 
                   help="Returns a list of the available PSD models")
parser.add_argument("--detectors-and-psds", 
                   default=[('L1', 'aLIGOZeroDetHighPower'), 
                            ('H1', 'aLIGOZeroDetHighPower'), 
                            ('V1', 'AdvVirgo')],
                   nargs='+',
                   type=DetectorPSDValidator(available_detectors, available_psd_models), 
                   metavar='det:PSD_model',
                   help="Specify detectors and their PSD models in the format 'detector:PSD_model' or 'detector:/path/to/psd/file'. \nUse --available-detectors or --available-psd-models to see the list of all available detectors and PSD models respectively. \nUse --is-asd option in addition to this option to indicate that the files are ASD not PSD")
parser.add_argument("--is-asd", action="store_true",
                   help="Use this option to indicate that the PSD files provided in --detectors-and-psds are ASD files. When not specified, the files are treated as PSD files.")
parser.add_argument("--write-out-file-with", choices={'pandas', 'h5py'}, default='h5py',
                    help="The structure of the h5 file will depend on whether it is written with pandas.Dataframe.to_hdf() or using h5py.")
parser.add_argument("--max-worker-chunksize", type=int, default=40,
                    help="Maximum worker chunksize to be alloted when using Pool. Use this with --num-procs option if needed")

args = parser.parse_args()

if args.available_detectors:
    for det in available_detectors_full_names.items():
        print(det)
    exit()

if args.available_psd_models:
    for psd_model in available_psd_models:
        print(psd_model)
    exit()

###########

def waveform_gen_base(pycbc_fd_wf_params):
    """
    Generates waveform for a given set of parameters
    
    Parameters: 
    -----------
    pycbc_fd_wf_params: key, value mappings as a dictionary or a row of pandas dataframe
        Takes all arguments accepted by PyCBC function `pycbc.waveform.get_fd_waveform`

    Returns:
    -----------
    hp: PyCBC Frequency series
        h_plus
    hc: PyCBC Frequency series
        h_cross
    """

    if type(pycbc_fd_wf_params) == dict:
        wf_kwargs = deepcopy(pycbc_fd_wf_params)
    else:
        wf_kwargs = pycbc_fd_wf_params.to_dict()
    
    hpf, hcf = get_fd_waveform(**wf_kwargs)

    return(hpf, hcf, wf_kwargs)

###################################

def project_signal_in_detector(hpf, hcf, ra, dec, polarization, ifo, trigger_time):
    
    """
    Generates waveform for a given set of parameters
    
    Parameters: 
    -----------
    hpf: PyCBC frequency series or time series
        h_plus
    hcf: PyCBC frequency series or time series
        h_cross
    ra: float
        right ascension (in radian)
    dec: float
        declination (in radian)
    polarization: float
        polarization angle (in radian)
    ifo: str
        short name of the detector
    trigger_time: float
        reference GPS time (in seconds)

    Returns:
    ---------
    hf: PyCBC frequency or time series (based on the input)
        hf = h_plus * f_plus + h_cross * f_cross
    """

    d = Detector(ifo)
    fp, fc = d.antenna_pattern(ra, dec, polarization, trigger_time)
    
    hf = fp * hpf + fc * hcf
    
    return(hf)

#####################################################

def calc_PSD(ifo, length, delta_f, f_low):
    """
    Calculates PSD for a given detector by looking up the input argument given to argparse in the form of --detectors-and-psds det:PSD_model

    Parameters:
    -----------
    ifo: str
        short name of the detector
    length: int
        length of the array to be generated
    delta_f: float
        Frequency step used to generate the waveform
    f_low: float
        Starting frequency for PSD generation

    Returns:
    ------------
    PyCBC FrequencySeries for PSD
    """
    psd_model = dict(args.detectors_and_psds)[ifo]
    if psd_model in available_psd_models:
        psd_data = generate_psd(psd_model, length, delta_f, f_low)
    else:
        if args.is_asd:
            is_asd = True
        else:
            is_asd = False
        psd_data = psd.from_txt(psd_model, length, delta_f, f_low, is_asd_file=is_asd)
    return(psd_data)

###########

class calc_snr:
    def __init__(self, psd_data_dict):
        """
        Initializes the class with a psd_data_dict which is a dictionary with keys as ifo names and values as the respective PSD data
        """
        self.psd_data_dict = psd_data_dict
        self.noise_dict = {}
        for key in psd_data_dict.keys():
            self.noise_dict[key] = frequency_noise_from_psd(psd=psd_data_dict[key])

    def add_noise_to_signal(self, htilde, ifo):
        """
        Adds noise to the signal provided

        Parameters:
        --------------
        htilde: Frequency Series
            Input vector containing the waveform
        ifo: str
            short name of the detector

        Returns:
        ----------------
        noise + htilde (PyCBC FrequencySeries)
        """
        #noise = frequency_noise_from_psd(psd=self.psd_data_dict[ifo])
        noise = self.noise_dict[ifo]
        if len(htilde) != len(self.psd_data_dict[ifo]):
            logging.warning("len(hf) > len(PSD_array). The calculation will only be done where PSD data is present.")
            data = noise + htilde[:len(noise)]
        else:
            data = noise + htilde
        return(data)

    def calc_opt_snr(self, htilde, ifo, f_low):
        """
        Calculates optimal SNR

        Parameters:
        ------------
        htilde: PyCBC TimeSeries or Frequency Series
            Input vector containing the waveform
        ifo: str
            short name of the detector
        f_low: float
            starting frequency calculate SNR

        Returns:
        ---------
        Optimal SNR (float)
        """
        if len(htilde) != len(self.psd_data_dict[ifo]):
            logging.warning("len(hf) > len(PSD_array). The SNR calculation will only be done where PSD data is present.")
            opt_snr = sigma(htilde[:len(self.psd_data_dict[ifo])], self.psd_data_dict[ifo], low_frequency_cutoff=f_low)
        else:
            opt_snr = sigma(htilde, self.psd_data_dict[ifo], low_frequency_cutoff=f_low)
        return (opt_snr)

    def calc_mf_from_opt_snr(self, opt_snr_sq):
        """
        Calcultes matched filter SNR from optimal SNR using chi_sq distribution

        Parameters:
        -------------
        opt_snr_sq: float
            square of the optimal snr

        Returns:
        -------------
        matched filter snr (float)
        """
        mf_snr_sq = ncx2.rvs(2, opt_snr_sq)
        mf_snr = np.sqrt(mf_snr_sq)
        return(mf_snr)

    def calc_mf_snr(self, template, ifo, f_low, opt_snr_sq):
        """
        Calculates matched filter SNR

        Parameters:
        ------------
        template: PyCBC TimeSeries or Frequency Series
            Input vector containing the waveform
        ifo: str
            short name of the detector
        f_low: float
            starting frequency calculate SNR
        opt_snr_sq: float
            square of the optimal snr

        Returns:
        ---------
        Maximum of absolute of the complex matched filter SNR (float)
        """
        data = self.add_noise_to_signal(template, ifo)

        if len(data) != len(self.psd_data_dict[ifo]) or len(template) != len(self.psd_data_dict[ifo]):
            logging.warning("len(hf) > len(PSD_array). The SNR calculation will only be done where PSD data is present.")
            mf_snr = matched_filter(template[:len(self.psd_data_dict[ifo])], data[:len(self.psd_data_dict[ifo])], psd=self.psd_data_dict[ifo], low_frequency_cutoff=f_low, sigmasq=opt_snr_sq)
        else:
            mf_snr = matched_filter(template, data, psd=self.psd_data_dict[ifo], low_frequency_cutoff=f_low, sigmasq=opt_snr_sq)
        return (max(abs(mf_snr)))

###########

# Find the lowest mass1 and mass2 values and highest spin1z and spin2z values to determine the (maximum) length of PSD to be generated

def find_max_PSD_length(method, params_dict_PyCBC):
    """
    Finds the maximum length of the PSD that needs to be generated to account for all the samples and maximum final frequency for waveform generation (if needed)
    
    Parameters:
    ------------
    method: str, choices = {'mass_spin', waveform_length}
        mass_spin: Uses the minimum mass1 and mass2 values and the maximum spin1z and spin2z values in the samples to generate a waveform with IMRPhenomXAS
        waveform_length: Assumes all waveforms in the samples are equal length and returns that length
    params_dict_PyCBC: dict
        dictionary containing parameter values with parameter names in PyCBC format

    Returns:
    -------------
    (max_PSD_length, max_f_final, delta_f, f_low)
    max_PSD_length: int
        maximum length of PSD
    max_f_final: float
        maximum f_final to be used for waveform generation
    delta_f: float
        Frequency time-step
    f_low: float
        Start frequency of waveform and PSD generation
    """
    if method == 'mass_spin':
        min_mass1 = min(params_dict_PyCBC['mass1'])
        min_mass2 = min(params_dict_PyCBC['mass2'])
        max_spin1z = max(params_dict_PyCBC['spin1z'])
        max_spin2z = max(params_dict_PyCBC['spin2z'])

        max_f_final = math.ceil(pnutils.get_final_freq('IMRPhenomXAS', min_mass1, min_mass2, max_spin1z, max_spin2z))
        if max_f_final > args.f_high:
            max_f_final = args.f_high
        
        hp_init, hc_init = get_fd_waveform(approximant = "IMRPhenomXP", 
                                           mass1 = min_mass1, 
                                           mass2 = min_mass2, 
                                           spin1z = max_spin1z,
                                           spin2z = max_spin2z,
                                           f_lower = args.f_low, 
                                           f_final = max_f_final, 
                                           delta_f = args.delta_f)        
        max_PSD_length = len(hp_init)
        return(max_PSD_length, max_f_final, args.delta_f, args.f_low)
    
    elif method == 'waveform_length':
        max_PSD_len = len(params_dict_PyCBC['h_plus'][0])
        max_f_final = params_dict_PyCBC['f_final'][0]
        delta_f = params_dict_PyCBC['delta_f'][0]
        f_low = params_dict_PyCBC['f_low'][0]
        return(max_PSD_length, max_f_final, delta_f, f_low)

#########################

def hdf_append(f, key, value, group=None):
    # Create the group if it doesn't exist
    if group:
        if group not in f:
            f.create_group(group)
        target = f[group]
    else:
        target = f

    # Convert pandas Series to numpy array
    if hasattr(value, 'values'):
        value = value.values

    value = np.atleast_1d(value)

    # Handle string data explicitly
    if value.dtype.kind in {'U', 'O'}:
        dt = h5py.string_dtype(encoding='utf-8')
        value = value.astype(str).astype(dt)

    if key in target:
        tmp = np.concatenate([target[key][:], value])
        del target[key]
        target.create_dataset(key, data=tmp)
    else:
        target.create_dataset(key, data=value)

###############################################

# Load data from the parameter file

load_params_file = dd.io.load(args.param_file)
params_dict = deepcopy(load_params_file)

config_dict = params_dict.pop("config", None)
    
if args.samples_key:
    params_dict = params_dict[args.samples_key]

# Convert the parameter names in the data files to PyCBC names

if args.input_param_names_format == 'PyCBC':
    params_dict_PyCBC0 = deepcopy(params_dict)
else:
    params_dict_PyCBC0 = convert_pesummary_to_pycbc(params_dict)

if args.num_samples:
    num_samples = args.num_samples
    if num_samples > len(params_dict_PyCBC0['mass1']):
        logging.warning(f'num_samples > number of available samples (={len(params_dict_PyCBC0["mass1"])}) in the param-file. All samples from the param-file will be used.')
        params_dict_PyCBC = deepcopy(params_dict_PyCBC0)
    else:
        params_dict_PyCBC = {}
        random_idxs = random.sample(list(np.arange(len(params_dict_PyCBC0['mass1']))), num_samples)
        for key in params_dict_PyCBC0.keys():
            params_dict_PyCBC[key] = params_dict_PyCBC0[key][random_idxs]
else:
    params_dict_PyCBC = deepcopy(params_dict_PyCBC0)

# Separate the waveform generation parameters and the location parameters

wf_gen_params_dict = {}
location_dict = {}
other_params_dict = {}

for key in params_dict_PyCBC.keys():    
    if key in fd_waveform_params:
        wf_gen_params_dict[key] = params_dict_PyCBC[key]    
    elif key in ['ra', 'dec', 'polarization', 'trigger_time']:
        location_dict[key] = params_dict_PyCBC[key]
    else:
        other_params_dict[key] = params_dict_PyCBC[key]

if 'trigger_time' not in location_dict.keys():
    logging.warning("trigger_time not found in input parameters. Setting trigger_time = numpy.arange(0, len(ra) * 1000, 1000)")
    location_dict["trigger_time"] = np.arange(0, len(location_dict["ra"]) * 1000, 1000)

sample_length = len(params_dict_PyCBC['mass1'])
print(f'\nSample length = {sample_length}')

wf_gen_params_dict.update(
    {'approximant': [args.approximant]*sample_length, 
     'f_lower': [args.f_low]*sample_length, 
     'delta_f': [args.delta_f]*sample_length})

# Get the detector network

PSD_model_names_dict = {}
detectors_and_psds_dict = dict(args.detectors_and_psds)
network = detectors_and_psds_dict.keys()

if args.calc_snr_from_waveforms:
    max_PSD_length, max_f_final, delta_f, f_low = find_max_PSD_length('waveform_length', params_dict_PyCBC)
else:
    max_PSD_length, max_f_final, delta_f, f_low = find_max_PSD_length('mass_spin', params_dict_PyCBC)
    
wf_gen_params_dict['f_final'] = [max_f_final]*sample_length

# Generate PSDs for all the detectors

PSD_dict = {}

for ifo in network:
    PSD_dict[ifo] = calc_PSD(ifo, max_PSD_length, args.delta_f, args.f_low)
    PSD_model_name = detectors_and_psds_dict[ifo]
    if ".dat" in PSD_model_name or ".txt" in PSD_model_name:
        PSD_model_names_dict[f'PSD_{ifo}'] = [PSD_model_name.split('/')[-1]]*sample_length
    else:
        PSD_model_names_dict[f'PSD_{ifo}'] = [PSD_model_name]*sample_length

# Initialize the calc_opt_snr class with PSD_dict

calc_snr_call = calc_snr(PSD_dict)

# Calculate SNR for all samples

wf_gen_params_df = pd.DataFrame(wf_gen_params_dict)
location_df = pd.DataFrame(location_dict)
other_params_df = pd.DataFrame(other_params_dict)
PSD_model_names_df = pd.DataFrame(PSD_model_names_dict)

results_dict = deepcopy(location_dict)
hf_dict = {}
snr_dict_opt = {}
snr_dict_mf_from_opt = {}
snr_dict_mf = {}

# If sample size is large, divide into chunks
if sample_length >= 250:
    n_chunks = math.ceil(sample_length/250)
    print(f'Sample length > 250. Dividing into {n_chunks} chunks.\n')
else:
    n_chunks = 1
wf_gen_params_df_chunked = np.array_split(wf_gen_params_df, n_chunks)
location_df_chunked = np.array_split(location_df, n_chunks)
results_df_chunked = []

if args.num_procs == None:
    for wf_gen_chunk, location_chunk, i in zip(wf_gen_params_df_chunked, location_df_chunked, range(1, n_chunks+1)):
        if n_chunks != 1:
            print("\nProcessing chunk {}, length = {}".format(i, len(location_chunk['ra'])))
        print("Generating waveforms")
        wf_data = list(map(waveform_gen_base, wf_gen_chunk.to_dict(orient='records')))
        hpf_data = np.array(wf_data, dtype="object")[:,0]
        hcf_data = np.array(wf_data, dtype="object")[:,1]
        #results_dict.update(pd.DataFrame.from_records(np.array(wf_data, dtype="object")[:,2]).to_dict(orient='list'))
        results_chunk = pd.DataFrame.from_records(np.array(wf_data, dtype="object")[:,2])
        results_chunk.index = location_chunk.index
        results_chunk = pd.concat([results_chunk, location_chunk], axis=1)

        netw_SNR_sq_opt = np.zeros(len(results_chunk))
        netw_SNR_sq_mf_from_opt = np.zeros(len(results_chunk))
        netw_SNR_sq_mf = np.zeros(len(results_chunk))
    
        for IFO in network:
            location_chunk['ifo'] = [IFO]*len(location_chunk['ra'])
            print(f"Calculating SNR for {IFO}")
            hf_dict[IFO] = list(map(project_signal_in_detector, 
                                    hpf_data,
                                    hcf_data,
                                    location_chunk['ra'],
                                    location_chunk['dec'],
                                    location_chunk['polarization'],
                                    location_chunk['ifo'],
                                    location_chunk['trigger_time']))
            snr_dict_opt[IFO] = list(map(calc_snr_call.calc_opt_snr,
                                     hf_dict[IFO],
                                     location_chunk['ifo'],
                                     wf_gen_chunk['f_lower']))
            snr_dict_mf_from_opt[IFO] = list(map(calc_snr_call.calc_mf_from_opt_snr, np.array(snr_dict_opt[IFO])**2))
            snr_dict_mf[IFO] = list(map(calc_snr_call.calc_mf_snr,
                                     hf_dict[IFO],
                                     location_chunk['ifo'],
                                     wf_gen_chunk['f_lower'],
                                     np.array(snr_dict_opt[IFO])**2))
            results_chunk['SNR_%s'%IFO] = snr_dict_opt[IFO]
            results_chunk['SNR_mf_from_opt_%s'%IFO] = snr_dict_mf_from_opt[IFO]
            results_chunk['SNR_mf_%s'%IFO] = snr_dict_mf[IFO]
            netw_SNR_sq_opt += np.array(snr_dict_opt[IFO])**2
            netw_SNR_sq_mf_from_opt += np.array(snr_dict_mf_from_opt[IFO])**2
            netw_SNR_sq_mf += np.array(snr_dict_mf[IFO])**2
    
        results_chunk['SNR_network'] = list(np.sqrt(netw_SNR_sq_opt))
        results_chunk['SNR_mf_from_opt_network'] = list(np.sqrt(netw_SNR_sq_mf_from_opt))
        results_chunk['SNR_mf_network'] = list(np.sqrt(netw_SNR_sq_mf))
        results_df_chunked.append(results_chunk)

if args.num_procs:
    print(f'Using multiprocessing with {args.num_procs} processes...')
    if __name__=='__main__':
        with Pool(args.num_procs) as p:
            for wf_gen_chunk, location_chunk, i in zip(wf_gen_params_df_chunked, location_df_chunked, range(1, n_chunks+1)):
                worker_chunksize = min(len(location_chunk['ra'])//args.num_procs, args.max_worker_chunksize)
                if n_chunks != 1:
                    print("\nProcessing chunk {}, length = {}".format(i, len(location_chunk['ra'])))
                print("Generating waveforms using imap")
                print(f"Chunksize for imap = {worker_chunksize}")
                wf_data = list(p.imap(waveform_gen_base, wf_gen_chunk.to_dict(orient='records'), chunksize=worker_chunksize))
                hpf_data = np.array(wf_data, dtype="object")[:,0]
                hcf_data = np.array(wf_data, dtype="object")[:,1]
                #results_dict.update(pd.DataFrame.from_records(np.array(wf_data, dtype="object")[:,2]).to_dict(orient='list'))
                results_chunk = pd.DataFrame.from_records(np.array(wf_data, dtype="object")[:,2])
                results_chunk.index = location_chunk.index
                results_chunk = pd.concat([results_chunk, location_chunk], axis=1)

                netw_SNR_sq_opt = np.zeros(len(results_chunk))
                netw_SNR_sq_mf_from_opt = np.zeros(len(results_chunk))
                netw_SNR_sq_mf = np.zeros(len(results_chunk))
                
                for IFO in network:
                    location_chunk['ifo'] = [IFO]*len(location_chunk['ra'])
                    print(f"Calculating SNR for {IFO}")
                    hf_dict[IFO] = list(p.starmap(project_signal_in_detector, 
                                                  zip(hpf_data, 
                                                      hcf_data, 
                                                      location_chunk['ra'], 
                                                      location_chunk['dec'], 
                                                      location_chunk['polarization'], 
                                                      location_chunk['ifo'], 
                                                      location_chunk['trigger_time']
                                                     )
                                                 )
                                       )
                    snr_dict_opt[IFO] = list(p.starmap(calc_snr_call.calc_opt_snr,
                                                   zip(hf_dict[IFO],
                                                       location_chunk['ifo'],
                                                       wf_gen_chunk['f_lower'])))
                    snr_dict_mf_from_opt[IFO] = list(p.starmap(calc_snr_call.calc_mf_from_opt_snr, [(x,) for x in (np.array(snr_dict_opt[IFO])**2)]))
                    snr_dict_mf[IFO] = list(p.starmap(calc_snr_call.calc_mf_snr,
                                                   zip(hf_dict[IFO],
                                                       location_chunk['ifo'],
                                                       wf_gen_chunk['f_lower'],
                                                       np.array(snr_dict_opt[IFO])**2)))
                    results_chunk['SNR_%s'%IFO] = snr_dict_opt[IFO]
                    results_chunk['SNR_mf_from_opt_%s'%IFO] = snr_dict_mf_from_opt[IFO]
                    results_chunk['SNR_mf_%s'%IFO] = snr_dict_mf[IFO]
                    netw_SNR_sq_opt += np.array(snr_dict_opt[IFO])**2
                    netw_SNR_sq_mf_from_opt += np.array(snr_dict_mf_from_opt[IFO])**2
                    netw_SNR_sq_mf += np.array(snr_dict_mf[IFO])**2

                results_chunk['SNR_network'] = list(np.sqrt(netw_SNR_sq_opt))
                results_chunk['SNR_mf_from_opt_network'] = list(np.sqrt(netw_SNR_sq_mf_from_opt))
                results_chunk['SNR_mf_network'] = list(np.sqrt(netw_SNR_sq_mf))
                results_df_chunked.append(results_chunk)

results_df = pd.concat([PSD_model_names_df, other_params_df, pd.concat(results_df_chunked)], axis=1)

if args.out_dir == None:
    out_dir = os.getcwd()
else:
    out_dir = args.out_dir
    if not os.path.isdir(out_dir):
        logging.warning(f'{out_dir} directory not found. Creating new directory.')
        os.makedirs(out_dir)

output_file = os.path.join(out_dir, args.set_name+'_SNR_data.h5')
print(f"Writing results to file: {output_file}")

if args.write_out_file_with == 'pandas':
    results_df.to_hdf(output_file, key='Optimal_SNR', mode='w')
elif args.write_out_file_with == 'h5py':
    with h5py.File(output_file,'w') as f:
        for key in results_df.keys():
            hdf_append(f, key, results_df[key], group='results')

if config_dict != None:
    print("Writing configuration settings from param-file to output file")
    with h5py.File(output_file, "a") as h5file:  # Open in append mode to add more data
        config_group = h5file.create_group("config")  # Create a group for configuration
        for section, settings in config_dict.items():
            section_group = config_group.create_group(section)
            for key, value in settings.items():
                section_group.attrs[key] = str(value)
print("Done!")

end_time = time.time()
print(f"Total time taken = {end_time-start_time} seconds.")

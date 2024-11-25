from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter,ArgumentError
import deepdish as dd
import os
from copy import deepcopy
from conversions import convert_pesummary_to_pycbc
from pycbc.detector import get_available_detectors, get_available_lal_detectors
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

available_detectors_full_names = deepcopy(get_available_lal_detectors())
available_detectors = list(np.array(available_detectors_full_names)[:,0])

available_psd_models = psd.analytical.get_psd_model_list()

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
parser.add_argument("--approximant", required=req,
                   help="LAL approximant for waveform generation")
parser.add_argument("--out-dir",
                   help="Path to the directory where output files will be saved. If None, files will be saved in the current directory.")
parser.add_argument("--input-param-names-format", choices={'PyCBC', 'PESummary', 'Bilby'}, default='PESummary',
                   help="The parameter names format in param-file Eg. mass_1 is Bilby/PESummary but mass1 is PyCBC")
parser.add_argument("--set-name", default="Test_Set",
                   help="Name which will be used in naming output files.")
parser.add_argument("--generate-waveform", action="store_true",
                   help="If specified, generates waveforms for all sets of parameters in the param-file but doesn't calculate SNR.")
parser.add_argument("--num-procs", type=int,
                   help="Number of processes to distribute task over, uses multiprocessing. If None, the process the carried out without multiprocessing.")
parser.add_argument("--delta-f", type=float, default=0.01,
                   help="The frequency step used to generate the waveform in frequency domain (in Hz)")
parser.add_argument("--delta-t", type=float, default=1/1024,
                   help="The time step used to generate the waveform (in s)")
parser.add_argument("--f-low", type=float, default=5,
                   help="Starting frequency of integration (in Hz)")
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

args = parser.parse_args()

if args.available_detectors:
    for det in available_detectors_full_names:
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

###########

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
        psd_data = eval('psd.analytical.'+psd_model)(length, delta_f, f_low)
    else:
        if args.is_asd:
            is_asd = True
        else:
            is_asd = False
        psd_data = psd.from_txt(psd_model, length, delta_f, f_low, is_asd_file=is_asd)
    return(psd_data)

###########

class calc_opt_snr:
    def __init__(self, psd_data_dict):
        """
        Initializes the class with a psd_data_dict which is a dictionary with keys as ifo names and values as the respective PSD data
        """
        self.psd_data_dict = psd_data_dict
    def __call__(self, htilde, ifo, f_low):
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
        opt_snr = sigma(htilde, self.psd_data_dict[ifo], low_frequency_cutoff=f_low)
        return (opt_snr)

###########

# Load data from the parameter file

params_dict = dd.io.load(args.param_file)

# Convert the parameter names in the data files to PyCBC names

if args.input_param_names_format == 'PyCBC':
    params_dict_PyCBC = deepcopy(params_dict)
else:
    params_dict_PyCBC = convert_pesummary_to_pycbc(params_dict)

# Separate the waveform generation parameters and the location parameters

wf_gen_params_dict = {}
location_dict = {}

for key in params_dict_PyCBC.keys():    
    if key in fd_waveform_params:
        wf_gen_params_dict[key] = params_dict_PyCBC[key]    
    if key in ['ra', 'dec', 'polarization', 'trigger_time']:
        location_dict[key] = params_dict_PyCBC[key]

sample_length = len(params_dict_PyCBC['mass1'])
print(f'Sample length = {sample_length}')
wf_gen_params_dict.update(
    {'approximant': [args.approximant]*sample_length, 
     'f_lower': [args.f_low]*sample_length, 
     'delta_f': [args.delta_f]*sample_length})

# Get the detector network

network = dict(args.detectors_and_psds).keys()

# Find the lowest mass1 and mass2 values and highest spin1z and spin2z values to determine the (maximum) length of PSD to be generated

min_mass1 = min(params_dict_PyCBC['mass1'])
min_mass2 = min(params_dict_PyCBC['mass2'])
max_spin1z = max(params_dict_PyCBC['spin1z'])
max_spin2z = max(params_dict_PyCBC['spin2z'])

max_f_final = math.ceil(pnutils.get_final_freq('IMRPhenomXAS', min_mass1, min_mass2, max_spin1z, max_spin2z))
wf_gen_params_dict['f_final'] = [max_f_final]*sample_length

hp_init, hc_init = get_fd_waveform(approximant = "IMRPhenomXP", 
                                   mass1 = min_mass1, 
                                   mass2 = min_mass2, 
                                   spin1z = max_spin1z,
                                   spin2z = max_spin2z,
                                   f_lower = args.f_low, 
                                   f_final = max_f_final, 
                                   delta_f = args.delta_f)

max_PSD_length = len(hp_init)

# Generate PSDs for all the detectors

PSD_dict = {}

for ifo in network:
    PSD_dict[ifo] = calc_PSD(ifo, max_PSD_length, args.delta_f, args.f_low)

# Initialize the calc_opt_snr class with PSD_dict

calc_opt_snr_call = calc_opt_snr(PSD_dict)

# Calculate SNR for all samples

params_df = pd.DataFrame(params_dict_PyCBC)
wf_gen_params_df = pd.DataFrame(wf_gen_params_dict)

results_dict = deepcopy(location_dict)
hf_dict = {}
snr_dict = {}

netw_SNR_sq = np.empty(sample_length)

if args.num_procs == None:
    if sample_length >= 350:
        raise Exception(f'No. of samples = {sample_length} is too large. Please use multiprocessing.')
    wf_data = list(map(waveform_gen_base, wf_gen_params_df.to_dict(orient='records')))
    hpf_data = np.array(wf_data, dtype="object")[:,0]
    hcf_data = np.array(wf_data, dtype="object")[:,1]
    results_dict.update(pd.DataFrame.from_records(np.array(wf_data, dtype="object")[:,2]).to_dict(orient='list'))

    for IFO in network:
        print(f"Calculating SNR for {IFO}")
        hf_dict[IFO] = list(map(project_signal_in_detector, 
                                hpf_data,
                                hcf_data,
                                location_dict['ra'],
                                location_dict['dec'],
                                location_dict['polarization'],
                                [IFO]*sample_length,
                                location_dict['trigger_time']))
        snr_dict[IFO] = list(map(calc_opt_snr_call, 
                                 hf_dict[IFO], 
                                 [IFO]*sample_length,  
                                 wf_gen_params_dict['f_lower']))
        results_dict['SNR_%s'%IFO] = snr_dict[IFO]
        netw_SNR_sq += np.array(snr_dict[IFO])**2

    results_dict['SNR_network_sq'] = list(netw_SNR_sq)
    results_dict['SNR_network'] = list(np.sqrt(netw_SNR_sq))

if args.num_procs:
    print(f'Using multiprocessing with {args.num_procs} processes...')
    if __name__=='__main__':
        with Pool(args.num_procs) as p:
            print("Generating waveforms")
            wf_data = list(p.map(waveform_gen_base, wf_gen_params_df.to_dict(orient='records')))
            hpf_data = np.array(wf_data, dtype="object")[:,0]
            hcf_data = np.array(wf_data, dtype="object")[:,1]
            results_dict.update(pd.DataFrame.from_records(np.array(wf_data, dtype="object")[:,2]).to_dict(orient='list'))
            
            for IFO in network:
                location_dict['ifo'] = [IFO]*sample_length
                print(f"Calculating SNR for {IFO}")
                hf_dict[IFO] = list(p.starmap(project_signal_in_detector, 
                                              zip(hpf_data, 
                                                  hcf_data, 
                                                  location_dict['ra'], 
                                                  location_dict['dec'], 
                                                  location_dict['polarization'], 
                                                  location_dict['ifo'], 
                                                  location_dict['trigger_time']
                                                 )
                                             )
                                   )
                snr_dict[IFO] = list(p.starmap(calc_opt_snr_call, 
                                               zip(hf_dict[IFO], 
                                                   location_dict['ifo'],  
                                                   wf_gen_params_dict['f_lower'])))
                results_dict['SNR_%s'%IFO] = snr_dict[IFO]
                netw_SNR_sq += np.array(snr_dict[IFO])**2

            results_dict['SNR_network_sq'] = list(netw_SNR_sq)
            results_dict['SNR_network'] = list(np.sqrt(netw_SNR_sq))

results_df = pd.DataFrame(results_dict)
if args.out_dir == None:
    out_dir = os.getcwd()
else:
    out_dir = args.out_dir
    if not os.path.isdir(out_dir):
        logging.warning(f'{out_dir} directory not found. Creating new directory.')
        os.makedirs(out_dir)
print("Writing results to file")
results_df.to_hdf(os.path.join(out_dir, args.set_name+'_SNR_data.h5'), key='Optimal_SNR')
print("Done!")

end_time = time.time()
print(f"Total time taken = {end_time-start_time} seconds.")
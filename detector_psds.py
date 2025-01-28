from pycbc import psd

pycbc_psds = psd.analytical.get_psd_model_list()

psds_from_files = {'ASharp':{'file':'./noise_curves/Asharp-asd.txt', #taken from https://dcc.ligo.org/LIGO-T2300041
                             'is_asd':True},
                   'CE20':{'file':'./noise_curves/CE20-asd.txt', #taken from https://dcc.cosmicexplorer.org/CE-T2000017-v8/public - cosmic_explorer_20km_strain.txt
                           'is_asd':True}, 
                   'CE40':{'file':'./noise_curves/CE40-asd.txt', 
                           'is_asd':True}} #taken from https://dcc.cosmicexplorer.org/CE-T2000017-v8/public - cosmic_explorer_strain.txt

def get_available_psds():
    return(pycbc_psds + list(psds_from_files.keys()))

def generate_psd(psd_name, length, delta_f, f_low):
    """
    Returns PSD data for a given psd_name

    Parameters:
    -------------
    psd_name: str
        PSD model name from the list available at `detector_psds.get_available_psds()`
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
    if psd_name in pycbc_psds:
        psd_data = eval('psd.analytical.'+psd_name)(length, delta_f, f_low)
    
    elif psd_name in psds_from_files.keys():
        psd_data = psd.from_txt(psds_from_files[psd_name]['file'], 
                                length, delta_f, f_low, 
                                is_asd_file=psds_from_files[psd_name]['is_asd'])

    else:
        raise ValueError(f"PSD model '{psd_name}' not found.")
    return(psd_data)
from pycbc import psd

pycbc_psds = psd.analytical.get_psd_model_list()

psds_from_files = {'ASharp':'./noise_curves/Asharp-asd.txt', 
                   'CE20': './noise_curves/CE20-asd.txt'}

def get_available_psds():
    return(pycbc_psds + list(psds_from_files.keys()))

def generate_psd(psd_name, length, delta_f, f_low):
    """
    Returns PSD data for a given psd_name

    Parameters:
    -------------
    psd_name: str
        PSD model name from `pycbc.psd.analytical.get_psd_model_list` or the dictionary above
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
        psd_data = psd.from_txt(psds_from_files[psd_name], length, delta_f, f_low, is_asd_file=True)

    else:
        raise ValueError(f"PSD model '{psd_name}' not found.")
    return(psd_data)
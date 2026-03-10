import pandas as pd
import numpy as np
import h5py

def get_detected_SNRs(data_dict, ifo_threshold=5, network_threshold=12, 
                      method='two-detector', 
                      snr_type='opt'):
    """
    Parameters
    -------------------------------------------
    data_dict : dictionary or pandas Dataframe
        data with keys SNR_i or SNR_mf_i or SNR_mf_from_opt_i where i stands for an IFO or network
    ifo_threshold : float (default = 5)
        SNR threshold for each IFO
    network_threshold : float (default = 12)
        SNR threshold for network
    method : str (default = 'two-detector')
        Method to apply SNR threshold. Choices:
            two-detector : Atleast two detectors meet the ifo_threshold and SNR_network is above network_threshold
            network : SNR_network meets the network_threshold
            all : All detectors meet ifo_threshold and SNR_network is above network_threshold
    snr_type : str (default = 'opt')
        SNR type to apply threshold on. Choices:
            opt : optimal SNR
            mf : matched-filter SNR
            mf_from_opt : matched-filter SNR derived from chi_sq distribution on optimal

    Returns
    -----------------------------------------
    Pandas dataframe containing detected events
    """
    if type(data_dict) == pd.core.frame.DataFrame:
        pass
    else:
        data_dict = pd.DataFrame(data_dict)
        
    if snr_type == 'opt':
        SNR_keys = [key for key in data_dict.keys() if 'SNR' in key and 'mf' not in key]
    elif snr_type == 'mf_from_opt':
        SNR_keys = [key for key in data_dict.keys() if 'SNR_mf_from_opt' in key]
    elif snr_type == 'mf_from_gaussian':
        SNR_keys = [key for key in data_dict.keys() if 'SNR_mf_from_gaussian' in key]
    elif snr_type == 'mf':
        SNR_keys = [key for key in data_dict.keys() if 'SNR_mf' in key and 'from_opt' not in key]
    else:
        raise KeyError('Please choose a valid snr_type')
    print(SNR_keys)
    detected_bool_dict = {}
    detected_dict = {}
    
    for key in SNR_keys:
        if snr_type == 'opt':
            dict_key = key.split('SNR_')[-1]
        elif snr_type == 'mf_from_opt':
            dict_key = key.split('SNR_mf_from_opt_')[-1]
        elif snr_type == 'mf_from_gaussian':
            dict_key = key.split('SNR_mf_from_gaussian_')[-1]
        elif snr_type == 'mf':
            dict_key = key.split('SNR_mf_')[-1]
        
        if "network" in key:
            threshold = network_threshold
        else:
            threshold = ifo_threshold

        detected_bool_dict[dict_key] = data_dict[key] >= threshold
        detected_dict[dict_key] = data_dict[detected_bool_dict[dict_key]]

    if method=='all':
        detected_events_df = data_dict[np.all(tuple(detected_bool_dict.values()), axis=0) & detected_bool_dict['network']]
    elif method == 'two-detector':
        detector_keys = [key for key in detected_bool_dict.keys() if key != 'network']
        detection_sum = np.sum([detected_bool_dict[key] for key in detector_keys], axis=0)
        detected_events_df = data_dict[(detection_sum >= 2) & (detected_bool_dict['network'])]
    elif method=='network':
        detected_events_df = detected_dict['network']

    return(detected_events_df)

def save_to_h5_group(group, data, string_dtype, key=None):
    # if key is given, create dataset/group under that name
    if isinstance(data, dict):
        subgroup = group if key is None else group.create_group(str(key))
        for k, v in data.items():
            save_to_h5_group(subgroup, v, string_dtype, k)

    elif isinstance(data, (list, tuple)):
        subgroup = group if key is None else group.create_group(str(key))
        for i, item in enumerate(data):
            save_to_h5_group(subgroup, item, string_dtype, str(i))

    elif isinstance(data, pd.DataFrame):
        subgroup = group if key is None else group.create_group(str(key))
        for col in data.columns:
            subgroup.create_dataset(str(col), data=data[col].to_numpy())

    elif isinstance(data, str):
        if key is None:
            raise ValueError("Strings must be stored with a key")
        group.create_dataset(str(key), data=data, dtype=string_dtype)

    else:
        if key is None:
            raise ValueError("Scalars/arrays must be stored with a key")
        group.create_dataset(str(key), data=np.array(data))


def save_results_to_h5(results, filename):
    dt = h5py.string_dtype(encoding='utf-8')
    with h5py.File(filename, 'w') as f:
        save_to_h5_group(f, results, dt)

def decode_data(data):
    """
    Decodes byte strings or arrays of byte strings from HDF5.
    """
    if isinstance(data, bytes):
        return data.decode('utf-8')
    elif isinstance(data, np.ndarray) and data.dtype.kind in {'S', 'O'}:
        return [d.decode('utf-8') if isinstance(d, bytes) else d for d in data]
    else:
        return data

def load_from_h5_group(group):
    """
    Recursively loads data from an HDF5 group and reconstructs Python objects.
    """
    result = {}

    # Check if this group is an array-style list (all keys are numeric)
    keys = list(group.keys())
    if all(k.isdigit() for k in keys):
        # Treat it as a list, sorted by numeric key
        items = []
        for key in sorted(keys, key=lambda x: int(x)):
            val = group[key]
            if isinstance(val, h5py.Group):
                items.append(load_from_h5_group(val))
            else:
                items.append(decode_data(val[()]))
        return items

    # Otherwise treat as dict
    for key in group:
        item = group[key]
        if isinstance(item, h5py.Group):
            result[key] = load_from_h5_group(item)
        else:
            result[key] = decode_data(item[()])

    return result

def load_results_from_h5(filename):
    """
    Loads structured data from a universally saved HDF5 file.
    """
    with h5py.File(filename, 'r') as f:
        return load_from_h5_group(f)
    
def transform_cov_DL_Mc_to_logDL_logMc(cov, DL, DL_index, Mc, Mc_index):
    """
    Transforms a covariance matrix where:
    - DL is replaced with log_DL using dlogDL/dDL = 1/DL
    - Mc is replaced with log_Mc using dlogMc/dMc = 1/Mc
    - Other parameters remain unchanged

    Parameters:
    -----------
    cov : np.ndarray
        Original NxN covariance matrix including DL and Mc.
    DL : float
        Mean value of DL (Mpc).
    DL_index : int
        Index of DL in the covariance matrix.
    Mc : float
        Mean value of chirp mass (solar masses).
    Mc_index : int
        Index of Mc in the covariance matrix.

    Returns:
    --------
    cov_new : np.ndarray
        Transformed covariance matrix with log_DL and log_Mc replacing DL and Mc.
    """

    # Derivatives for Jacobian
    dlogDL_dDL = 1.0 / DL
    dlogMc_dMc = 1.0 / Mc

    # Build Jacobian matrix
    N = cov.shape[0]
    J = np.eye(N)
    J[DL_index, DL_index] = dlogDL_dDL
    J[Mc_index, Mc_index] = dlogMc_dMc

    # Transform covariance matrix
    cov_new = J @ cov @ J.T

    return cov_new

def transform_cov_chi1_chi2_to_chieff_chianti(cov, q, chi1_index, chi2_index):
    """
    Transforms a covariance matrix where:
    - chi_1 and chi_2 are replaced with chi_eff and chi_anti
    - chi_eff  = (chi_1 + q * chi_2) / (1 + q)
    - chi_anti = (chi_1 - q * chi_2) / (1 + q)
    - Other parameters remain unchanged

    Parameters:
    -----------
    cov : np.ndarray
        Original NxN covariance matrix including chi_1 and chi_2.
    q : float
        Mass ratio.
    chi1_index : int
        Index of chi_1 in the covariance matrix.
    chi2_index : int
        Index of chi_2 in the covariance matrix.

    Returns:
    --------
    cov_new : np.ndarray
        Transformed covariance matrix with chi_eff and chi_anti
        replacing chi_1 and chi_2.
    """

    # Derivatives for Jacobian
    dchieff_dchi1  = 1.0 / (1.0 + q)
    dchieff_dchi2  = q   / (1.0 + q)
    dchianti_dchi1 = 1.0 / (1.0 + q)
    dchianti_dchi2 = -q  / (1.0 + q)

    # Build Jacobian matrix
    N = cov.shape[0]
    J = np.eye(N)

    # chi_eff row
    J[chi1_index, chi1_index] = dchieff_dchi1
    J[chi1_index, chi2_index] = dchieff_dchi2

    # chi_anti row
    J[chi2_index, chi1_index] = dchianti_dchi1
    J[chi2_index, chi2_index] = dchianti_dchi2

    # Transform covariance matrix
    cov_new = J @ cov @ J.T

    return cov_new

def slice_mtotal_pop(arr, mtotal_range):
    """
    Returns: A bool array corresponding to arr, depending on the range provided
    """
    if '<' in mtotal_range:
        max_boundary = float(mtotal_range.split('<')[-1])
        return(arr < max_boundary)
        
    elif '<=' in mtotal_range:
        max_boundary = float(mtotal_range.split('<=')[-1])
        return(arr <= max_boundary)
        
    elif '>' in mtotal_range:
        min_boundary = float(mtotal_range.split('>')[-1])
        return(arr > min_boundary)
        
    elif '>=' in mtotal_range:
        min_boundary = float(mtotal_range.split('>=')[-1])
        return(arr >= min_boundary)
        
    elif '-' in mtotal_range:
        min_boundary, max_boundary = map(float, mtotal_range.split('-'))
        return(np.all((arr >= min_boundary, arr <= max_boundary), axis=0))
    
def z_peak_new(gamma, kappa, z_peak):
    new_peak = (gamma/(kappa-gamma))**(1/kappa) * (1+z_peak) - 1
    return(new_peak)

def z_peak_new_from_dict(parameters):
    """
    parameters: dict
    
    Returns
    ------------------
    converted_parameters: dict
    """
    converted_parameters = parameters.copy()
    gamma = parameters['gamma']
    kappa = parameters['kappa']
    z_peak = parameters['z_peak']
    if isinstance(gamma, float):
        if gamma >= kappa:
            converted_parameters['z_peak_new'] = -1
    elif isinstance(gamma, np.ndarray) or isinstance(gamma, list):
        converted_parameters['z_peak_new'] = []
        for i in range(len(gamma)):
            gamma_i = gamma[i]
            kappa_i = kappa[i]
            z_peak_i = z_peak[i]
            if gamma_i >= kappa_i:
                converted_parameters['z_peak_new'].append(-1)
            else:
                converted_parameters['z_peak_new'].append((gamma_i/(kappa_i-gamma_i))**(1/kappa_i) * (1+z_peak_i) - 1)
        converted_parameters = {key:np.array(converted_parameters[key]) for key in converted_parameters.keys()}
    return converted_parameters
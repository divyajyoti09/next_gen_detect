from pycbc.detector import get_available_detectors, load_detector_config, get_available_lal_detectors

load_detector_config("detector_config.ini")
lal_detectors = dict(get_available_lal_detectors())
all_detectors = get_available_detectors()
extra_detectors_names = {'CE20':'Cosmic_Explorer_20km'}

def get_available_detectors_list():
    """
    Returns a list of all available detectors including those loaded from detector_config.ini file.
    """
    return all_detectors

def get_available_detectors_full_names():
    """
    Returns a dictionary of all available detectors with their full names from LAL or from custom name dictionary.
    If full name is not available, short name is returned for that key
    Format: dict(short_name : full_name)
    """
    det_full_names = {}
    for det in all_detectors:
        if det in lal_detectors.keys():
            det_full_names[det] = lal_detectors[det]
        elif det in extra_detectors_names.keys():
            det_full_names[det] = extra_detectors_names[det]
        else:
            det_full_names[det] = det
    return det_full_names
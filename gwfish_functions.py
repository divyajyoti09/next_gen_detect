from multiprocessing import Pool, cpu_count
from GWFish.modules.detection import Network
from GWFish.modules.fishermatrix import compute_network_errors
import GWFish.modules as gwf_mods
import pathlib
import numpy as np
import shutil
import os

def worker(args):
    """
    Worker function to compute network errors for a chunk of injections.
    Returns: (global_indices_chunk, detected_indices, snrs, parameter_errors, sky_locs)
    """
    (network, indices, parameter_values, fisher_params, f_ref,
     base_dir, postfix, chunk_idx, kwargs) = args

    det_idx, snrs, errs, sky = compute_network_errors(
        network=network,
        parameter_values=parameter_values,
        fisher_parameters=fisher_params,
        f_ref=f_ref,
        waveform_model='IMRPhenomXPHM',
        save_matrices=True,
        save_matrices_path=pathlib.Path(os.path.join(
            base_dir,
            'GWFish_analysis',
            'BBH',
            'Fisher_matrices'
        )),
        matrix_naming_postfix=f"{postfix}_chunk{chunk_idx}",
        **kwargs
    )

    return indices, det_idx, snrs, errs, sky


def parallel_compute_network_errors(
    network,
    gwfish_input_data,
    fisher_params,
    f_ref,
    base_dir,
    matrix_file_names,
    nproc=None,
    **kwargs
):
    """
    Parallel wrapper for compute_network_errors with multiprocessing.
    Returns: detected_idxs, netw_snrs, errors (2D), sky_locs
    """
    if nproc is None:
        nproc = min(cpu_count(), 8)

    N = len(gwfish_input_data)
    n_params = len(fisher_params)
    indices = np.arange(N)

    # Split data and indices into chunks
    chunks_idx = np.array_split(indices, nproc)
    chunks_data = np.array_split(gwfish_input_data, nproc)

    args = [
        (network, idx_chunk, data_chunk, fisher_params,
         f_ref, base_dir, matrix_file_names, i, kwargs)
        for i, (idx_chunk, data_chunk) in enumerate(zip(chunks_idx, chunks_data))
    ]

    # Run in parallel
    with Pool(processes=nproc) as pool:
        results = pool.map(worker, args)

    # Allocate arrays
    detected_idxs = []
    netw_snrs = np.zeros(N)
    errors = np.zeros((N, n_params))      # 2D array
    sky_locs = np.zeros(N)  # 1D array of areas

    # Stitch results back in original order
    for idx_chunk, det_idx, snrs, errs, sky in results:
        detected_idxs.extend(idx_chunk[det_idx])
        netw_snrs[idx_chunk] = snrs
        errors[idx_chunk] = errs       # 2D assignment
        sky_locs[idx_chunk] = sky      # 1D assignment


    return np.array(detected_idxs), netw_snrs, errors, sky_locs

def combine_and_archive_fisher_matrices(base_dir, matrix_file_prefix, n_chunks, output_file):
    """
    Combines chunked Fisher matrix npy files into a single npy file
    and moves the individual chunk files to a 'chunks' subdirectory.

    Parameters
    ----------
    base_dir : str or Path
        Base folder where the chunked matrices are saved
    matrix_file_prefix : str
        Prefix used in matrix_naming_postfix (without _chunkX)
    n_chunks : int
        Number of chunks used in parallel processing
    output_file : str or Path
        Path to save the combined Fisher matrices
    """
    base_dir = pathlib.Path(base_dir)
    chunks_dir = base_dir / 'chunks'
    chunks_dir.mkdir(exist_ok=True)

    matrices = []

    for i in range(n_chunks):
        file_path = base_dir / f"{matrix_file_prefix}_chunk{i}.npy"
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} not found")
        matrices.append(np.load(file_path))

    # Combine along first axis (injection axis)
    combined = np.vstack(matrices)
    np.save(output_file, combined)
    print(f"Combined Fisher matrices saved to {output_file}")

    # Move chunked files to chunks directory
    for i in range(n_chunks):
        file_path = base_dir / f"{matrix_file_prefix}_chunk{i}.npy"
        shutil.move(str(file_path), chunks_dir / file_path.name)
    print(f"Moved {n_chunks} chunked Fisher matrix files to {chunks_dir}")
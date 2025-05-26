import numpy as np
import scipy as sp
import json
from collections import Counter
import math
from scipy.stats import chi2
import os

def convert_primes_to_binary_without_last_bit(filepath):
    """
    Lee primos desde un archivo (uno por línea),
    los convierte a binario de ancho fijo w = ceil(L * log2(10)),
    elimina el LSB (último bit), y concatena todos los resultados en un único bitstream.
    """
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip().isdigit()]

    if not lines:
        return ""

    L = len(lines[0])  # número de cifras decimales del primer primo
    w = math.ceil(L * math.log2(10))  # ancho fijo recomendado por NIST

    stream = []
    for p in lines:
        b = format(int(p), f'0{w}b')  # binario de longitud fija
        stream.append(b[:-1])         # eliminar el LSB

    return ''.join(stream)

def aproximate_entropy_params(primes_sample):
    return 0
def bin_matrix_params(primes_sample):
    return 0
def cumsums_params(primes_sample):
    return 0
def excursion_params(primes_sample):
    return 0
def excursions_variant_params(primes_sample):
    return 0



def frequency_params(filepath, json_path="monobit_calibration_P5.json", block_sizes=[50, 100, 200, 400]):
    binaries = convert_primes_to_binary_without_last_bit(filepath)
    bitstream = [int(bit) for b in binaries for bit in b]
    n_bits = len(bitstream)

    results = {}

    for B in block_sizes:
        N = n_bits // B
        if N < 100:
            continue

        chisq = 0
        for j in range(N):
            block = bitstream[j*B : (j+1)*B]
            pi_j = sum(block) / B
            chisq += (pi_j - 0.5)**2

        chisq_stat = 4 * B * chisq
        p_value = chi2.sf(chisq_stat, df=N)

        results[str(B)] = {
            "N_blocks": int(N),
            "chi2_stat": float(chisq_stat),
            "p_value": float(p_value)
        }

    # Guardar resultados en JSON
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            try:
                calib = json.load(f)
            except json.JSONDecodeError:
                calib = {}
    else:
        calib = {}

    calib["BlockFrequencyTest"] = {
        "total_bits": n_bits,
        "block_results": results,
        "block_sizes_tested": list(results.keys())  # sólo informativo
    }

    with open(json_path, "w") as f:
        json.dump(calib, f, indent=4)

    return calib["BlockFrequencyTest"]

def linear_complexity_params(primes_sample):
    return 0
def longest_run_params(primes_sample):
    return 0
def maurer_params(primes_sample):
    return 0

import json
from collections import Counter

def monobit_params(primes_sample, output_file="monobit_calibration.json"):
    """
    Calibrates digit distributions from a reference sample of primes.
    Returns position-wise distributions and saves to JSON.
    """
    count_first = Counter()
    count_mid = Counter()
    count_last = Counter()
    total_first = total_mid = total_last = 0

    for p in primes_sample:
        p_str = str(p).strip()
        if not p_str.isdigit() or len(p_str) < 3:
            continue

        first_digit = int(p_str[0])
        last_digit = int(p_str[-1])
        mid_digits = [int(ch) for ch in p_str[1:-1]]

        count_first[first_digit] += 1
        count_last[last_digit] += 1
        total_first += 1
        total_last += 1

        for d in mid_digits:
            count_mid[d] += 1
            total_mid += 1

    # Convert to probability distributions
    P_first = {str(d): count_first[d] / total_first for d in range(10)}
    P_mid = {str(d): count_mid[d] / total_mid for d in range(10)}
    P_last = {str(d): count_last[d] / total_last for d in range(10)}

    calibration = {
        "P_first": P_first,
        "P_mid": P_mid,
        "P_last": P_last
    }

    with open(output_file, "w") as f:
        json.dump(calibration, f, indent=4)

    return calibration


def non_overlap_matching_params(primes_sample):
    return 0
def overlap_matching_params(primes_sample):
    return 0
def runs_params(primes_sample):
    return 0
def serial_params(primes_sample):
    return 0
def spectral_fft_params(primes_sample):
    return 0


import numpy as np
import scipy as sp


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
def frequency_params(primes_sample):
    return 0
def linear_complexity_params(primes_sample):
    return 0
def longest_run_params(primes_sample):
    return 0
def maurer_params(primes_sample):
    return 0
from collections import Counter
import numpy as np

def monobit_params(primes_sample):
    """
    Calcula los parámetros del Monobit Test (sin Benford):
    - Primer dígito + intermedios → distribución uniforme.
    - Último dígito → Dirichlet (dígitos 1,3,7,9).
    Devuelve un diccionario JSON con estadísticas clave.
    """

    # === Modelos teóricos internos ===
    def p_mid(d):
        return 0.1

    def p_last(d):
        return 0.25 if d in {1, 3, 7, 9} else 0

    # === Conteo observado ===
    observed_counts = Counter()
    for p in primes_sample:
        digits = list(map(int, p))
        for d in digits[0:4]:                # primer + intermedios
            observed_counts[d] += 1
        observed_counts[digits[4]] += 1      # último dígito

    # === Conteo esperado ===
    N = len(primes_sample)
    expected_counts = {}
    for d in range(10):
        expected_counts[d] = (
            N * 4 * p_mid(d) +
            N * p_last(d)
        )

    # === Estadístico chi² ===
    chi2 = 0
    for d in range(10):
        E = expected_counts[d]
        O = observed_counts[d]
        if E > 0:
            chi2 += (O - E) ** 2 / E

    return {
        "test_name": "Monobit Test (Uniform + Dirichlet)",
        "num_primes": N,
        "total_digits": N * 5,
        "observed_counts": dict(observed_counts),
        "expected_counts": {str(k): round(v, 2) for k, v in expected_counts.items()},
        "chi_squared_stat": round(chi2, 4),
        "note": "Model assumes uniform distribution for first 4 digits and Dirichlet for last digit."
    }

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


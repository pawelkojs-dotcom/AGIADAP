#!/usr/bin/env python3
"""
test_R4_regression_v1_1.py — REG-R4-002 runner (TRL-4 embedding kernel)

Ten skrypt porównuje przebieg kandydata z embeddingowym baseline'em TRL-4
(AGI-BASELINE-002) zgodnie z zasadami opisanymi w REG-R4-002_PROCEDURE.md.

Wyjścia:
- kod 0  – PASS (wszystkie warunki spełnione),
- kod 1  – FAIL (któryś z warunków odrzucony),
- kod 2  – ERROR (błąd techniczny: brak pliku, zły format itp.).

Zakładana struktura JSON (pojedynczy przebieg):
{
  "n_eff":      [float, ...],
  "I_ratio":    [float, ...],
  "d_sem":      [float, ...],
  "sigma_coh":  [float, ...],
  "phase":      [str,   ...],   # np. "R2_EXPLORATORY", "R4_REFLECTIVE"
  "norms":      [[float, ...],  # krok 0: normy agentów
                 [float, ...],  # krok 1: normy agentów
                 ...
                ]
}

Progi i tolerancje są zgodne z R4_BASELINE_SPEC_v1_1 (wersja v1.1).

Użycie:
    python3 test_R4_regression_v1_1.py \
        BASELINE_JSON \
        CANDIDATE_JSON \
        [--verbose]
"""

import sys
import json
import argparse
from typing import Any, Dict, Tuple, List

import numpy as np


# ---------------------------------------------------------------------------
# Stałe progowe (odpowiadające R4_BASELINE_SPEC_v1_1)
# ---------------------------------------------------------------------------

# Faza docelowa
REQUIRED_FINAL_PHASE = "R4_REFLECTIVE"

# Progi twarde dla wartości końcowych
MIN_N_EFF_FINAL = 4.0       # efektywna liczba warstw
MIN_I_RATIO_FINAL = 0.30    # udział informacji pośredniej
MIN_D_SEM_FINAL = 20.0      # wymiarowość semantyczna
MIN_SIGMA_FINAL = 0.70      # koherencja końcowa

MIN_SIGMA_TRAJ = 0.0        # sigma_coh nie może spaść poniżej 0.0

# Zakres norm embeddingów (bezpieczny dla stabilności numerycznej)
MIN_NORM = 0.1
MAX_NORM = 20.0

# Tolerancje „miękkie" względem baseline'u (końcowe wartości)
DEFAULT_SIGMA_TOL = 0.10   # |σ_coh_final^cand - σ_coh_final^base|
DEFAULT_I_TOL = 0.15       # |I_ratio_final^cand - I_ratio_final^base|
DEFAULT_DSEM_FRAC_TOL = 0.25  # względne odchylenie d_sem_final


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def load_metrics(path: str) -> Dict[str, Any]:
    """Wczytuje plik JSON z metrykami (pojedynczy przebieg)."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def flatten_norms(norms_series: List[List[float]]) -> np.ndarray:
    """
    norms_series – lista kroków; każdy krok to lista norm agentów.
    Zwraca spłaszczoną tablicę wszystkich norm ze wszystkich kroków.
    """
    flat: List[float] = []
    for step_norms in norms_series:
        flat.extend(step_norms)
    return np.array(flat, dtype=float) if flat else np.array([], dtype=float)


def ensure_equal_lengths(candidate: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Sprawdza, czy serie czasowe metryk mają tę samą długość.
    Nie jest to wymóg formalny R4, ale chroni przed cichymi błędami.
    """
    keys = ["n_eff", "I_ratio", "d_sem", "sigma_coh", "phase"]
    lengths = {}
    for k in keys:
        if k not in candidate:
            return False, f"Brak klucza '{k}' w JSON kandydata."
        lengths[k] = len(candidate[k])

    unique_lens = set(lengths.values())
    if len(unique_lens) != 1:
        detail = ", ".join(f"{k}={v}" for k, v in lengths.items())
        return False, f"Niespójne długości szeregów czasowych: {detail}"

    if next(iter(unique_lens)) == 0:
        return False, "Puste serie czasowe (0 kroków) w JSON kandydata."

    return True, "Długości szeregów czasowych są spójne."


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_hard_conditions(candidate: Dict[str, Any], verbose: bool = False) -> Tuple[bool, str]:
    """
    Sprawdza warunki twarde REG-R4-002 dla przebiegu kandydata.

    Zakłada strukturę JSON:
      - "phase": [str, ...],
      - "n_eff", "I_ratio", "d_sem", "sigma_coh": listy float,
      - "norms": lista list floatów.
    """
    ok_len, msg_len = ensure_equal_lengths(candidate)
    if not ok_len:
        return False, msg_len

    try:
        phases = candidate["phase"]
        n_eff_arr = np.asarray(candidate["n_eff"], dtype=float)
        I_arr = np.asarray(candidate["I_ratio"], dtype=float)
        d_sem_arr = np.asarray(candidate["d_sem"], dtype=float)
        sigma_arr = np.asarray(candidate["sigma_coh"], dtype=float)
        norms_arr = flatten_norms(candidate.get("norms", []))
    except KeyError as e:
        return False, f"Brak klucza w JSON kandydata: {e}"
    except Exception as e:
        return False, f"Błąd przy odczycie metryk kandydata: {e}"

    # Faza końcowa
    phase_final = phases[-1]
    if phase_final != REQUIRED_FINAL_PHASE:
        return False, (
            f"FAIL: phase_final = {phase_final}, "
            f"oczekiwano {REQUIRED_FINAL_PHASE}"
        )

    n_eff_final = float(n_eff_arr[-1])
    I_final = float(I_arr[-1])
    d_sem_final = float(d_sem_arr[-1])
    sigma_final = float(sigma_arr[-1])

    if verbose:
        print("  [DEBUG] Final candidate metrics:")
        print(f"    n_eff_final   = {n_eff_final:.3f}")
        print(f"    I_ratio_final = {I_final:.3f}")
        print(f"    d_sem_final   = {d_sem_final:.3f}")
        print(f"    sigma_final   = {sigma_final:.3f}")

    # Progi twarde
    if n_eff_final < MIN_N_EFF_FINAL:
        return False, f"FAIL: n_eff_final = {n_eff_final:.3f} < {MIN_N_EFF_FINAL:.3f}"
    if I_final < MIN_I_RATIO_FINAL:
        return False, f"FAIL: I_ratio_final = {I_final:.3f} < {MIN_I_RATIO_FINAL:.3f}"
    if d_sem_final < MIN_D_SEM_FINAL:
        return False, f"FAIL: d_sem_final = {d_sem_final:.3f} < {MIN_D_SEM_FINAL:.3f}"
    if sigma_final < MIN_SIGMA_FINAL:
        return False, f"FAIL: sigma_coh_final = {sigma_final:.3f} < {MIN_SIGMA_FINAL:.3f}"

    # Trajektoria sigma_coh nie może „przechodzić" poniżej 0
    if np.min(sigma_arr) < MIN_SIGMA_TRAJ:
        return False, (
            "FAIL: w trajektorii występują wartości sigma_coh "
            f"< {MIN_SIGMA_TRAJ:.3f}"
        )

    # Normy embeddingów – sanity check stabilności numerycznej
    if norms_arr.size > 0:
        min_norm = float(np.min(norms_arr))
        max_norm = float(np.max(norms_arr))
        if min_norm < MIN_NORM:
            return False, (
                "FAIL: minimalna norma embeddingu "
                f"= {min_norm:.3f} < {MIN_NORM:.3f}"
            )
        if max_norm > MAX_NORM:
            return False, (
                "FAIL: maksymalna norma embeddingu "
                f"= {max_norm:.3f} > {MAX_NORM:.3f}"
            )

        if verbose:
            print("  [DEBUG] Embedding norms:")
            print(f"    min_norm = {min_norm:.3f}")
            print(f"    max_norm = {max_norm:.3f}")

    return True, "Hard conditions OK."


def check_soft_conditions(
    baseline: Dict[str, Any],
    candidate: Dict[str, Any],
    sigma_tol: float = DEFAULT_SIGMA_TOL,
    I_tol: float = DEFAULT_I_TOL,
    dsem_frac_tol: float = DEFAULT_DSEM_FRAC_TOL,
    verbose: bool = False,
) -> Tuple[bool, str]:
    """
    Sprawdza odchylenia końcowych metryk względem baseline'u.

    sigma_tol      – tolerancja absolutna dla sigma_coh_final,
    I_tol          – tolerancja absolutna dla I_ratio_final,
    dsem_frac_tol  – tolerancja względna dla d_sem_final
                     (|Δd_sem| / d_sem_baseline).
    """

    try:
        b_sigma = float(baseline["sigma_coh"][-1])
        b_I = float(baseline["I_ratio"][-1])
        b_dsem = float(baseline["d_sem"][-1])

        c_sigma = float(candidate["sigma_coh"][-1])
        c_I = float(candidate["I_ratio"][-1])
        c_dsem = float(candidate["d_sem"][-1])
    except Exception as e:
        return False, f"FAIL: problem z odczytem końcowych metryk (baseline/kandydat): {e}"

    d_sigma = abs(c_sigma - b_sigma)
    d_I = abs(c_I - b_I)
    d_dsem = abs(c_dsem - b_dsem)
    d_dsem_frac = d_dsem / (abs(b_dsem) + 1e-8)

    if verbose:
        print("  [DEBUG] Final baseline vs candidate:")
        print(f"    sigma_coh: cand={c_sigma:.3f}, base={b_sigma:.3f}, |Δ|={d_sigma:.3f}")
        print(f"    I_ratio  : cand={c_I:.3f}, base={b_I:.3f}, |Δ|={d_I:.3f}")
        print(f"    d_sem    : cand={c_dsem:.3f}, base={b_dsem:.3f}, "
              f"|Δ|={d_dsem:.3f}, frac={d_dsem_frac:.3f}")

    if d_sigma > sigma_tol:
        return False, (
            f"FAIL: |sigma_coh_final(candidate) - baseline| = {d_sigma:.3f} "
            f"> {sigma_tol:.3f}"
        )

    if d_I > I_tol:
        return False, (
            f"FAIL: |I_ratio_final(candidate) - baseline| = {d_I:.3f} "
            f"> {I_tol:.3f}"
        )

    if d_dsem_frac > dsem_frac_tol:
        return False, (
            "FAIL: |d_sem_final(candidate) - baseline|/baseline = "
            f"{d_dsem_frac:.3f} > {dsem_frac_tol:.3f}"
        )

    return True, "Soft conditions OK."


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="REG-R4-002 regression test (TRL-4 embedding kernel)"
    )
    parser.add_argument(
        "baseline_json",
        help="Ścieżka do pliku JSON z baseline_TRL4_embedding.json",
    )
    parser.add_argument(
        "candidate_json",
        help="Ścieżka do pliku JSON z przebiegiem kandydata",
    )
    parser.add_argument(
        "--sigma-tol",
        type=float,
        default=DEFAULT_SIGMA_TOL,
        help=f"Tolerancja dla sigma_coh_final (domyślnie {DEFAULT_SIGMA_TOL})",
    )
    parser.add_argument(
        "--I-tol",
        type=float,
        default=DEFAULT_I_TOL,
        help=f"Tolerancja dla I_ratio_final (domyślnie {DEFAULT_I_TOL})",
    )
    parser.add_argument(
        "--dsem-frac-tol",
        type=float,
        default=DEFAULT_DSEM_FRAC_TOL,
        help=(
            "Względna tolerancja dla d_sem_final względem baseline'u "
            f"(domyślnie {DEFAULT_DSEM_FRAC_TOL})"
        ),
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Wypisz dodatkowe informacje diagnostyczne",
    )
    return parser.parse_args(argv[1:])


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    try:
        baseline = load_metrics(args.baseline_json)
        candidate = load_metrics(args.candidate_json)
    except FileNotFoundError as e:
        print(f"[ERROR] Nie udało się wczytać plików: {e}")
        return 2
    except Exception as e:
        print(f"[ERROR] Błąd podczas wczytywania JSON: {e}")
        return 2

    print("=== REG-R4-002: Regression-to-Baseline R4 (TRL-4 Embedding) ===")
    print(f"Baseline : {args.baseline_json}")
    print(f"Candidate: {args.candidate_json}")
    print("")

    # 1. Hard conditions
    ok_hard, msg_hard = check_hard_conditions(candidate, verbose=args.verbose)
    print(f"[Hard conditions] {msg_hard}")
    if not ok_hard:
        print("=== RESULT: FAIL (hard conditions) ===")
        return 1

    # 2. Soft deviations vs baseline
    ok_soft, msg_soft = check_soft_conditions(
        baseline,
        candidate,
        sigma_tol=args.sigma_tol,
        I_tol=args.I_tol,
        dsem_frac_tol=args.dsem_frac_tol,
        verbose=args.verbose,
    )
    print(f"[Soft deviations] {msg_soft}")
    if not ok_soft:
        print("=== RESULT: FAIL (soft conditions) ===")
        return 1

    # TODO: 3. Opcjonalnie – uruchomić mini-sweep (γ, Θ) w tym skrypcie,
    # zamiast robić to wyłącznie w wrapperze run_R4_002.sh.
    # Na razie zakładamy, że sweep jest obsługiwany na poziomie CI.

    print("=== RESULT: PASS (REG-R4-002 hard+soft conditions satisfied) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

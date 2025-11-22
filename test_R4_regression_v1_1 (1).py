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
MIN_N_EFF_FINAL = 4.5       # efektywna liczba warstw
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


def validate_json_schema(data: Dict[str, Any], data_type: str = "candidate") -> Tuple[bool, str]:
    """
    Sprawdza czy JSON ma wymaganą strukturę dla REG-R4-002.
    
    Args:
        data: Wczytane dane JSON
        data_type: "baseline" lub "candidate" (dla lepszych komunikatów)
    
    Returns:
        (is_valid, error_message)
    """
    required_keys = ["n_eff", "I_ratio", "d_sem", "sigma_coh", "phase"]
    
    # Sprawdź obecność kluczy
    for key in required_keys:
        if key not in data:
            return False, f"[{data_type}] Missing required key: '{key}'"
    
    # Sprawdź typy i długości
    for key in required_keys:
        if not isinstance(data[key], list):
            return False, (
                f"[{data_type}] Key '{key}' must be a list, "
                f"got {type(data[key]).__name__}"
            )
        
        if len(data[key]) == 0:
            return False, f"[{data_type}] Key '{key}' is empty (0 timesteps)"
    
    # Sprawdź strukturę norms (opcjonalna, ale jeśli istnieje musi być poprawna)
    if "norms" in data:
        if not isinstance(data["norms"], list):
            return False, (
                f"[{data_type}] Key 'norms' must be a list of lists, "
                f"got {type(data['norms']).__name__}"
            )
        
        if len(data["norms"]) > 0:
            for i, step_norms in enumerate(data["norms"]):
                if not isinstance(step_norms, list):
                    return False, (
                        f"[{data_type}] norms[{i}] must be a list, "
                        f"got {type(step_norms).__name__}"
                    )
                
                # Sprawdź czy są to liczby
                try:
                    _ = [float(x) for x in step_norms]
                except (ValueError, TypeError) as e:
                    return False, (
                        f"[{data_type}] norms[{i}] contains non-numeric values: {e}"
                    )
    
    # Sprawdź czy phase zawiera stringi
    try:
        phases = data["phase"]
        if not all(isinstance(p, str) for p in phases):
            return False, f"[{data_type}] 'phase' must contain strings"
    except Exception as e:
        return False, f"[{data_type}] Error validating 'phase': {e}"
    
    # Sprawdź czy metryki numeryczne są numeryczne
    for key in ["n_eff", "I_ratio", "d_sem", "sigma_coh"]:
        try:
            _ = np.asarray(data[key], dtype=float)
        except (ValueError, TypeError) as e:
            return False, (
                f"[{data_type}] Key '{key}' contains non-numeric values: {e}"
            )
    
    return True, f"[{data_type}] Schema valid"


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


def print_box(title: str, width: int = 70):
    """Drukuje ładny box header."""
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_metric_line(label: str, value: float, threshold: float, 
                      status: str = "", width: int = 70):
    """Drukuje linię metryki z wyrównaniem."""
    status_str = f"  [{status}]" if status else ""
    print(f"  {label:15s} = {value:7.3f}  (threshold: ≥ {threshold:.3f}){status_str}")


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
        print_box("CANDIDATE METRICS (final timestep)")
        print_metric_line("n_eff", n_eff_final, MIN_N_EFF_FINAL)
        print_metric_line("I_ratio", I_final, MIN_I_RATIO_FINAL)
        print_metric_line("d_sem", d_sem_final, MIN_D_SEM_FINAL)
        print_metric_line("sigma_coh", sigma_final, MIN_SIGMA_FINAL)
        print(f"  {'phase':15s} = {phase_final}")

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
            print("\n  Embedding norms (stability check):")
            print(f"    min = {min_norm:.3f}  (threshold: ≥ {MIN_NORM:.3f})")
            print(f"    max = {max_norm:.3f}  (threshold: ≤ {MAX_NORM:.3f})")

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
        print_box("BASELINE vs CANDIDATE COMPARISON (final timestep)")
        print(f"  {'Metric':<15s}  {'Candidate':>10s}  {'Baseline':>10s}  {'|Delta|':>10s}  {'Status':>10s}")
        print(f"  {'-'*15}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*10}")
        
        # sigma_coh
        status = "PASS" if d_sigma <= sigma_tol else "FAIL"
        print(f"  {'sigma_coh':<15s}  {c_sigma:>10.3f}  {b_sigma:>10.3f}  "
              f"{d_sigma:>10.3f}  {status:>10s}  (tol: {sigma_tol:.3f})")
        
        # I_ratio
        status = "PASS" if d_I <= I_tol else "FAIL"
        print(f"  {'I_ratio':<15s}  {c_I:>10.3f}  {b_I:>10.3f}  "
              f"{d_I:>10.3f}  {status:>10s}  (tol: {I_tol:.3f})")
        
        # d_sem
        status = "PASS" if d_dsem_frac <= dsem_frac_tol else "FAIL"
        print(f"  {'d_sem':<15s}  {c_dsem:>10.3f}  {b_dsem:>10.3f}  "
              f"{d_dsem:>10.3f}  {status:>10s}  (frac: {d_dsem_frac:.3f}, tol: {dsem_frac_tol:.3f})")

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
        description="REG-R4-002 regression test (TRL-4 embedding kernel)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python3 test_R4_regression_v1_1.py baseline.json candidate.json
  
  # With verbose output
  python3 test_R4_regression_v1_1.py baseline.json candidate.json --verbose
  
  # Custom tolerances
  python3 test_R4_regression_v1_1.py baseline.json candidate.json \\
      --sigma-tol 0.05 --I-tol 0.10 --dsem-frac-tol 0.20
        """
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

    print_box("REG-R4-002: Regression-to-Baseline R4 (TRL-4 Embedding)", width=70)
    print(f"  Baseline : {args.baseline_json}")
    print(f"  Candidate: {args.candidate_json}")

    # Load files
    try:
        baseline = load_metrics(args.baseline_json)
        candidate = load_metrics(args.candidate_json)
    except FileNotFoundError as e:
        print(f"\n[ERROR] Nie udało się wczytać plików: {e}")
        return 2
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Błąd parsowania JSON: {e}")
        return 2
    except Exception as e:
        print(f"\n[ERROR] Błąd podczas wczytywania JSON: {e}")
        return 2

    # Validate JSON schema
    ok_baseline, msg_baseline = validate_json_schema(baseline, "baseline")
    if not ok_baseline:
        print(f"\n[ERROR] {msg_baseline}")
        return 2
    
    ok_candidate, msg_candidate = validate_json_schema(candidate, "candidate")
    if not ok_candidate:
        print(f"\n[ERROR] {msg_candidate}")
        return 2
    
    if args.verbose:
        print(f"\n  ✓ {msg_baseline}")
        print(f"  ✓ {msg_candidate}")

    # 1. Hard conditions
    ok_hard, msg_hard = check_hard_conditions(candidate, verbose=args.verbose)
    
    print_box("TEST RESULTS", width=70)
    print(f"\n[Hard conditions] {msg_hard}")
    
    if not ok_hard:
        print_box("RESULT: FAIL (hard conditions)", width=70)
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
    print(f"\n[Soft deviations] {msg_soft}")
    
    if not ok_soft:
        print_box("RESULT: FAIL (soft conditions)", width=70)
        return 1

    # Success!
    print_box("RESULT: ✓ PASS (REG-R4-002 satisfied)", width=70)
    print("\nAll hard and soft conditions satisfied.")
    print("Candidate is compatible with AGI-BASELINE-002.\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

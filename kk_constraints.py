
# kk_constraints.py (clean build)
# Gap 1: KK Constraints as a Hard Condition
# Implements:
#  - HilbertTransform with methods: 'kernel', 'fft', 'odd_fft', 'pv_quad'
#  - KramersKronigRelations (forward/backward/check)
#  - KKProjector (projection onto H_KK)
#  - ConstrainedOptimizer (minimize F = E - Theta*S with KK constraint)

from __future__ import annotations
import numpy as np
import warnings
from dataclasses import dataclass

class HilbertTransform:
    """
    Discrete Hilbert transform operators suitable for KK relations on omega>0.
    """

    def __init__(self, omega: np.ndarray, method: str = 'kernel'):
        if not np.all(omega > 0):
            raise ValueError("Omega must be strictly positive.")
        if not np.all(np.diff(omega) > 0):
            raise ValueError("Omega grid must be strictly increasing.")
        self.omega = np.asarray(omega, dtype=float)
        self.n = len(self.omega)
        self.method = method

        if method == 'kernel':
            self.H_matrix = self._build_kernel_matrix()
        elif method == 'fft':
            self._fft_len = None  # lazy
        elif method == 'odd_fft':
            self._odd_fft_prepare()
        elif method == 'pv_quad':
            self.H_matrix = self._build_kernel_matrix_pv()
        else:
            raise ValueError("method must be 'kernel' or 'fft' or 'odd_fft' or 'pv_quad'")

    def _build_kernel_matrix(self) -> np.ndarray:
        # Basic kernel (no explicit weights) - kept for backward compatibility
        w = self.omega
        n = self.n
        H = np.zeros((n, n), dtype=float)
        for i in range(n):
            for j in range(n):
                if i == j:
                    H[i, j] = 0.0
                else:
                    denom = (w[j]**2 - w[i]**2)
                    if abs(denom) > 1e-12:
                        H[i, j] = (2.0/np.pi) * w[j] / denom
                    else:
                        # fallback finite-difference
                        dw = (w[j] - w[i])
                        H[i, j] = (1.0/dw) if dw != 0 else 0.0
        return H

    def _build_kernel_matrix_pv(self) -> np.ndarray:
        # PV quadrature with trapezoid weights and exclusion of nearest neighbors
        w = self.omega
        n = self.n
        H = np.zeros((n, n), dtype=float)
        dw = np.zeros(n, dtype=float)
        dw[1:-1] = 0.5*(w[2:] - w[:-2])
        dw[0] = w[1]-w[0]
        dw[-1] = w[-1]-w[-2]
        for i in range(n):
            for j in range(n):
                if i == j:
                    H[i, j] = 0.0
                else:
                    denom = (w[j]**2 - w[i]**2)
                    H[i, j] = (2.0/np.pi) * w[j] / denom * dw[j]
        # local PV exclusion (nearest neighbors)
        for i in range(n):
            if i-1 >= 0:
                H[i, i-1] = 0.0
            if i+1 < n:
                H[i, i+1] = 0.0
        return H

    def _odd_fft_prepare(self):
        w = self.omega
        # symmetric grid [-w_max,...,-w_min, w_min,...,w_max]
        w_neg = -w[::-1]
        self._w_sym = np.concatenate([w_neg, w])
        n_sym = len(self._w_sym)
        # taper to reduce edge effects
        k = max(8, n_sym//50)
        win = np.hanning(2*k)
        taper = np.ones(n_sym)
        taper[:k] = win[:k]
        taper[-k:] = win[-k:]
        self._taper = taper
        # next power of two for FFT length
        N = 1
        while N < n_sym:
            N <<= 1
        self._N_fft = N

    def _transform_fft(self, f: np.ndarray) -> np.ndarray:
        f = np.asarray(f, dtype=float)
        n = self.n
        # zero-pad to 2n
        N = 1
        while N < 2*n:
            N <<= 1
        f_ext = np.zeros(N, dtype=float)
        f_ext[:n] = f
        F = np.fft.fft(f_ext)
        freqs = np.fft.fftfreq(N)
        Fh = -1j*np.sign(freqs)*F
        fh = np.fft.ifft(Fh).real[:n]
        return fh

    def _transform_odd_fft(self, f: np.ndarray) -> np.ndarray:
        f = np.asarray(f, dtype=float)
        # odd extension
        f_sym = np.concatenate([-f[::-1], f])
        f_sym = f_sym * self._taper
        F = np.fft.fft(f_sym, n=self._N_fft)
        freqs = np.fft.fftfreq(self._N_fft)
        Fh = -1j*np.sign(freqs)*F
        fh_sym = np.fft.ifft(Fh).real
        fh_sym = fh_sym[:len(f_sym)]
        # extract positive half
        return fh_sym[len(f_sym)//2:]

    def transform(self, f: np.ndarray) -> np.ndarray:
        if len(f) != self.n:
            raise ValueError("Input length mismatch with omega grid.")
        if self.method == 'kernel':
            return self.H_matrix @ f
        elif self.method == 'fft':
            return self._transform_fft(f)
        elif self.method == 'odd_fft':
            return self._transform_odd_fft(f)
        elif self.method == 'pv_quad':
            return self.H_matrix @ f
        else:
            raise RuntimeError("Unknown method")

class KramersKronigRelations:
    """
    KK relations:
      sigma2(omega) = - omega * H[ sigma1/omega ]
      sigma1(omega) =   omega * H[ sigma2/omega ]
    """

    def __init__(self, omega: np.ndarray, method: str = 'odd_fft'):
        self.omega = np.asarray(omega, dtype=float)
        self.H = HilbertTransform(self.omega, method=method)

    def forward(self, sigma1: np.ndarray) -> np.ndarray:
        w = self.omega
        wsafe = np.where(w > 1e-12, w, 1e-12)
        g = np.asarray(sigma1, dtype=float) / wsafe
        Hg = self.H.transform(g)
        return -w * Hg

    def backward(self, sigma2: np.ndarray) -> np.ndarray:
        w = self.omega
        wsafe = np.where(w > 1e-12, w, 1e-12)
        g = np.asarray(sigma2, dtype=float) / wsafe
        Hg = self.H.transform(g)
        return w * Hg

    def check_consistency(self, sigma1: np.ndarray, sigma2: np.ndarray, tol: float = 0.1):
        s2_from_s1 = self.forward(sigma1)
        s1_from_s2 = self.backward(sigma2)
        e_fwd = np.linalg.norm(sigma2 - s2_from_s1) / (np.linalg.norm(sigma2) + 1e-16)
        e_bwd = np.linalg.norm(sigma1 - s1_from_s2) / (np.linalg.norm(sigma1) + 1e-16)
        return {
            'consistent': bool((e_fwd < tol) and (e_bwd < tol)),
            'error_forward': float(e_fwd),
            'error_backward': float(e_bwd)
        }

class KKProjector:
    """
    Projection onto H_KK via fixed-point averaging with normalization and positivity.
    """

    def __init__(self, omega: np.ndarray, method: str = 'odd_fft'):
        self.omega = np.asarray(omega, dtype=float)
        self.kk = KramersKronigRelations(self.omega, method=method)

    def _normalize(self, x: np.ndarray) -> np.ndarray:
        x = np.maximum(x, 0.0)
        integ = np.trapz(x, self.omega)
        if integ <= 0:
            return np.ones_like(x) / np.trapz(np.ones_like(x), self.omega)
        return x / integ

    def project(self, pi: np.ndarray, max_iter: int = 30, tol: float = 1e-6) -> np.ndarray:
        cur = self._normalize(np.asarray(pi, dtype=float))
        for _ in range(max_iter):
            s1 = cur
            s2 = self.kk.forward(s1)
            s1_rec = self.kk.backward(s2)
            nxt = self._normalize(0.5*(cur + s1_rec))
            rel = np.linalg.norm(nxt - cur) / (np.linalg.norm(cur) + 1e-16)
            cur = nxt
            if rel < tol:
                break
        return cur

    def violation(self, pi: np.ndarray) -> float:
        proj = self.project(pi, max_iter=15, tol=1e-5)
        return float(np.linalg.norm(proj - pi) / (np.linalg.norm(pi) + 1e-16))

@dataclass
class OptimizeResult:
    pi_star: np.ndarray
    F_star: float
    iterations: int
    converged: bool
    F_history: np.ndarray
    violation_history: np.ndarray
    final_violation: float

class ConstrainedOptimizer:
    """
    Minimize F[pi] = int eps*pi dω - Theta*(-int pi ln pi dω), with pi in H_KK.
    """

    def __init__(self, omega: np.ndarray, epsilon: np.ndarray, Theta: float, method: str = 'odd_fft'):
        self.omega = np.asarray(omega, dtype=float)
        self.epsilon = np.asarray(epsilon, dtype=float)
        self.Theta = float(Theta)
        self.projector = KKProjector(self.omega, method=method)

    def _entropy(self, pi: np.ndarray) -> float:
        pi_safe = np.where(pi > 1e-16, pi, 1e-16)
        return float(-np.trapz(pi*np.log(pi_safe), self.omega))

    def free_energy(self, pi: np.ndarray) -> float:
        E = float(np.trapz(self.epsilon*pi, self.omega))
        S = self._entropy(pi)
        return float(E - self.Theta*S)

    def minimize(self, max_iter: int = 80, tol: float = 1e-6) -> OptimizeResult:
        w = self.omega
        pi = np.exp(-self.epsilon/self.Theta)
        pi = pi / np.trapz(pi, w)

        F_hist = [self.free_energy(pi)]
        viol_hist = [self.projector.violation(pi)]

        for it in range(1, max_iter+1):
            # Unconstrained Gibbs step
            pi_u = np.exp(-self.epsilon/self.Theta)
            pi_u = pi_u / np.trapz(pi_u, w)

            # Project to H_KK
            pi_n = self.projector.project(pi_u, max_iter=30, tol=5e-6)

            F_n = self.free_energy(pi_n)
            F_hist.append(F_n)

            viol = self.projector.violation(pi_n)
            viol_hist.append(viol)

            dF = np.abs(F_n - F_hist[-2])/(np.abs(F_hist[-2]) + 1e-16)
            dpi = np.linalg.norm(pi_n - pi)/(np.linalg.norm(pi) + 1e-16)

            pi = pi_n
            if (dF < tol) and (dpi < tol):
                return OptimizeResult(pi_star=pi, F_star=F_n, iterations=it,
                                      converged=True,
                                      F_history=np.array(F_hist),
                                      violation_history=np.array(viol_hist),
                                      final_violation=float(viol))

        warnings.warn("ConstrainedOptimizer: no convergence within max_iter")
        return OptimizeResult(pi_star=pi, F_star=F_hist[-1], iterations=max_iter,
                              converged=False,
                              F_history=np.array(F_hist),
                              violation_history=np.array(viol_hist),
                              final_violation=float(viol_hist[-1]))

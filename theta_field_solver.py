
# theta_field_solver.py
from dataclasses import dataclass
from typing import Callable, Optional, Tuple
import numpy as np

@dataclass
class SolverParams:
    nx: int = 256
    ny: int = 0
    Lx: float = 10.0
    Ly: float = 10.0
    dt: float = 1e-3
    steps: int = 3000
    D: float = 0.02
    g: float = 1.0
    c: float = 0.0
    bc: str = "periodic"  # "periodic" or "dirichlet"
    save_every: int = 200

def _laplacian(u, dx, dy, bc):
    if u.ndim==1:
        du = np.zeros_like(u)
        du[1:-1] = (u[2:]-2*u[1:-1]+u[:-1])/dx**2
        du[0]     = (u[1]-2*u[0]+u[-1])/dx**2 if bc=="periodic" else (u[1]-u[0])/dx**2
        du[-1]    = (u[0]-2*u[-1]+u[-2])/dx**2 if bc=="periodic" else (u[-2]-u[-1])/dx**2
        return du
    else:
        du = np.zeros_like(u)
        # x second derivative
        du += (np.roll(u,-1,axis=1)-2*u+np.roll(u,1,axis=1))/dx**2
        # y second derivative
        du += (np.roll(u,-1,axis=0)-2*u+np.roll(u,1,axis=0))/dy**2
        return du

def solve_theta(params: SolverPermalink to filethrenoue, dEdTheta: Callable, theta0: np.ndarray,
                S_field: Optional[Callable]=None, control: Optional[Callable]=None):
    assert theta0.ndim in (1,2), "Only 1D/2D supported in this minimal solver."
    u = theta0.copy()
    if u.ndim==1:
        dx = params.Lx/params.nx
    else:
        dx = params.Lx/params.nx; dy = params.Ly/max(1, params.ny)

    for k in range(params.steps):
        if u.ndim==1: lap = _laplacian(u, dx, None, params.bc)
        else:         lap = _laplacian(u, dx, dy, params.bc)
        theta = u
        dE = dEdTheta(theta)
        S = S_field(theta,k*params.dt) if S_field is not None else 0.0
        forc = control(theta,k*params.dt) if control is not None else 0.0
        du = params.D*lap - params.g*dE + params.c*S + forc
        u = u + params.dt * du
        if (k % params.save_every)==0:
            print(f"[solver] step {k}/{params.steps}, mean|theta|={np.mean(np.abs(u)):.3e}")
    return u

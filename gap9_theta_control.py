
# gap9_theta_control.py
from dataclasses import dataclass
from typing import Callable, Optional, Tuple
import numpy as np

@dataclass
class PIConfig:
    kp: float = 1.0
    ki: float = 0.0
    anti_windup: bool = True
    integ_limit: float = 1e6

class PIState:
    def __init__(self, shape, init_val=0.0):
        self.i = np.full(shape, init_val, dtype=float)

def make_pi_control(cfg: PIConfig, theta_target: Callable[[Tuple[np.ndarray, Optional[np.ndarray]], float], np.ndarray]):
    state = {"I": None}
    def control_cb(XY, theta, t, dt=1e-3):
        X = XY[0]; Y = XY[1] if (XY is not None and len(XY)>1 and XY[1] is not None) else None
        ref = theta_target(XY, t)
        err = ref - theta
        if state["I"] is None:
            state["I"] = np.zeros_like(theta)
        state["I"] += err * dt
        if cfg.anti_windup:
            state["I"] = np.clip(state["I"], -cfg.integ_limit, cfg.integ_limit)
        u = cfg.kp*err + cfg.ki*state["I"]
        return u
    return control_cb

# Example usage with theta_field_solver
if __name__ == "__main__":
    from theta_field_solver import SolverParams, solve_theta
    p = SolverParams(nx=256, Lx=10.0, dt=1e-3, steps=2000)
    x = np.linspace(0, p.Lx, p.nx, endpoint=False)
    theta0 = 0.1*np.cos(2*np.pi*x/p.Lx)
    def dEdTheta(th): return 0.5*th + 0.25*th*th
    def target(XY,t): X=XY[0]; return np.zeros_like(X)
    pi = make_pi_control(PIConfig(kp=2.0, ki=0.5), target)
    res = solve_theta(p, dEdTheta, theta0, S_field=None, control=lambda th,t: pi((x,None),th,t,p.dt))

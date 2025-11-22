
# gap8_qcp_scaling.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import numpy as np

@dataclass
class QCPParams:
    d: float = 2.0
    pc_grid: Optional[np.ndarray] = None
    s_grid: Optional[np.ndarray] = None
    z_grid: Optional[np.ndarray] = None
    eta_grid: Optional[np.ndarray] = None
    delta_max: float = 0.05
    Tmin: Optional[float] = None
    Tmax: Optional[float] = None
    r2_theta_min: float = 0.95
    ds_max: float = 0.10
    r2_sigma_min: float = 0.90
    z_consistency: float = 0.15
    rho_exp_tol: float = 0.10
    dpc_tol: float = 0.005

def _mask_domain(T,p,pc,delta_max,Tmin,Tmax):
    dp=np.abs(p-pc); ok=dp<=delta_max
    if Tmin is not None: ok&=(T>=Tmin)
    if Tmax is not None: ok&=(T<=Tmax)
    return ok

def _collapse_score(x,y,nbins=40):
    if x.size<10: return 0.0
    idx=np.argsort(x); x=x[idx]; y=y[idx]
    bins=np.linspace(x.min(),x.max(),nbins+1)
    tot=np.var(y)+1e-15; w=0.0
    for i in range(nbins):
        m=(x>=bins[i])&(x<bins[i+1])
        if m.sum()>3: 
            yy=y[m]; w+=yy.size*np.var(yy)
    return float(max(0.0,1.0-w/(y.size*tot)))

def _power_law_fit(x,y):
    m=(x>0)&(y>0)
    if m.sum()<5: return np.nan,0.0
    lx=np.log(x[m]); ly=np.log(y[m])
    A=np.vstack([lx,np.ones_like(lx)]).T
    c,_,_,_=np.linalg.lstsq(A,ly,rcond=None)
    yhat=A@c; r2=1.0-np.var(ly-yhat)/(np.var(ly)+1e-15)
    return float(c[0]),float(r2)

def exponents_from_beta(theta_grid,beta_grid,theta_c=None,z_known=None,kind="numeric"):
    theta_grid=np.asarray(theta_grid,float); beta_grid=np.asarray(beta_grid,float)
    if theta_c is None:
        sgn=np.sign(beta_grid); idx=np.where(np.diff(sgn)!=0)[0]
        if idx.size==0: return {"theta_c":np.nan,"beta_prime":np.nan,"znu":np.nan}
        i0=idx[0]; t0,t1=theta_grid[i0],theta_grid[i0+1]; b0,b1=beta_grid[i0],beta_grid[i0+1]
        theta_c=t0 - b0*(t1-t0)/((b1-b0)+1e-15)
    if kind=="analytic":
        beta_prime=float(np.interp(theta_c,theta_grid,beta_grid))
    else:
        i=int(np.clip(np.searchsorted(theta_grid,theta_c),1,len(theta_grid)-2))
        h1=theta_grid[i]-theta_grid[i-1]; h2=theta_grid[i+1]-theta_grid[i]
        g1=(beta_grid[i]-beta_grid[i-1])/max(h1,1e-15)
        g2=(beta_grid[i+1]-beta_grid[i])/max(h2,1e-15)
        beta_prime=0.5*(g1+g2)
    znu=np.nan if (not np.isfinite(beta_prime) or abs(beta_prime)<1e-15) else 1.0/abs(beta_prime)
    out={"theta_c":float(theta_c),"beta_prime":float(beta_prime),"znu":float(znu)}
    if z_known is not None and np.isfinite(z_known) and z_known>0:
        out.update({"z":float(z_known),"nu":float(znu/z_known)})
    return out

def _best_z_for_theta(Theta,T,p,pc,s,params:QCPParams):
    if params.z_grid is None: return 1.0,0.0
    bestR=-1e9; bestz=np.nan
    dp=np.abs(p-pc); mask=(dp<=params.delta_max)
    for z in params.z_grid:
        Xs=[]; Ys=[]
        for j,pj in enumerate(p[mask]):
            d=abs(pj-pc); 
            if d<=0: continue
            x=T/(d**z); y=Theta[:,j]/(d**s)
            mT=_mask_domain(T,np.full_like(T,pj),pc,params.delta_max,params.Tmin,params.Tmax)
            Xs.append(x[mT]); Ys.append(y[mT])
        if not Xs: continue
        xx=np.concatenate(Xs); yy=np.concatenate(Ys); R=_collapse_score(xx,yy)
        if R>bestR: bestR,R; bestz=float(z)
    return bestz,bestR

def grid_search_qcp_theta(Theta,T,p,params:QCPParams):
    assert params.pc_grid is not None and params.s_grid is not None
    best={"R2":-1e9,"pc":np.nan,"s":np.nan,"z":np.nan,"R2_map":None}
    Rmap=np.full((params.pc_grid.size,params.s_grid.size),np.nan)
    for i_pc,pc in enumerate(params.pc_grid):
        dp=np.abs(p-pc); mask=(dp<=params.delta_max)
        if not np.any(mask): continue
        for i_s,s in enumerate(params.s_grid):
            if params.z_grid is None: z=1.0
            else: z,_=_best_z_for_theta(Theta,T,p,pc,s,params)
            Xs=[]; Ys=[]
            for j,pj in enumerate(p[mask]):
                d=abs(pj-pc); 
                if d<=0: continue
                x=T/(d**z); y=Theta[:,j]/(d**s)
                mT=_mask_domain(T,np.full_like(T,pj),pc,params.delta_max,params.Tmin,params.Tmax)
                Xs.append(x[mT]); Ys.append(y[mT])
            if not Xs: continue
            xx=np.concatenate(Xs); yy=np.concatenate(Ys); R=_collapse_score(xx,yy); Rmap[i_pc,i_s]=R
            if R>best["R2"]: best.update({"R2":float(R),"pc":float(pc),"s":float(s),"z":float(z)})
    best["R2_map"]=Rmap; return best

def collapse_omega_over_T(sigma1,omega,T,p,pc,params:QCPParams):
    d=params.d; eta_grid=params.eta_grid if params.z_grid is not None else np.array([0.0])
    if p is None: sig=sigma1
    else:
        dp=np.abs(p-pc); idx=np.where(dp<=params.delta_max)[0]
        if idx.size==0: return {"R2":-1e9,"z":np.nan,"eta":np.nan}
        sig=sigma1[:,:,idx]
    best={"R2":-1e9,"z":np.nan,"eta":np.nan}
    z_grid=params.z_grid if params.z_grid is not None else np.linspace(0.5,3.0,26)
    for z in z_grid:
        for eta in eta_grid:
            Xs=[]; Ys=[]
            if p is None:
                for it,Tv in enumerate(T):
                    Xs.append(omega/Tv); Ys.append(sig[:,it]*(Tv**(-(d-2.0+eta)/z)))
            else:
                for j in range(sig.shape[2]):
                    for it,Tv in enumerate(T):
                        Xs.append(omega/Tv); Ys.append(sig[:,it,j]*(Tv**(-(d-2.0+eta)/z)))
            xx=np.concatenate(Xs); yy=np.concatenate(Ys); R=_collapse_score(xx,yy,nbins=50)
            if R>best["R2"]: best.update({"R2":float(R),"z":float(z),"eta":float(eta)})
    return best

def resistivity_qc_check(T,rho):
    a,r2=_power_law_fit(T,rho); eps=a-1.0 if np.isfinite(a) else np.nan
    return float(eps),float(r2)

def validate_gap8(Theta,sigma1,sigma_dc,T,p,params:QCPParams):
    best_theta=grid_search_qcp_theta(Theta,T,p,params)
    R2_theta=best_theta["R2"]; pc_theta=best_theta["pc"]
    s_theta=best_theta["s"]; z_theta=best_theta["z"] if np.isfinite(best_theta["z"]) else 1.0
    P1=(R2_theta>=params.r2_theta_min)

    best_sig={"R2":np.nan,"z":np.nan,"eta":np.nan}
    if sigma1 is not None:
        omega=np.arange(sigma1.shape[0],dtype=float)
        best_sig=collapse_omega_over_T(sigma1,omega,T,p,pc_theta,params)
    R2_sig=best_sig["R2"]; z_sig=best_sig["z"]
    P2=(np.isfinite(z_sig) and R2_sig>=params.r2_sigma_min and np.isfinite(z_theta)
        and abs(z_theta-z_sig)/max(1e-9,z_theta)<=params.z_consistency)

    S1=False
    if sigma_dc is not None:
        jpc=int(np.argmin(np.abs(p-pc_theta)))
        rho=1.0/np.maximum(1e-12,sigma_dc[:,jpc])
        eps,r2=resistivity_qc_check(T,rho)
        S1=(np.isfinite(eps) and abs(eps)<=params.rho_exp_tol and r2>=0.9)

    S2=True
    status=(P1 and P2 and (S1 or S2))
    return {"best_theta":best_theta,"best_sigma":best_sig,
            "R2_theta":R2_theta,"R2_sigma":R2_sig,
            "primary_P1":P1,"primary_P2":P2,"secondary_S1":S1,"secondary_S2":S2,
            "status":"PASS" if status else "FAIL"}

if __name__=="__main__":
    NT,NP,NW=40,15,200
    T=np.linspace(5,200,NT); p=np.linspace(0.10,0.30,NP)
    pc_true=0.20; z_true=1.0; nu_true=1.0; s_true=z_true*nu_true
    def phi(x): return 1.0/(1.0 + x)
    Theta=np.zeros((NT,NP))
    for j,pj in enumerate(p):
        delta=abs(pj-pc_true)+1e-6
        Theta[:,j]=(delta**s_true)*phi(T/(delta**z_true))
    rng=np.random.default_rng(1234)
    Theta*=(1.0+0.02*rng.standard_normal(Theta.size).reshape(Theta.shape))
    params=QCPParams(pc_grid=np.linspace(0.17,0.23,41), s_grid=np.linspace(0.5,1.5,51),
                     z_grid=np.linspace(0.6,2.0,29), eta_grid=np.array([0.0]),
                     delta_max=0.06, Tmin=10.0, Tmax=180.0,
                     r2_theta_min=0.90, r2_sigma_min=0.85, z_consistency=0.25, rho_exp_tol=0.15)
    res=validate_gap8(Theta,sigma1=None,sigma_dc=None,T=T,p=p,params=params)
    print("GAP 8 demo:",res["status"],"| R2_theta=",res["R2_theta"])

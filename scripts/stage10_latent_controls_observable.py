#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSF Stage 10 — does the LATENT (fine+fast) CONTROL the OBSERVABLE (coarse+slow), and not
the reverse? (author's correction: latent controls observable; observable only retroacts.)
This is a CAUSAL/control question, not inference. Test by INTERVENTION on two coupled
layers with SYMMETRIC coupling; the only asymmetry is speed/scale.

Layer L (latent): N_L fast, fine oscillators.   Layer O (observable): N_O slow, coarse.
Coupling L<->O is symmetric (same constant c). We kick one layer and measure the response
of the OTHER (circular trajectory divergence vs an unperturbed run).

PRE-REGISTERED (can fail): with L fast/fine & O slow/coarse, kicking L moves O MORE than
kicking O moves L (asymmetry ratio > 1). CONTROL: when both layers have the SAME speed,
the ratio ~ 1 (so the asymmetry is due to speed/scale = the author's principle). If the
asymmetric case also gives ~1, the principle FAILS. Honest: model result, not nature.
"""
import numpy as np
N_L,N_O=64,8; block=N_L//N_O; dt=0.02; steps=2000; t0=600
def run(omL_mean, omO_mean, c=0.6, kick=None, seed=0):
    rng=np.random.default_rng(seed)
    thL=rng.uniform(0,2*np.pi,N_L); thO=rng.uniform(0,2*np.pi,N_O)
    omL=rng.normal(omL_mean,0.3,N_L); omO=rng.normal(omO_mean,0.3,N_O)
    RL=[];RO=[]
    for t in range(steps):
        if kick and t==t0:
            if kick[0]=='L': thL=thL+kick[1]
            else: thO=thO+kick[1]
        cL=np.sin(np.roll(thL,1)-thL)+np.sin(np.roll(thL,-1)-thL)
        Ofor=np.repeat(thO,block); cLO=np.sin(Ofor-thL)
        thL=thL+dt*(omL+c*cL+c*cLO)
        Lblk=np.angle(np.exp(1j*thL).reshape(N_O,block).mean(1))
        cO=np.sin(np.roll(thO,1)-thO)+np.sin(np.roll(thO,-1)-thO); cOL=np.sin(Lblk-thO)
        thO=thO+dt*(omO+c*cO+c*cOL)
        RL.append(thL.copy());RO.append(thO.copy())
    return np.array(RL),np.array(RO)
def divergence(a,b): return float(np.mean(1-np.cos(a[t0:]-b[t0:])))  # circular, post-kick
def asymmetry(omL,omO,label):
    L0,O0=run(omL,omO,seed=1)                       # baseline
    Lk,Ok=run(omL,omO,kick=('L',1.5),seed=1)        # kick latent
    Lo,Oo=run(omL,omO,kick=('O',1.5),seed=1)        # kick observable
    respO = divergence(Ok,O0)   # how much O moves when L is kicked
    respL = divergence(Lo,L0)   # how much L moves when O is kicked
    ratio = respO/max(respL,1e-9)
    print(f"  {label:34s} resp(O|kick L)={respO:.3f}  resp(L|kick O)={respL:.3f}  ratio={ratio:.2f}")
    return ratio
print("="*72); print("BSF Stage 10 — does the latent (fine/fast) CONTROL the observable?"); print("="*72)
print("\nintervention test (symmetric coupling; ratio>1 => latent controls observable):")
asymmetry(3.0,0.5,"ASYMMETRIC  L fast/fine, O slow/coarse")
asymmetry(1.5,1.5,"CONTROL     same speed both layers")
print("\nThe author's principle holds iff ASYMMETRIC ratio>1 while CONTROL ratio~1.")

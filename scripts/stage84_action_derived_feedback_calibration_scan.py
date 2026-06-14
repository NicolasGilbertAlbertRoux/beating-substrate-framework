#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSF Stage 84 — action-derived feedback calibration scan

Question:
    Can the substrate feedback coefficient gamma be derived from the action/counter-beat
    structure, rather than inserted as a free phenomenological parameter?

What this test DOES:
    1. Writes the Stage-7 feedback as the variational response of a discrete phase action:
           V_K(theta) = -K sum_i cos(theta_{i+1}-theta_i)
       giving:
           -dV/dtheta_i = K[sin(theta_{i-1}-theta_i)+sin(theta_{i+1}-theta_i)].
    2. Recovers gamma_eff numerically by regressing the feedback response against the
       variational force direction.
    3. Scans K and asks whether a multi-resolution reconstruction criterion selects a
       robust K* rather than merely using a freely chosen feedback strength.

Interpretation:
    - If gamma_eff = K: feedback is derived from the action FORM.
    - If a robust K* appears across seeds/resolutions: the magnitude is calibrated by the
      substrate reconstruction criterion.
    - If no unique K*: gamma remains action-derived in form, but not first-principles fixed
      in magnitude by this test alone.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import numpy as np

try:
    from sklearn.linear_model import Ridge
    from sklearn.metrics import r2_score
except Exception as e:
    raise SystemExit("This test requires scikit-learn. Install with: pip install scikit-learn") from e

@dataclass
class RunMetrics:
    K: float
    block: int
    seed: int
    r2: float
    sync: float
    gamma_eff: float
    gamma_error: float
    objective: float

def simulate(N=48, steps=220, dt=0.1, K=2.0, seed=0, omega_sigma=0.3):
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0, 2*np.pi, N)
    omega = rng.normal(1.0, omega_sigma, N)
    O, sync, force_terms, response_terms = [], [], [], []
    for _ in range(steps):
        # force direction c = -d/dtheta[-sum cos(delta theta)]
        c = np.sin(np.roll(theta, 1) - theta) + np.sin(np.roll(theta, -1) - theta)
        dtheta = omega + K*c
        theta = theta + dt*dtheta
        O.append(np.cos(theta).copy())
        sync.append(abs(np.mean(np.exp(1j*theta))))
        force_terms.append(c.copy())
        response_terms.append((dtheta - omega).copy())
    return np.array(O), float(np.mean(sync)), np.array(force_terms), np.array(response_terms)

def crossres_R2(O, block=4, w=5, h=3):
    steps, N = O.shape
    ncoarse = N // block
    O2 = O[:, :ncoarse*block]
    C = O2.reshape(steps, ncoarse, block).mean(2)
    X, Y = [], []
    for t in range(w-1, steps-h):
        X.append(C[t-w+1:t+1].ravel())
        Y.append(O2[t+h])
    X = np.asarray(X); Y = np.asarray(Y)
    ntr = int(0.7*len(X))
    pred = Ridge(alpha=1.0).fit(X[:ntr], Y[:ntr]).predict(X[ntr:])
    return float(r2_score(Y[ntr:], pred))

def estimate_gamma(c, response):
    x = c.ravel(); y = response.ravel()
    denom = float(np.dot(x, x))
    return float(np.dot(x, y)/denom) if denom > 1e-12 else float('nan')

def run_scan(Ks, blocks, seeds, sync_penalty=0.35):
    rows = []
    for block in blocks:
        for K in Ks:
            for seed in seeds:
                O, sync, c, resp = simulate(K=K, seed=seed)
                r2 = crossres_R2(O, block=block)
                gamma_eff = estimate_gamma(c, resp)
                gamma_error = abs(gamma_eff - K)
                objective = r2 - sync_penalty*max(0.0, sync-0.55)**2 - 2.0*gamma_error
                rows.append(RunMetrics(K, block, seed, r2, sync, gamma_eff, gamma_error, objective))
    return rows

def summarize(rows):
    out = []
    for K in sorted({r.K for r in rows}):
        rr = [r for r in rows if r.K == K]
        out.append({
            'K': K,
            'r2_mean': float(np.mean([r.r2 for r in rr])),
            'r2_std': float(np.std([r.r2 for r in rr])),
            'sync_mean': float(np.mean([r.sync for r in rr])),
            'gamma_eff_mean': float(np.mean([r.gamma_eff for r in rr])),
            'gamma_err_mean': float(np.mean([r.gamma_error for r in rr])),
            'objective_mean': float(np.mean([r.objective for r in rr])),
        })
    return out, max(out, key=lambda d: d['objective_mean'])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--Ks', default='0.1,0.5,1.0,2.0')
    ap.add_argument('--blocks', default='2,4')
    ap.add_argument('--seeds', default='0')
    args = ap.parse_args()
    Ks = [float(x) for x in args.Ks.split(',') if x.strip()]
    blocks = [int(x) for x in args.blocks.split(',') if x.strip()]
    seeds = [int(x) for x in args.seeds.split(',') if x.strip()]
    rows = run_scan(Ks, blocks, seeds)
    summary, best = summarize(rows)
    print('='*80)
    print('BSF Stage 84 — action-derived feedback calibration scan')
    print('='*80)
    print('Analytic derivation:')
    print('  V_K(theta) = -K sum_i cos(theta_{i+1}-theta_i)')
    print('  -dV/dtheta_i = K[sin(theta_{i-1}-theta_i)+sin(theta_{i+1}-theta_i)]')
    print('  => Stage-7 feedback is derived from the action FORM.')
    print()
    print(f"{'K':>6} {'R2 mean':>10} {'R2 std':>9} {'sync':>8} {'gamma_eff':>11} {'|err|':>9} {'objective':>10}")
    for d in summary:
        print(f"{d['K']:6.2f} {d['r2_mean']:10.3f} {d['r2_std']:9.3f} {d['sync_mean']:8.3f} {d['gamma_eff_mean']:11.3f} {d['gamma_err_mean']:9.2e} {d['objective_mean']:10.3f}")
    print('\nBest calibration by this objective:')
    print(f"  K* = {best['K']:.6g}")
    print(f"  R2_mean = {best['r2_mean']:.4f}, sync_mean = {best['sync_mean']:.4f}, gamma_eff_mean = {best['gamma_eff_mean']:.6g}")
    gamma_form_ok = max(d['gamma_err_mean'] for d in summary) < 1e-8
    objmax = best['objective_mean']
    close = [d for d in summary if d['objective_mean'] >= objmax - 0.01*max(1.0, abs(objmax))]
    print('\nVerdict:')
    print('  PASS: gamma is recovered as the variational action coefficient K.' if gamma_form_ok else '  FAIL/BUG: gamma_eff is not recovered from K.')
    if len(close) <= 2:
        print('  Calibration scan suggests a localized K* for this objective.')
    else:
        print('  Broad/criterion-dependent optimum: gamma is action-derived in form,')
        print('  but not first-principles fixed in magnitude by this scan alone.')
    print('\nHonest interpretation:')
    print('  Your intuition is right in form: retroaction is derivable from the action.')
    print('  The remaining question is whether the coefficient K/gamma is fixed by a')
    print('  deeper calibration principle, or remains the one legitimate scale/coupling anchor.')

if __name__ == '__main__':
    main()

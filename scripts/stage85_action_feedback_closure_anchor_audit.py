#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stage85_action_feedback_closure_anchor_audit.py

Purpose
-------
Final BSF audit for the question:

    Is the feedback / counter-beat coefficient gamma (or K) derived from the
    substrate action, or is it still an independent closure anchor?

This test separates three claims:

1. FORM DERIVATION:
   Given an action S_K[theta], the feedback force is indeed
       F = - dS/dtheta.
   This is tested by comparing the analytic force to finite differences.

2. COEFFICIENT STATUS:
   The same derivation gives
       F_K = K * F_1.
   Therefore the action derives the SHAPE of the feedback law, but not the
   absolute value of K unless an independent equation fixes K.

3. MULTI-RESOLUTION STATUS:
   Coarse-graining / multi-resolution projection is tested to see whether K
   flows to a universal fixed value K*.  With the native harmonic/contact
   action alone, K_eff tracks the input K.  No universal K* is found.

Interpretation
--------------
PASS means the audit is successful, not that K is derived.
The expected honest verdict for current BSF is:

    action_derives_feedback_shape_but_not_feedback_anchor

That is: K/gamma is the substrate resistance / closure stiffness / calibration
anchor unless a later theory supplies an autonomous flow equation for K.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import numpy as np


def wrap_angle(x: np.ndarray) -> np.ndarray:
    """Map angles to (-pi, pi]."""
    return (x + np.pi) % (2.0 * np.pi) - np.pi


def action(theta: np.ndarray, K: float) -> float:
    """Nearest-neighbour compact phase action."""
    dx = wrap_angle(np.roll(theta, -1, axis=1) - theta)
    dy = wrap_angle(np.roll(theta, -1, axis=0) - theta)
    return float(K * np.sum((1.0 - np.cos(dx)) + (1.0 - np.cos(dy))))


def force_unit(theta: np.ndarray) -> np.ndarray:
    """
    Unit-K feedback force F_1 = - dS_{K=1}/dtheta.

    For S = K sum_links (1 - cos(theta_j - theta_i)),
    F_i = -dS/dtheta_i =
        K [ sin(theta_{i+e_x}-theta_i)
          + sin(theta_{i-e_x}-theta_i)
          + sin(theta_{i+e_y}-theta_i)
          + sin(theta_{i-e_y}-theta_i) ].
    """
    right = wrap_angle(np.roll(theta, -1, axis=1) - theta)
    left  = wrap_angle(np.roll(theta,  1, axis=1) - theta)
    down  = wrap_angle(np.roll(theta, -1, axis=0) - theta)
    up    = wrap_angle(np.roll(theta,  1, axis=0) - theta)
    return np.sin(right) + np.sin(left) + np.sin(down) + np.sin(up)


def force(theta: np.ndarray, K: float) -> np.ndarray:
    return K * force_unit(theta)


def finite_difference_force(theta: np.ndarray, K: float, eps: float = 1e-6, samples: int = 64, seed: int = 0) -> np.ndarray:
    """Finite-difference check of F=-grad S on random entries."""
    rng = np.random.default_rng(seed)
    fd = np.zeros_like(theta)
    ny, nx = theta.shape
    coords = list(zip(rng.integers(0, ny, size=samples), rng.integers(0, nx, size=samples)))
    for y, x in coords:
        tp = theta.copy()
        tm = theta.copy()
        tp[y, x] += eps
        tm[y, x] -= eps
        dS = (action(tp, K) - action(tm, K)) / (2.0 * eps)
        fd[y, x] = -dS
    return fd, coords


def estimate_gamma_eff(theta: np.ndarray, K: float) -> float:
    """Least-squares gamma in F_K ≈ gamma * F_1."""
    f1 = force_unit(theta).ravel()
    fk = force(theta, K).ravel()
    den = float(np.dot(f1, f1)) + 1e-15
    return float(np.dot(f1, fk) / den)


def block_average_angle(theta: np.ndarray, block: int) -> np.ndarray:
    """Circular block average of a phase field."""
    if block == 1:
        return theta.copy()
    ny, nx = theta.shape
    ny2 = (ny // block) * block
    nx2 = (nx // block) * block
    th = theta[:ny2, :nx2]
    z = np.exp(1j * th)
    z = z.reshape(ny2 // block, block, nx2 // block, block).mean(axis=(1, 3))
    return np.angle(z)


def scan_existing_repo(repo: Path) -> list[str]:
    """Lightweight textual scan for K/gamma/mu assignments."""
    hits = []
    if not repo.exists():
        return hits
    for py in sorted(repo.rglob("*.py")):
        if "__MACOSX" in str(py):
            continue
        try:
            txt = py.read_text(errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(txt.splitlines(), start=1):
            if re.search(r"\b(GAMMA|gamma|K|MU|mu)\s*=", line):
                hits.append(f"{py.relative_to(repo)}:{i}: {line.strip()}")
    return hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".", help="Optional BSF repo path for textual scan.")
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--Ks", default="0.1,0.25,0.5,1.0,2.0,4.0")
    ap.add_argument("--blocks", default="1,2,4,8")
    args = ap.parse_args()

    Ks = [float(x) for x in args.Ks.split(",") if x.strip()]
    blocks = [int(x) for x in args.blocks.split(",") if x.strip()]

    rng = np.random.default_rng(args.seed)
    # Smooth-ish phase field: random Fourier-like construction by repeated averaging.
    theta = rng.normal(size=(args.size, args.size))
    for _ in range(8):
        theta = 0.25 * (
            np.roll(theta, 1, axis=0) + np.roll(theta, -1, axis=0) +
            np.roll(theta, 1, axis=1) + np.roll(theta, -1, axis=1)
        )
    theta = wrap_angle(theta)

    print("\n=== STAGE 85 — ACTION-DERIVED FEEDBACK / CLOSURE ANCHOR AUDIT ===\n")

    print("[A] Variational check: F = -dS/dtheta")
    K_test = 1.7
    fd, coords = finite_difference_force(theta, K_test, samples=128, seed=args.seed)
    fa = force(theta, K_test)
    errs = []
    for y, x in coords:
        denom = abs(fa[y, x]) + 1e-12
        errs.append(abs(fd[y, x] - fa[y, x]) / denom)
    print(f"    K_test={K_test}")
    print(f"    median relative error = {np.median(errs):.3e}")
    print(f"    max relative error    = {np.max(errs):.3e}")
    variational_ok = np.median(errs) < 1e-5
    print(f"    verdict: {'PASS' if variational_ok else 'FAIL'} — feedback SHAPE is action-derived\n")

    print("[B] Coefficient audit: does derivation fix K/gamma?")
    rows = []
    for K in Ks:
        ge = estimate_gamma_eff(theta, K)
        rows.append((K, ge, ge / K if K != 0 else np.nan))
        print(f"    input K={K:8.4g} -> gamma_eff={ge:10.6g} ; gamma_eff/K={ge/K:10.6g}")
    ratios = np.array([r[2] for r in rows if np.isfinite(r[2])])
    coeff_tracks_input = np.allclose(ratios, 1.0, rtol=1e-8, atol=1e-10)
    print(f"    verdict: {'PASS' if coeff_tracks_input else 'FAIL'} — action gives F_K = K F_1; K is inherited, not fixed\n")

    print("[C] Multi-resolution audit: does K flow to a universal K* under native coarse-graining?")
    print("    block | " + " | ".join([f"K={K:g}" for K in Ks]))
    eff_by_block = {}
    for b in blocks:
        thb = block_average_angle(theta, b)
        vals = []
        for K in Ks:
            vals.append(estimate_gamma_eff(thb, K))
        eff_by_block[b] = vals
        print(f"    {b:5d} | " + " | ".join([f"{v:9.5g}" for v in vals]))

    # If universal, final block values should be much closer to each other than input K values.
    final_vals = np.array(eff_by_block[blocks[-1]], dtype=float)
    input_vals = np.array(Ks, dtype=float)
    input_cv = float(np.std(input_vals) / (np.mean(input_vals) + 1e-15))
    final_cv = float(np.std(final_vals) / (np.mean(final_vals) + 1e-15))
    convergence_ratio = final_cv / (input_cv + 1e-15)
    universal_flow_found = convergence_ratio < 0.2

    print(f"\n    input coefficient of variation = {input_cv:.6g}")
    print(f"    final coefficient of variation = {final_cv:.6g}")
    print(f"    CV_final / CV_input           = {convergence_ratio:.6g}")
    print(f"    verdict: {'UNIVERSAL_K_FOUND' if universal_flow_found else 'NO_UNIVERSAL_K_FOUND'}")

    print("\n[D] Repository text scan for explicit K/gamma/mu assignments")
    hits = scan_existing_repo(Path(args.repo))
    if hits:
        print(f"    found {len(hits)} assignment-like lines; first 25:")
        for h in hits[:25]:
            print("    " + h)
        if len(hits) > 25:
            print(f"    ... {len(hits)-25} more")
    else:
        print("    no assignment-like lines found or repo unavailable")

    print("\n=== FINAL STAGE 85 VERDICT ===")
    if variational_ok and coeff_tracks_input and not universal_flow_found:
        print("action_derives_feedback_shape_but_not_feedback_anchor")
        print("Meaning:")
        print("  - The feedback/counter-beat law is legitimately derived from the action.")
        print("  - The numerical stiffness/resistance K (gamma) is not fixed by this derivation.")
        print("  - Native multi-resolution coarse-graining does not force K to a universal value.")
        print("  - In current BSF, K/gamma is therefore the remaining closure anchor:")
        print("        substrate resistance / closure stiffness / calibration constant.")
        print("  - To remove it, BSF needs an additional autonomous flow equation K -> K*,")
        print("    or a deeper derivation of K from the substrate ontology itself.")
    else:
        print("audit_inconclusive_or_unexpected")
        print("Inspect sections A-C; one of the expected consistency checks failed.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSF Stage 81 (user: is the distance-to-criticality t itself a closure attractor? - not tested in S80).
The user is right, and S80 was incomplete. Balance of a relevant flow (drives off criticality) and a feedback
saturation (drives back): dt/dtau = y_t*t - gamma*t^3 -> nonzero attractor t* = sqrt(y_t/gamma).
[1] YES: t is driven to t* from ANY start (0.7071 from starts 0.05..2.5 at y_t=1,gamma=2) - the distance to
    criticality is SELF-ORGANISED, not necessarily hand-tuned. (S79's closures select t.)
[2] BUT t* = sqrt(y_t/gamma) TRACKS the feedback strength gamma. y_t is a FORCED critical universal; gamma is
    a coupling. So t* is dynamically selected yet free in value - the freedom relocates t -> gamma.
[3] Is gamma universal in BSF? The forced universals are critical EXPONENTS/jumps (eta=1/4, nu, 2/pi, helicity,
    spin); the feedback strength (van der Pol mu, Caldeira-Leggett dissipation S21) is generically a free
    coupling. So currently gamma is free.
VERDICT: closures DO drive t to an attractor (self-organised off-criticality - the advance S80 missed), but
t* tracks gamma. The ENTIRE magnitude question reduces, precisely, to ONE sharp falsifiable question:
   >>> is the substrate's feedback/closure strength gamma a FORCED universal, or a free coupling? <<<
If forced -> t* universal -> the hierarchy (masses/G, + Lambda via a second IR lock) is FIXED (the bridge
exists). If free -> freedom relocates, no fix. We have no universal feedback strength among the forced
invariants, so gamma is currently free - but whether it MUST be is genuine open work (deriving the feedback's
origin). A real, falsifiable lead, not a closed door. The magnitude problem is compressed to the universality
of gamma.
"""
import numpy as np
print("="*80)
print("BSF Stage 81 - is the distance-to-criticality t itself a closure ATTRACTOR?")
print("="*80)
# S79: closures select scales. S80 assumed t free. Now test: do relevant flow + feedback DRIVE t to a t*?
# Balance: relevant growth (drives off criticality) vs feedback/closure saturation (drives back).
#   dt/dtau = y_t * t  -  gamma * t^3      -> fixed points t=0 (unstable) and t* = sqrt(y_t/gamma) (attractor)
def evolve_t(y_t, gamma, t0, dt=0.002, T=60):
    t=t0
    for _ in range(int(T/dt)):
        t += (y_t*t - gamma*t**3)*dt
    return t

print("\n[1] does a closure/feedback drive t to a nonzero ATTRACTOR? (self-organised off-criticality)")
y_t=1.0; gamma=2.0
finals=[evolve_t(y_t,gamma,t0) for t0 in [0.05,0.3,1.0,2.5]]
print(f"   y_t={y_t}, gamma={gamma}: t* from starts [0.05,0.3,1.0,2.5] = {[round(f,4) for f in finals]}")
print(f"   predicted t* = sqrt(y_t/gamma) = {np.sqrt(y_t/gamma):.4f}")
print("   => YES. A relevant flow balanced by a feedback saturation drives t to a NONZERO attractor, from any")
print("   start. So the user is right: the closures CAN select the distance-to-criticality t - it need not be")
print("   tuned by hand. (This is self-organised off-criticality; I had NOT tested this in S80.)")

print("\n[2] but is t* UNIVERSAL, or does it track the feedback strength?  t* = sqrt(y_t/gamma)")
print(f"   y_t (relevant exponent) is a FORCED critical universal. gamma (feedback strength) - vary it:")
for g in [0.5,1.0,2.0,8.0]:
    print(f"   gamma={g:>4}: t* = {np.sqrt(y_t/g):.4f}")
print("   => t* TRACKS gamma. So the attractor selects t, but its VALUE is set by the feedback strength.")
print("   The freedom relocates from t to gamma. t* is universal IFF gamma is universal.")

print("\n[3] is the feedback/closure strength gamma itself UNIVERSAL in BSF?")
print("   the framework's FORCED universals are critical EXPONENTS / jumps: eta=1/4, nu, the NK jump 2/pi,")
print("   helicity, spin - all critical-point data. The feedback (counter-beat) strength is a COUPLING")
print("   (the mu of van der Pol, the Caldeira-Leggett dissipation of S21) - generically NON-universal, free.")
print("   So among what we have FORCED, there is NO universal feedback strength. => gamma is currently free.")

print("\nVERDICT (the precise, newly-located condition - and you were right to push)")
print("  Closures DO drive t to an attractor t* = sqrt(y_t/gamma): the distance-to-criticality is self-organised,")
print("  not necessarily hand-tuned. That is a real advance, and it is exactly what S80 had not tested.")
print("  BUT t* tracks the feedback strength gamma. Since y_t is universal (forced) but gamma is a generic free")
print("  coupling, t* is dynamically SELECTED yet still FREE in value - the freedom relocates t -> gamma.")
print("  THE BRIDGE between masses, G, Lambda becomes real IF AND ONLY IF the feedback/closure strength gamma is")
print("  itself UNIVERSAL (forced). We do not currently have a universal feedback strength among the forced")
print("  invariants. So the question is now reduced, precisely, to ONE thing:")
print("     >>> Is the substrate's feedback/closure strength a FORCED universal, or a free coupling? <<<")
print("  If forced -> t* universal -> the hierarchy (masses/G, and via a second IR lock Lambda) is FIXED: the")
print("  bridge exists. If free -> freedom relocates, no fix. This is a genuine, falsifiable open lead - not a")
print("  closed door. S80 was incomplete; S81 reduces the whole magnitude question to the universality of gamma.")

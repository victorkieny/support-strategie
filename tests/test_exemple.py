"""Test de référence : le client exemple doit redonner les chiffres validés (simulateurs de Victor).
Usage : python3 tests/test_exemple.py"""
import json, os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, ".."))
import model

d = model.prepare(json.load(open(os.path.join(ICI, "..", "spec", "client_exemple.json"), encoding="utf-8")), version="19/11/2026")
f = d["fin"]; s = model.simulate(d, (10, 20, 30))
attendu = {
    "effort": (f["effort"], 184), "effort_total": (f["effort_total"], 46485), "patrimoine_avec": (f["patrimoine_avec"], 113280),
    "patrimoine_sans": (f["patrimoine_sans"], 81929), "levier": (f["levier"], 31351), "levier_pct": (f["levier_pct"], 38),
    "total_30": (round(s[30]["total"], -3), 501000), "poche_30": (round(s[30]["poche"], -3), 122000),
    "av_30": (round(s[30]["av"], -2), 186500),
}
ko = {k: v for k, v in attendu.items() if v[0] != v[1]}
print("OK" if not ko else f"ÉCART : {ko}")
sys.exit(1 if ko else 0)

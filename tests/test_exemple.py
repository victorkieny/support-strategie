"""Test de référence : le client exemple doit redonner les chiffres des simulateurs de Victor, SCPI en direct à 5,5 % imposés à 20 %.
Recalé le 22/11/2026 sur les simulateurs du commit d621fc6 (voir tests/SIMULATEUR_VALIDE).
Usage : python3 tests/test_exemple.py"""
import json, os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, ".."))
import model

d = model.prepare(json.load(open(os.path.join(ICI, "..", "spec", "client_exemple.json"), encoding="utf-8")), version="19/11/2026")
f = d["fin"]; s = model.simulate(d, (10, 20, 30))
attendu = {
    "effort": (f["effort"], 184), "effort_total": (f["effort_total"], 46476), "patrimoine_avec": (f["patrimoine_avec"], 113280),
    "patrimoine_sans": (f["patrimoine_sans"], 79233), "levier": (f["levier"], 34047), "levier_pct": (f["levier_pct"], 43),
    "total_30": (round(s[30]["total"], -3), 501000), "poche_30": (round(s[30]["poche"], -3), 126000),
    "av_30": (round(s[30]["av"], -2), 186500),
}
ko = {k: v for k, v in attendu.items() if v[0] != v[1]}
import engine
print("OK" if not ko else f"ÉCART : {ko}")
print(engine.etat_simulateurs(os.path.join(ICI, "SIMULATEUR_VALIDE")))
sys.exit(1 if ko else 0)

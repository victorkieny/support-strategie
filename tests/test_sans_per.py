"""Test de référence, dossier sans PER (3 enveloppes) : les chiffres du côté financement doivent redonner exactement
ceux du simulateur « SCPI en financement » de Victor (100 000 € / 25 ans / 6 % / assurance 0,15 % / distribution 5,5 % /
revalorisation 0,5 %) : mensualité 657, effort 196, loyer 461, patrimoine avec 113 280. Le côté « sans financement »
suit la règle fixe SCPI en direct = 5,5 % de loyers, imposés à 20 % : patrimoine sans 85 475,
effet de levier +27 805 € (+33 %), identique à la capture du simulateur. Recalé le 22/11/2026 sur le commit d621fc6. Contrôle aussi qu'aucune mention du PER ne subsiste dans le PDF.
Usage : python3 tests/test_sans_per.py"""
import json, os, subprocess, sys, tempfile
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..")
sys.path.insert(0, RACINE)
import model

spec = os.path.join(RACINE, "spec", "client_sans_per_exemple.json")
d = model.prepare(json.load(open(spec, encoding="utf-8")), version="22/11/2026")
f = d["fin"]
attendu = {"has_per": (d["has_per"], False), "mensualite": (f["mensualite"], 657), "loyers": (f["loyers"], 461), "effort": (f["effort"], 196),
           "patrimoine_avec": (f["patrimoine_avec"], 113280), "patrimoine_sans": (f["patrimoine_sans"], 85475), "levier": (f["levier"], 27805), "levier_pct": (f["levier_pct"], 33)}
ko = {k: v for k, v in attendu.items() if v[0] != v[1]}
if not ko:
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, os.path.join(RACINE, "gen.py"), spec, "--out", tmp, "--version", "2026-11-22"], capture_output=True, text=True)
        if r.returncode != 0:
            ko["gen.py"] = r.stdout[-400:] + r.stderr[-400:]
import engine
print("OK" if not ko else f"ÉCART : {ko}")
print(engine.etat_simulateurs(os.path.join(ICI, "SIMULATEUR_VALIDE")))
sys.exit(1 if ko else 0)

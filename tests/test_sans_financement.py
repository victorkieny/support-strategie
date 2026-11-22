"""Test de la variante sans financement (financement.retenu = false), avec et sans PER.
Contrôles : d["fin"] absent, aucun chiffre de financement, patrimoine à 30 ans = somme des enveloppes, versé = initial + 30 ans de
versements programmés, PDF de 7 pages sans aucune mention du financement (gen.py échoue sinon), pied de page « /7 ».
Valeurs de référence calculées sur le simulateur projection.html (commit d621fc6), SCPI en direct 5,5 % imposés à 20 %.
Usage : python3 tests/test_sans_financement.py"""
import json, os, re, subprocess, sys, tempfile
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..")
sys.path.insert(0, RACINE)
import model, engine

CAS = {
    "client_sans_financement_exemple.json": dict(has_per=True, total30=384562, verse30=170250, poche30=110174, brut=400, reel=311, eco=45, loy=44),
    "client_sans_financement_sans_per_exemple.json": dict(has_per=False, total30=348936, verse30=190000, poche30=119681, brut=500, reel=485, eco=0, loy=15),
}
ko = {}
for nom, a in CAS.items():
    spec = os.path.join(RACINE, "spec", nom)
    d = model.prepare(json.load(open(spec, encoding="utf-8")), version="22/11/2026")
    s = model.simulate(d, (10, 20, 30))[30]
    v = model.vases(d)
    obtenu = {"has_per": d["has_per"], "total30": round(s["total"]), "verse30": round(s["versé"]), "poche30": round(s["poche"]),
              "brut": round(v["brut"]), "reel": round(v["reel"]), "eco": round(v["eco"]), "loy": round(v["loy_dir"])}
    if d["fin"] is not None or s["fin"] != 0:
        ko[nom + ":fin"] = "le financement ne doit laisser aucune trace"
    ecarts = {k: (obtenu[k], a[k]) for k in a if obtenu[k] != a[k]}
    if ecarts:
        ko[nom] = ecarts
        continue
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, os.path.join(RACINE, "gen.py"), spec, "--out", tmp, "--version", "2026-11-22"], capture_output=True, text=True)
        if r.returncode != 0:
            ko[nom + ":gen"] = (r.stdout + r.stderr)[-400:]
            continue
        pdf = [os.path.join(tmp, f) for f in os.listdir(tmp) if f.endswith(".pdf")][0]
        txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
        if txt.count("\f") != 7 or not re.search(r"7\s*/\s*7", txt) or re.search(r"financement|emprunt|Démultiplicatrice", txt, re.I):
            ko[nom + ":pdf"] = "7 pages attendues, pied « /7 », aucun mot de financement"
print("OK" if not ko else f"ÉCART : {ko}")
print(engine.etat_simulateurs(os.path.join(ICI, "SIMULATEUR_VALIDE")))
sys.exit(1 if ko else 0)

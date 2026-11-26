"""Test du réinvestissement des loyers de la SCPI en direct (scpi.reinvestir_loyers = true).
Contrôles : valeurs de patrimoine et de « poche » à 30 ans issues du simulateur projection.html (commit d621fc6, option « Réinvestir les loyers »),
aucun loyer perçu de la SCPI en direct, page 4 en « Loyers réinvestis » (somme investie croissante, effort stable ou en baisse
seulement par le financement), et refus de gen.py si la question n'a pas été posée (champ absent).
Usage : python3 tests/test_reinvestissement.py"""
import copy, json, os, subprocess, sys, tempfile
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..")
sys.path.insert(0, RACINE)
import model

CAS = {
    "client_reinvest_sans_financement_sans_per_exemple.json": dict(total30=469957, scpi30=222747, poche30=190000, loyers_mois30=0),
    "client_reinvest_exemple.json": dict(total30=581000, scpi30=133071, poche30=168763, loyers_mois30=532),
}
ko = {}
for nom, a in CAS.items():
    spec = os.path.join(RACINE, "spec", nom)
    d = model.prepare(json.load(open(spec, encoding="utf-8")), version="22/11/2026")
    s = model.simulate(d, (10, 20, 30))[30]
    obtenu = dict(total30=round(s["total"]), scpi30=round(s["scpi"]), poche30=round(s["poche"]), loyers_mois30=round(s["loyers_mois"]))
    ecarts = {k: (obtenu[k], a[k]) for k in a if obtenu[k] != a[k]}
    if ecarts or not d["reinv"]:
        ko[nom] = ecarts or "reinv attendu"
        continue
    cols = model.evolution_reinv(d)
    tot = [c["total"] for c in cols]
    if not all(tot[i] < tot[i + 1] for i in range(3)) or cols[0]["reinv"] != 0 or any(c["effort"] > cols[0]["effort"] + 0.001 for c in cols):
        ko[nom + ":page4"] = "la somme investie doit croître, sans loyer réinvesti au 1er mois, et l'effort ne doit jamais dépasser celui du 1er mois"
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, os.path.join(RACINE, "gen.py"), spec, "--out", tmp, "--version", "2026-11-22"], capture_output=True, text=True)
        if r.returncode != 0:
            ko[nom + ":gen"] = (r.stdout + r.stderr)[-300:]
            continue
        pdf = [os.path.join(tmp, f) for f in os.listdir(tmp) if f.endswith(".pdf")][0]
        p4 = " ".join(subprocess.run(["pdftotext", "-f", "4", "-l", "4", "-layout", pdf, "-"], capture_output=True, text=True).stdout.split())
        if "Loyers réinvestis (SCPI en direct)" not in p4 or "Loyers perçus" in p4 or "SCPI en financement" in p4 or "investi + " not in p4:
            ko[nom + ":pdf"] = "page 4 : légende « Loyers réinvestis (SCPI en direct) », ni « Loyers perçus » ni SCPI en financement (ses loyers remboursent la banque), « investi + x % »"
# champ absent : gen.py doit refuser
c = json.load(open(os.path.join(RACINE, "spec", "client_exemple.json"), encoding="utf-8"))
del c["scpi"]["reinvestir_loyers"]
with tempfile.TemporaryDirectory() as tmp:
    f = os.path.join(tmp, "c.json"); json.dump(c, open(f, "w", encoding="utf-8"))
    r = subprocess.run([sys.executable, os.path.join(RACINE, "gen.py"), f, "--out", tmp], capture_output=True, text=True)
    if r.returncode == 0 or "reinvestir_loyers" not in (r.stdout + r.stderr):
        ko["champ_absent"] = "gen.py doit refuser un dossier sans scpi.reinvestir_loyers"
print("OK" if not ko else f"ÉCART : {ko}")

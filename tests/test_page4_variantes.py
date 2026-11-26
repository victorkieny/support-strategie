"""Test de la page 4 selon la composition : PER seul (aucune SCPI) → cascade du 1er mois, sans « de plus en plus » ni loyers ;
dès qu'il y a une SCPI (en direct ou financée) → graphique dans le temps (1er mois, 5, 10, 15 ans) avec « de plus en plus avec le temps » ;
ni PER ni SCPI → pas de page 4 (document de 6 pages, pieds « x/6 »).
Usage : python3 tests/test_page4_variantes.py"""
import os, subprocess, sys, tempfile
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..")
CAS = {  # fichier : graphique dans le temps ? (None = pas de page 4)
    "client_av_seule_exemple.json": None,
    "client_per_seul_exemple.json": False,
    "client_exemple.json": True,
    "client_sans_financement_exemple.json": True,
    "client_sans_financement_sans_per_exemple.json": True,
}
ko = {}
for nom, temps in CAS.items():
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, os.path.join(RACINE, "gen.py"), os.path.join(RACINE, "spec", nom), "--out", tmp, "--version", "2026-11-22"], capture_output=True, text=True)
        if r.returncode != 0:
            ko[nom] = (r.stdout + r.stderr)[-300:]
            continue
        pdf = [os.path.join(tmp, f) for f in os.listdir(tmp) if f.endswith(".pdf")][0]
        if temps is None:
            txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
            if txt.count("\f") != 6 or "Ton effort réel" in txt or not all(f"{i}/6" in " ".join(txt.split()).replace(" / ", "/") for i in range(1, 7)):
                ko[nom] = "6 pages attendues, sans page 4, pieds « x/6 »"
            continue
        p4 = subprocess.run(["pdftotext", "-f", "4", "-l", "4", "-layout", pdf, "-"], capture_output=True, text=True).stdout
        flat = " ".join(p4.split())
        a = {"de plus en plus": "de plus en plus avec le temps" in flat, "dans 15 ans": "Dans 15 ans" in flat, "loyers": "Loyers perçus" in flat}
        att = {"de plus en plus": temps, "dans 15 ans": temps, "loyers": temps}
        if a != att:
            ko[nom] = dict(obtenu=a, attendu=att)
print("OK" if not ko else f"ÉCART : {ko}")

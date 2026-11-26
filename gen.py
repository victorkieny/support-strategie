"""Génère le PDF « Stratégie patrimoniale » d'un client : python3 gen.py client.json [--out dossier] [--version AAAA-MM-JJ]
Étapes : contrôles des entrées -> calculs (simulateurs de Victor) -> HTML -> PDF -> contrôles du PDF."""
import argparse, datetime, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TMI_VALIDES = (0, 0.11, 0.30, 0.41, 0.45)       # barème de l'IR : à vérifier chaque année
MOTS_INTERDITS = [r"\bnous\b", r"\bsocle\b", r"\bscénarios?\b", r"\bindépendant", r"\bProdémial"]


def valider(c):
    """Retourne (erreurs, avertissements). Les erreurs bloquent la génération."""
    E, W = [], []
    cl, fi = c["client"], c["financement"]
    if cl["registre"] not in ("tu", "vous", "couple"):
        E.append("registre : tu, vous ou couple")
    if len(cl["prenoms"]) != (2 if cl["registre"] == "couple" else 1):
        E.append("prénoms : 2 pour un couple, 1 sinon")
    try:
        datetime.date.fromisoformat(c["rdv"]["date"])
    except ValueError:
        E.append("rdv.date : format AAAA-MM-JJ")
    if c["rdv"].get("passe") not in ("brouillon", "final"):
        E.append("rdv.passe : brouillon ou final")
    ini = c["av"]["initial"] + c["scpi"]["initial"] + c["per"]["initial"] + (fi.get("apport", 750) if fi["retenu"] else 0)
    if ini != c["situation"]["investir"]:
        E.append(f"AV + SCPI + PER (initiaux)" + (" + apport" if fi["retenu"] else "") + f" = {ini} € ≠ épargne à investir {c['situation']['investir']} €")
    comp = c["situation"].get("composition")
    if not comp:
        E.append("situation.composition requise : patrimoine actuel du client, un poste par ligne (libelle, montant), tel que relevé au R1 ; à demander, jamais à déduire")
    else:
        if not (1 <= len(comp) <= 8) or any(not p.get("libelle") or not p.get("montant", 0) > 0 for p in comp):
            E.append("situation.composition : 1 à 8 postes, chacun avec libelle et montant > 0")
        elif sum(p["montant"] for p in comp) < c["situation"]["precaution"]["montant"] + c["situation"]["investir"]:
            E.append(f"situation.composition ({sum(p['montant'] for p in comp)} €) inférieure à épargne de précaution + épargne à investir ({c['situation']['precaution']['montant'] + c['situation']['investir']} €) : où se trouvent ces sommes ?")
    ori = c["situation"].get("origine")
    if not ori:
        E.append("situation.origine requise : d'où vient l'épargne à investir, poste par poste (libelle identique à la composition, montant) ; à demander, jamais à déduire")
    elif comp:
        lignes = {p["libelle"]: p["montant"] for p in comp if p.get("libelle")}
        if sum(p["montant"] for p in ori) != c["situation"]["investir"]:
            E.append(f"situation.origine : total {sum(p['montant'] for p in ori)} € ≠ épargne à investir {c['situation']['investir']} €")
        for p in ori:
            if p["libelle"] not in lignes:
                E.append(f"situation.origine : « {p['libelle']} » absent de la composition")
            elif p["montant"] > lignes[p["libelle"]]:
                E.append(f"situation.origine : {p['libelle']} {p['montant']} € > montant détenu {lignes[p['libelle']]} €")
    L = c.get("leviers", {})
    has_per = c["per"]["initial"] + c["per"]["mensuel"] > 0
    if (has_per or "tmi" in L) and L.get("tmi") not in TMI_VALIDES:
        E.append(f"TMI {L.get('tmi')} hors barème {TMI_VALIDES}")
    if has_per and "impot_annee" not in L:
        E.append("leviers.impot_annee requis dès qu'il y a un PER")
    if c.get("hypotheses", {}).get("scpi_brut", 0.055) != 0.055:
        E.append("hypotheses.scpi_brut : SCPI en direct = 5,5 % de loyers, imposés à 20 %, valeur fixe (règle de Victor) ; ne pas la surcharger")
    h = c.get("horizons", [10, 20, 30])
    if not (2 <= len(h) <= 3 and list(h) == sorted(set(h))):
        E.append("horizons : 2 ou 3 valeurs strictement croissantes")
    if fi["retenu"]:
        if not (5 <= fi["duree"] <= 25): E.append("financement.duree hors plage du simulateur (5 à 25 ans)")
        if not (10000 <= fi["emprunte"] <= 500000): E.append("financement.emprunte hors plage du simulateur (10 000 à 500 000 €)")
        if not (0.03 <= fi["taux"] <= 0.075): E.append("financement.taux hors plage du simulateur (3 à 7,5 %)")
    eco1 = (c["per"].get("economie_annee1") or (c["per"]["initial"] + 12 * c["per"]["mensuel"]) * L.get("tmi", 0)) if has_per else 0
    if has_per and eco1 > L.get("impot_annee", 0):
        E.append(f"économie d'impôt PER année 1 ({eco1:.0f} €) supérieure à l'impôt prévisionnel ({L.get('impot_annee')} €)")
    if has_per and "economie_annee1" not in c["per"]:
        W.append("économie d'impôt PER = versement × TMI (approximation) ; renseigner per.economie_annee1 si le cas est limite")
    return E, W


def controles_pdf(pdf, d, retenu):
    E, W = [], []
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    attendu = 6 + (1 if retenu else 0) + (1 if d["page_effort"] else 0)     # 6 pages de base + financement + effort réel
    if n != attendu:
        E.append(f"{n} pages au lieu de {attendu}")
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    for mot in MOTS_INTERDITS:
        for m in re.finditer(mot, txt, flags=re.I):
            E.append(f"mot interdit « {m.group(0)} » : …{txt[max(0, m.start()-30):m.end()+30].strip()}…".replace("\n", " "))
    if not d.get("has_per", True):
        for m in re.finditer(r"\bPER\b", txt):
            E.append("« PER » présent alors que le dossier est sans PER : …" + txt[max(0, m.start()-30):m.end()+30].strip().replace("\n", " ") + "…")
    for m in re.finditer(r"cr[ée]dit", txt, flags=re.I):
        ctx = txt[max(0, m.start()-25):m.end()+25].replace("\n", " ")
        if "opération de crédit" not in ctx:
            W.append(f"« crédit » : …{ctx.strip()}…")
    if not retenu:
        for m in re.finditer(r"financement|Démultiplicatrice|emprunt", txt, flags=re.I):
            E.append("mention du financement alors qu'il n'est pas retenu (objectif du client à reformuler ?) : …" + txt[max(0, m.start()-30):m.end()+30].strip().replace("\n", " ") + "…")
    if retenu and d["fin"]["duree"] < 15:
        W.append(f"financement de {d['fin']['duree']} ans : page 4, la participation au financement disparaît avant l'horizon de 15 ans, à relire")
    if retenu and d["fin"]["annee_limite"] < d["fin"]["duree"]:
        W.append(f"autofinancement atteint en année {d['fin']['annee_limite']} (avant le terme {d['fin']['duree']}) : page 6 à relire")
    return E, W


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("client"); ap.add_argument("--out", default=os.path.join(HERE, "out")); ap.add_argument("--version")
    a = ap.parse_args()
    c = json.load(open(a.client, encoding="utf-8"))
    E, W = valider(c)
    if c["client"]["registre"] != "tu":
        E.append("la version « vous » / « couple » du texte n'existe pas encore : génération refusée plutôt que de produire un texte au tutoiement")
    for w in W: print("  ! " + w)
    if E:
        print("ÉCHEC — corriger avant génération :"); [print("  ✗ " + e) for e in E]; sys.exit(1)
    sys.path.insert(0, HERE)
    import model, build
    v = datetime.date.fromisoformat(a.version).strftime("%d/%m/%Y") if a.version else None
    d = model.prepare(c, version=v)
    os.makedirs(a.out, exist_ok=True)
    html = build.build(d, os.path.join(HERE, "out", "maquette.html"))
    subprocess.run([sys.executable, os.path.join(HERE, "render.py")], check=True, capture_output=True)
    nom = re.sub(r"[^A-Za-z0-9]+", "_", c["client"]["nom"]).strip("_")
    pdf = os.path.join(a.out, f"Strategie_patrimoniale_{nom}_{c['rdv']['passe']}_{c['rdv']['date']}.pdf")
    os.replace(os.path.join(HERE, "out", "Strategie_patrimoniale_maquette.pdf"), pdf)
    E2, W2 = controles_pdf(pdf, d, c["financement"]["retenu"])
    for w in W2: print("  ! " + w)
    if E2:
        print("ÉCHEC contrôles PDF :"); [print("  ✗ " + e) for e in E2]; sys.exit(1)
    print("OK  " + pdf)


if __name__ == "__main__":
    main()

"""Moteur financement : appelle le JavaScript du simulateur de Victor (source de vérité) via Node."""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.environ.get("SIMULATEUR_DEPOT", "/home/claude/victorkieny/site-internet")
HTML = os.environ.get("SIMULATEUR_HTML", os.path.join(DEPOT, "simulateurs", "une-pierre-deux-coups.html"))
HTML_PROJ = os.environ.get("PROJECTION_HTML", os.path.join(DEPOT, "simulateurs", "projection.html"))


def ensure_simulateur():
    if not os.path.exists(HTML):
        os.makedirs(os.path.dirname(DEPOT), exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/victorkieny/site-internet", DEPOT],
                       check=True, env={**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"})
    return HTML


def params_simulateur(fin, hyp):
    return {
        "montantEmprunte": fin["emprunte"], "dureeCredit": fin["duree"],
        "tauxInteretPct": round(fin["taux"] * 100, 6), "tauxAssurancePct": round(fin["assurance"] * 100, 6),
        "rendementCreditPct": round(fin["loyers_taux_simu"] * 100, 6),
        "revalorisationPartsPct": round(hyp["scpi_reval"] * 100, 6),
        "rendementComptantPct": round(hyp["scpi_brut"] * 100, 6),
        "tauxEffectifEstimePct": round(hyp["fiscalite_comptant"] * 100, 6),
    }


def run_financement(fin, hyp, horizon=30):
    p = subprocess.run(["node", os.path.join(HERE, "engine_fin.js"), ensure_simulateur()],
                       input=json.dumps({**params_simulateur(fin, hyp), "horizonAnnees": max(30, horizon)}), capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("Moteur financement en échec : " + (p.stderr.strip() or "erreur inconnue"))
    return json.loads(p.stdout)


def run_projection(d, horizon):
    """Capital AV, PER et SCPI en direct, année par année, via projection.html (JavaScript tel quel)."""
    ensure_simulateur()
    h = d["hyp"]
    q = {
        "av": {"capitalInitial": d["av"]["initial"], "versementMensuel": d["av"]["mensuel"],
               "rendement": round(h["taux_av_per"] * 100, 6), "dureeTotale": horizon},
        "per": {"capitalInitial": d["per"]["initial"], "versementMensuel": d["per"]["mensuel"],
                "rendement": round(h["taux_av_per"] * 100, 6), "dureeTotale": horizon},
        "scpi": {"rendement": round(h["scpi_brut"] * 100, 6), "versementInitial": d["scpi"]["initial"],
                 "versementMensuel": d["scpi"]["mensuel"], "dureeVersements": horizon, "dureeTotale": horizon,
                 "revalorisationPartsPct": round(h["scpi_reval"] * 100, 6), "reinvestir": bool(d.get("reinv")), "tmi": 30,
                 "fiscaliteEuropeenne": True, "tauxEffectifReinvestissement": round(h["fiscalite_comptant"] * 100, 6)},
    }
    p = subprocess.run(["node", os.path.join(HERE, "engine_proj.js"), HTML_PROJ],
                       input=json.dumps(q), capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("Moteur projection en échec : " + (p.stderr.strip() or "erreur inconnue"))
    return json.loads(p.stdout)


def etat_simulateurs(fichier_valide):
    """Compare le commit des simulateurs utilisés à celui sur lequel les tests ont été recalés (diagnostic d'un écart)."""
    ensure_simulateur()
    actuel = subprocess.run(["git", "-C", DEPOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    valide = open(fichier_valide).read().strip()
    return (f"simulateurs @ {actuel} (commit de référence des tests : {valide})" if actuel == valide
            else f"simulateurs @ {actuel} ≠ commit de référence {valide} : le simulateur a changé depuis le dernier recalage des tests")

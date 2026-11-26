"""Modèle du support « Stratégie patrimoniale » : données client (JSON) -> données de génération.
Les calculs viennent des simulateurs de Victor (JavaScript exécuté tel quel, cf. engine.py)."""
import datetime, json, os

from engine import run_financement

MOIS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
HYP_DEFAUT = {"taux_av_per": 0.055, "scpi_brut": 0.055, "fiscalite_comptant": 0.20, "scpi_reval": 0.005, "loyers_taux_simu": 0.055}
APPORT_DEFAUT = 750


def prepare(c, version=None):
    """Transforme les entrées d'un client (cf. spec/client_exemple.json) en données prêtes pour build.py."""
    y, m, j = (int(x) for x in c["rdv"]["date"].split("-"))
    fi = c["financement"]
    per = {k: v for k, v in c["per"].items() if k != "economie_annee1"}
    eco1 = c["per"].get("economie_annee1")       # économie d'impôt réelle année 1 (simulateur PER), sinon versement × TMI
    per["taux_eco"] = eco1 / (per["initial"] + 12 * per["mensuel"]) if eco1 else c.get("leviers", {}).get("tmi", 0)
    h = {**HYP_DEFAUT, **c.get("hypotheses", {})}
    d = {
        "client": {"prenom": " et ".join(c["client"]["prenoms"]), "nom": c["client"]["nom"], "registre": c["client"]["registre"]},
        "date_rdv": f"{j} {MOIS_FR[m - 1]} {y}",
        "passe": c["rdv"].get("passe", "brouillon"),
        "fictif": c.get("fictif", False),                     # exemples et tests uniquement
        "version": version or datetime.date.today().strftime("%d/%m/%Y"),
        "situation": {"precaution": c["situation"]["precaution"], "investir": {"montant": c["situation"]["investir"]}, "composition": c["situation"].get("composition", []), "origine": c["situation"].get("origine", [])},
        "objectifs": c["objectifs"],
        "financement": fi["retenu"],
        "docs_fournis": c.get("docs_fournis", []),
        "logement": {"statut": fi.get("logement", "locataire"), "par": fi.get("heberge_par", "la personne qui t’héberge")},   # locataire | heberge
        "pertinence": fi.get("pertinence", {}),
        "horizons": tuple(c.get("horizons", (10, 20, 30))),
        "leviers": c.get("leviers", {}),
        "has_per": (per["initial"] + per["mensuel"]) > 0,      # sans PER : 3 enveloppes (pas de colonne, de page ni de mention PER)
        "av": c["av"], "scpi": c["scpi"], "per": per,
        "fin": ({"apport": fi.get("apport", APPORT_DEFAUT), "emprunte": fi["emprunte"], "duree": fi["duree"],
                 "taux": fi["taux"], "assurance": fi.get("assurance", 0.0), "loyers_taux_simu": h["loyers_taux_simu"]}
                if fi["retenu"] else None),             # sans financement : None (jamais des zéros, un oubli doit planter)
        "hyp": {"taux_av_per": h["taux_av_per"], "scpi_brut": h["scpi_brut"],
                "fiscalite_comptant": h["fiscalite_comptant"], "scpi_reval": h["scpi_reval"]},
    }
    d["hyp"]["scpi_distribution"] = h["scpi_brut"] * (1 - h["fiscalite_comptant"])   # part perçue après impôt
    # page 4 (effort réel) : n'existe que s'il y a un PER (économie d'impôt) ou une SCPI (loyers, en direct ou financée)
    d["has_sd"] = (c["scpi"]["initial"] + c["scpi"]["mensuel"]) > 0         # SCPI en direct (sinon : aucune mention de la SCPI en direct)
    # loyers de la SCPI en direct réinvestis (choix du client, demandé avant chaque dossier) : jamais de valeur par défaut, cf. gen.py
    d["reinv"] = bool(c["scpi"].get("reinvestir_loyers")) and d["has_sd"]
    d["page_effort"] = d["has_per"] or d["has_sd"] or fi["retenu"]
    f = d["fin"]
    if f is None:                                             # variante sans financement : aucun calcul de financement
        return d
    r = run_financement(f, d["hyp"], max(d["horizons"]))      # simulateur de Victor (JavaScript, tel quel)
    f["mensualite_exacte"] = r["mensualite"]
    f["mensualite"] = round(r["mensualite"])                  # mensualité affichée (assurance comprise)
    f["mensualite_pret"] = r["mensualite_pret"]               # hors assurance (amortissement du capital)
    f["loyers"] = round(r["loyer_mois1"])                     # loyer mensuel brut de la SCPI financée, année 1
    f["effort"] = round(r["effort_m1"])                       # effort réel du 1er mois (diminue ensuite)
    f["effort_fin"] = round(r["effort_fin"])
    f["annee_limite"] = r["annee_limite"]                     # année de comparaison (autofinancement, sinon fin du financement)
    f["annee_autofinancement"] = r["annee_autofinancement"]
    f["effort_total"] = round(r["effort_total"])
    f["patrimoine_avec"] = round(r["avec"])
    f["parts_sans"] = round(r["capital_sans"])
    f["loyers_sans"] = round(r["loyers_sans"])
    f["patrimoine_sans"] = round(r["sans"])                   # parts + loyers perçus cumulés (non réinvestis)
    f["levier"] = f["patrimoine_avec"] - f["patrimoine_sans"]   # le simulateur affiche 1 € de moins (arrondi)
    f["levier_pct"] = round(r["levier_pct"])
    return d


_EXEMPLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec", "client_exemple.json")
DATA = prepare(json.load(open(_EXEMPLE, encoding="utf-8")), version="19/11/2026") if os.path.exists(_EXEMPLE) else None


def eur(x, dec=0):
    s = f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s + " €"


def num(x):
    return f"{x:,.0f}".replace(",", " ")


def simulate(d, horizons=(10, 20, 30)):
    """Projection année par année. AV, PER, SCPI en direct et financement viennent des simulateurs de Victor
    (projection.html et une-pierre-deux-coups.html, exécutés tels quels) ; le modèle ne fait que les assembler."""
    from engine import run_projection
    H = max(horizons)
    proj = run_projection(d, H)
    fin = d["fin"]
    rf = run_financement(fin, d["hyp"], H)["annees"] if fin else None
    fisc = d["hyp"]["fiscalite_comptant"]
    tmi = d["leviers"].get("tmi", 0)
    prog = d["av"]["mensuel"] + d["scpi"]["mensuel"] + d["per"]["mensuel"]
    invest0 = d["situation"]["investir"]["montant"]
    loy_dir = loy_fin = 0.0
    out, series = {}, {}
    for y in range(1, H + 1):
        a, p, s = proj["av"][y - 1], proj["per"][y - 1], proj["scpi"][y - 1]
        f = rf[y - 1] if fin else {"loyer": 0.0, "valeur": 0.0, "crd": 0.0, "loyer_mois": 0.0}   # sans financement : rien
        loy_fin += f["loyer"]
        # déjà nets de fiscalité dans projection.html (fiscaliteEuropeenne, taux effectif). Loyers réinvestis (reinvestir) : ils sont
        # dans le capital de la SCPI (le simulateur les y ajoute) et ne sont pas perçus : rien à déduire de la poche du client.
        loy_dir = 0.0 if d["reinv"] else s["revenusCumules"]
        versé = invest0 + 12 * y * prog + (12 * fin["mensualite_exacte"] * min(y, fin["duree"]) if fin else 0)
        impot = (d["per"]["initial"] + 12 * y * d["per"]["mensuel"]) * d["per"]["taux_eco"]
        total = a["capital"] + p["capital"] + s["capital"] + f["valeur"] - f["crd"]
        rec = {
            "av": a["capital"], "per": p["capital"], "scpi": s["capital"], "fin": f["valeur"] - f["crd"], "total": total,
            "versé": versé, "impot": impot, "loyers": loy_dir + loy_fin,
            "poche": versé - impot - loy_dir - loy_fin,
            "loyers_mois": (0.0 if d["reinv"] else s["revenuMensuel"]) + f["loyer_mois"],      # loyers perçus (hors réinvestis)
            "loy_dir_mois": 0.0 if d["reinv"] else s["revenuMensuel"],   # loyers mensuels perçus nets de la seule SCPI en direct (page 4)
            "reinv_mois": s["revenuMensuel"] if d["reinv"] else 0.0,     # loyers mensuels réinvestis (équivalent mensuel d'un réinvestissement annuel)
            "loy_fin_mois": f["loyer_mois"],             # loyer mensuel de la SCPI en financement (page 4)
        }
        series[y] = rec
        if y in horizons:
            out[y] = rec
    out["series"] = series
    return out


def vases(d):
    """Cascade mensuelle (1er mois) : versements programmés + participation au financement,
    moins économie PER et loyers SCPI en direct perçus."""
    prog_av, prog_sc, prog_per = d["av"]["mensuel"], d["scpi"]["mensuel"], d["per"]["mensuel"]
    part = d["fin"]["effort"] if d["fin"] else 0    # participation mensuelle au financement (0 sans financement)
    eco = prog_per * d["per"]["taux_eco"]
    loy_dir = 0.0 if d["reinv"] else d["scpi"]["initial"] * d["hyp"]["scpi_distribution"] / 12     # loyers perçus au 1er mois (réinvestis : aucun)
    brut = prog_av + prog_sc + prog_per + part
    reel = brut - eco - loy_dir
    return dict(av=prog_av, sc=prog_sc, per=prog_per, part=part, eco=eco,
                loy_dir=loy_dir, brut=brut, reel=reel, prog=prog_av + prog_sc + prog_per)


HORIZONS_EFFORT = (5, 10, 15)    # page 4 : 1er mois, puis dans 5, 10 et 15 ans (indépendant des horizons de la page 5)


def evolution(d):
    """Page 4 : ce que financent chaque mois l'économie d'impôt du PER et les loyers des SCPI, au 1er mois puis à chaque horizon.
    Le versement programmé (brut) est celui du 1er mois (participation au financement comprise, nette des loyers de la SCPI
    financée). Les loyers qui s'y ajoutent ensuite viennent des simulateurs : SCPI en direct (versements mensuels et
    revalorisation des parts déjà acquises) et progression du loyer de la SCPI financée (revalorisation), qui réduit la
    participation au financement. L'économie d'impôt du PER est gardée constante (tranche constante)."""
    v = vases(d)
    sim = simulate(d, HORIZONS_EFFORT)
    l1_fin = sim["series"][1]["loy_fin_mois"]
    plafond = v["brut"] - v["eco"]
    pts = [("Au 1er mois", v["loy_dir"])]
    for h in HORIZONS_EFFORT:
        r = sim[h]
        gain_fin = 0.0
        if d["fin"]:
            # financement terminé avant l'horizon : la participation disparaît ; sinon elle baisse avec le loyer de la SCPI financée
            gain_fin = v["part"] if h > d["fin"]["duree"] else r["loy_fin_mois"] - l1_fin
        pts.append((f"Dans {h} ans", r["loy_dir_mois"] + gain_fin))
    cols = []
    for lab, loy in pts:
        loy = min(max(loy, 0.0), plafond)
        cols.append(dict(label=lab, loy=loy, eco=v["eco"], reel=plafond - loy, brut=v["brut"]))
    return cols


if __name__ == "__main__":
    import json
    s = simulate(DATA)
    for y, v in [(k, x) for k, x in s.items() if k != "series"]:
        print(y, {k: round(x) for k, x in v.items()})
    print({k: round(v, 1) for k, v in vases(DATA).items()})


def evolution_reinv(d):
    """Page 4, loyers de la SCPI en direct réinvestis : la quantité investie par mois augmente, l'effort réel reste le même.
    Colonnes : effort réel (bas, constant), économie d'impôt du PER, loyers réinvestis de la SCPI en direct (haut, croissants).
    Les loyers de la SCPI financée ne figurent pas et ne modifient pas l'effort affiché : ils remboursent la banque, ils ne sont pas
    investis (décision du 26/11/2026 ; l'effort est donc légèrement surévalué pour un client avec financement, la baisse figure
    page 6). Seule la fin du financement retire la participation au financement (horizon > durée).
    Au 1er mois aucun loyer n'est encore réinvesti (délai de jouissance).
    Les loyers réinvestis viennent du simulateur (projection.html, reinvestir) : réinvestis une fois par an dans le simulateur,
    affichés ici en équivalent mensuel."""
    v = vases(d)
    sim = simulate(d, HORIZONS_EFFORT)
    base_effort = v["brut"] - v["eco"]
    cols = [dict(label="Au 1er mois", effort=base_effort, eco=v["eco"], reinv=0.0)]
    for h in HORIZONS_EFFORT:
        r = sim[h]
        part_h = 0.0 if (d["fin"] and h > d["fin"]["duree"]) else v["part"]   # financement terminé : plus de participation
        effort = max(v["brut"] - v["part"] + part_h - v["eco"], 0.0)
        cols.append(dict(label=f"Dans {h} ans", effort=effort, eco=v["eco"], reinv=r["reinv_mois"]))
    for c in cols:
        c["total"] = c["effort"] + c["eco"] + c["reinv"]
    return cols

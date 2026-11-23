"""Maquette — document « Stratégie patrimoniale » (HTML -> PDF). Données fictives, charte des slides de Victor."""
import sys
from model import DATA, eur, num, simulate, vases

C = dict(bg="#2a251f", card="#332d26", card2="#3b352d", line="#4a4339", text="#f1eee7", muted="#8e8a83",
         gold="#b49868", tan="#c3af8d", blue="#758aa4", prec="#9aa3ad", sage="#86a08a", lev="#5b9a6b")

CSS = """
@font-face{font-family:'Bodoni Moda';font-weight:400;src:url('fonts/bodoni-moda-latin-400-normal.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-weight:500;src:url('fonts/bodoni-moda-latin-500-normal.woff2') format('woff2');}
@font-face{font-family:'Bodoni Moda';font-weight:600;src:url('fonts/bodoni-moda-latin-600-normal.woff2') format('woff2');}
@font-face{font-family:'Inter';font-weight:400;src:url('fonts/Inter-Regular.otf') format('opentype');}
@font-face{font-family:'Inter';font-weight:500;src:url('fonts/Inter-Medium.otf') format('opentype');}
@font-face{font-family:'Inter';font-weight:600;src:url('fonts/Inter-SemiBold.otf') format('opentype');}
@font-face{font-family:'Inter';font-weight:700;src:url('fonts/Inter-Bold.otf') format('opentype');}
@page{size:794px 1123px;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#2a251f;--card:#332d26;--card2:#3b352d;--line:#4a4339;--text:#f1eee7;--muted:#8e8a83;--gold:#b49868;--tan:#c3af8d;--blue:#758aa4;--prec:#9aa3ad;--sage:#86a08a;--lev:#5b9a6b}
html,body{background:var(--bg)}
body{font-family:'Inter',sans-serif;color:var(--text);-webkit-font-smoothing:antialiased}
.page{width:794px;height:1123px;position:relative;background:var(--bg);overflow:hidden;page-break-after:always;break-after:page}
.hdr{position:absolute;top:30px;left:48px;right:48px;height:52px;display:flex;align-items:center;border-bottom:1px solid var(--line)}
.hdr img{height:40px;margin-right:18px}
.hdr .sep{width:1px;height:26px;background:var(--line);margin-right:20px}
.nav{display:flex;gap:22px;flex:1}
.nav span{font-size:8.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:600}
.nav span b{font-family:'Bodoni Moda',serif;font-weight:400;font-size:13px;letter-spacing:0;color:var(--muted);margin-right:6px}
.nav span.on{color:var(--text)}
.nav span.on b{color:var(--gold)}
.who{font-size:11px;color:var(--gold)}
.main{position:absolute;top:104px;left:48px;right:48px;bottom:64px}
.ftr{position:absolute;bottom:26px;left:48px;right:48px;display:flex;justify-content:space-between;align-items:center;font-size:8px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.ftr .mq{border:1px solid var(--gold);color:var(--gold);padding:2px 8px;border-radius:10px}
.eyebrow{font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);font-weight:600}
h1{font-family:'Bodoni Moda',serif;font-weight:400;font-size:54px;line-height:1.04;margin:14px 0 16px}
h2{font-family:'Bodoni Moda',serif;font-weight:400;font-size:29px;line-height:1.12;margin:8px 0 8px}
.lead{font-size:13.5px;line-height:1.5;color:rgba(241,238,231,.74)}
.rule{width:56px;height:2px;background:var(--gold);margin:12px 0 0}
p,li{font-size:11px;line-height:1.52;color:rgba(241,238,231,.8)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:15px 17px}
.card.top{border-top:3px solid var(--c,var(--gold))}
.pill{display:inline-block;font-size:8px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;padding:3px 9px;border-radius:10px;color:#2a251f;background:var(--c,var(--gold))}
.big{font-family:'Bodoni Moda',serif;font-size:31px;line-height:1;color:var(--text)}
.big small{font-family:'Inter',sans-serif;font-size:11px;color:var(--muted);margin-left:3px}
.lbl{font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:600}
.sec{display:flex;align-items:baseline;gap:10px;margin:0 0 9px}
.sec .n{font-family:'Bodoni Moda',serif;font-size:17px;color:var(--gold)}
.sec .t{font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;color:var(--text)}
.sbar{display:flex;gap:3px;height:15px;margin:2px 0 11px}
.sbar div{border-radius:8px}
.cols3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.cols4{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:11px}
.darrow{display:flex;align-items:center;justify-content:center;gap:10px;height:62px}
.darrow span{font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);font-weight:600}
.obj{display:grid;grid-template-columns:1fr 1fr;gap:12px 30px}
.obj li{list-style:none;padding:13px 16px 13px 28px;position:relative;font-size:13px;color:var(--text);background:var(--card);border:1px solid var(--line);border-radius:12px}
.obj li:before{content:'';position:absolute;left:13px;top:19px;width:5px;height:5px;border-radius:50%;background:var(--gold)}
.nb{position:absolute;border-radius:13px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:6px 8px}
.nb .a{font-family:'Bodoni Moda',serif;font-size:22px;line-height:1.05}
.nb .b{font-size:9px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;margin-top:4px}
.nb .c{font-size:9.5px;margin-top:3px;opacity:.9}
table{border-collapse:collapse;width:100%}
th{font-size:8px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600;text-align:right;padding:6px 8px;border-bottom:1px solid var(--line)}
th:first-child,td:first-child{text-align:left}
td{font-size:11px;padding:7px 8px;border-bottom:1px solid rgba(74,67,57,.6);text-align:right;color:rgba(241,238,231,.88)}
tr.tot td{font-weight:700;color:var(--text);background:rgba(180,152,104,.12);border-bottom:none}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin:0 2px;background:var(--c)}
.dot.o{background:transparent;border:1.4px solid var(--line)}
.dc{width:9px;height:9px;border-radius:50%;display:inline-block;margin-right:7px;vertical-align:middle}
.lim{font-size:9.5px;line-height:1.4;color:var(--muted);border-top:1px solid var(--line);padding-top:7px;margin-top:9px}
.lim b{color:var(--tan);font-weight:600}
.banner{background:#1f1b16;border:1px solid var(--line);border-radius:14px;padding:16px 22px;display:flex;justify-content:space-between;align-items:center}
.banner .k{font-size:10.5px;color:var(--muted)}
.banner .v{font-family:'Bodoni Moda',serif;font-size:30px}
.note{font-size:9px;line-height:1.45;color:var(--muted)}
.todo{color:var(--gold);font-style:italic}
"""

LOGO = "assets/logo_vk_placeholder.png"
NAV = ["Constat", "Stratégie", "Projection", "Mise en place"]


def shell(idx, nav_on, inner, d, total=None):
    total = total or (8 if d.get("financement") else 7)     # sans financement : la page 6 n'existe pas
    nav = "".join(f'<span class="{"on" if i == nav_on else ""}"><b>0{i+1}</b>{n}</span>' for i, n in enumerate(NAV))
    # pastille centrale du pied de page : données fictives (exemples) > « Brouillon » > rien (version finale)
    mq = "Maquette · données fictives" if d.get("fictif") else ("Brouillon" if d.get("passe") == "brouillon" else "")
    mq_html = f'<span class="mq">{mq}</span>' if mq else "<span></span>"
    return f"""
<section class="page">
  <div class="hdr"><img src="{LOGO}"><div class="sep"></div><div class="nav">{nav}</div><div class="who">{d['client']['nom']}</div></div>
  <div class="main">{inner}</div>
  <div class="ftr"><span>Victor Kieny</span>{mq_html}<span>Version du {d['version']} · {idx}/{total}</span></div>
</section>"""


def arrow_down(label=""):
    return f"""<div class="darrow"><svg width="22" height="30" viewBox="0 0 22 30"><path d="M11 0 V22" stroke="{C['gold']}" stroke-width="1.6" fill="none"/><path d="M4 17 L11 26 L18 17" stroke="{C['gold']}" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg><span>{label}</span></div>"""


# ------------------------------------------------------------------ page 1
def page1(d):
    s = d["situation"]
    prec = s["precaution"]["montant"]
    inv = s["investir"]["montant"]
    tot = prec + inv
    # composition actuelle du patrimoine, telle que relevée (un poste = un libellé et un montant), dans l'ordre fourni
    comp = s["composition"]
    pal = ["#b49868", "#c3af8d", "#758aa4", "#9eb2c8", "#86a08a", "#9aa3ad", "#a98f8a", "#7e8f7f"]
    tot_c = sum(p["montant"] for p in comp)
    brut = [p["montant"] * 1000 / tot_c for p in comp]   # pourcentages au dixième, arrondis au plus fort reste : somme = 100,0
    pcts = [int(x) for x in brut]
    for i in sorted(range(len(comp)), key=lambda i: brut[i] - pcts[i], reverse=True)[:1000 - sum(pcts)]:
        pcts[i] += 1
    bar = "".join(f'<div style="flex:{p["montant"]};background:{pal[i]}"></div>' for i, p in enumerate(comp))
    def poste(i, p):
        note = f" · {p['note']}" if p.get("note") else ""
        return (f'<div><div style="height:2px;background:{pal[i]};margin-bottom:10px"></div>'
                f'<div style="font-size:12.5px">{p["libelle"]}</div>'
                f'<div class="big" style="font-size:24px;margin:5px 0 4px">{eur(p["montant"])}</div>'
                f'<div style="font-size:8.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600">{("%.1f" % (pcts[i] / 10)).replace(".", ",")}&nbsp;%{note}</div></div>')
    corps = f'<div style="display:grid;grid-template-columns:repeat({min(len(comp), 4)},1fr);gap:18px 18px">{"".join(poste(i, p) for i, p in enumerate(comp))}</div>'
    prog = d["av"]["mensuel"] + d["scpi"]["mensuel"] + d["per"]["mensuel"]
    def col(c, t, m, sub):
        return f'<div><div style="height:2px;background:{c};margin-bottom:10px"></div><div class="lbl" style="color:{c}">{t}</div><div class="big" style="font-size:30px;margin:8px 0 6px">{eur(m)}</div><p style="font-size:10.5px;color:var(--muted)">{sub}</p></div>'
    def lev(c, t, big, sub):
        return f'<div class="card top" style="--c:{c};padding:20px 14px 18px"><div class="lbl" style="white-space:nowrap;letter-spacing:.1em">{t}</div><div class="big" style="margin:22px 0 10px;font-size:29px">{big}</div><p style="font-size:9.5px;color:var(--muted)">{sub}</p></div>'
    L = d["leviers"]
    hp = d.get("has_per", True)
    hf = bool(d.get("financement"))
    imp_lev = lev(C['blue'], 'Impôt sur le revenu', eur(L['impot_annee']), f"L’impôt que tu devrais payer en {L['annee_impot']}. L’objectif : en rediriger une partie vers ta poche, au service de tes propres intérêts.") if hp else ""
    n_lev = 2 + (1 if hp else 0) + (1 if hf else 0)       # versement initial, versement mensuel, + impôt (PER), + capacité de financement
    ini = d['av']['initial'] + d['scpi']['initial'] + d['per']['initial'] + (d['fin']['apport'] if hf else 0)
    mens = prog + (d['fin']['effort'] if hf else 0)
    ori = [f"{p['libelle']}&nbsp;({eur(p['montant'])})" for p in s["origine"]]
    ori_txt = ori[0] if len(ori) == 1 else ", ".join(ori[:-1]) + " et " + ori[-1]
    ini_sub = f"Ce que tu peux investir dès le départ, prélevé sur {ori_txt}.<br><span style='color:var(--text)'>Il te reste {eur(prec)} d’épargne de précaution, disponible.</span>"
    mens_sub = f"Investi chaque mois de façon automatique, dont {num(d['fin']['effort'])}&nbsp;€ pour le financement." if hf else "Investi chaque mois de façon automatique."
    cap_lev = (lev(C['lev'], 'Capacité de financement', '<span style="position:relative;display:inline-block"><span style="position:absolute;top:-11px;left:1px;font-size:10px;letter-spacing:.04em;font-family:Inter,sans-serif;color:var(--text)">jusqu’à</span>' + eur(L['capacite_mensualite']) + '<span style="font-size:14px;letter-spacing:.02em">/mois</span></span>', 'Jusqu’où tu peux aller chaque mois. À toi de choisir, dans la limite de cette mensualité, ce que tu consacres au levier du financement.')) if hf else ""
    inner = f"""
<div class="eyebrow">Stratégie patrimoniale</div>
<h1 data-fit style="font-size:41px;white-space:nowrap">{d['client']['prenom']}&nbsp;: ce que tu as, ce que tu veux,<br>et comment y arriver.</h1>
<p class="lead">Ce qui a été défini lors de notre rendez-vous du {d['date_rdv']}, et ce que cela donne dans le temps.</p>
<div class="rule"></div>

<div style="margin-top:34px">
  <div class="sec"><span class="n">01</span><span class="t">Situation initiale</span></div>
  <div class="card" style="padding:24px 22px 22px">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px"><span class="lbl">Composition actuelle de ton patrimoine</span><span class="big" style="font-size:22px">{eur(tot_c)}</span></div>
    <div class="sbar" style="height:20px;margin-bottom:16px">{bar}</div>
    {corps}
  </div>
</div>

{arrow_down('ce que tu veux atteindre')}

<div>
  <div class="sec"><span class="n">02</span><span class="t">Objectifs</span></div>
  <ul class="obj">{''.join(f'<li>{o}</li>' for o in d['objectifs'])}</ul>
</div>

{arrow_down('les leviers pour y arriver')}

<div>
  <div class="sec"><span class="n">03</span><span class="t">Les {n_lev} leviers</span></div>
  <div class="cols4" style="{'' if n_lev == 4 else 'grid-template-columns:' + ' '.join(['1fr'] * n_lev)}">
    {lev(C['gold'], 'Versement initial', eur(ini), ini_sub)}
    {lev(C['sage'], 'Versement mensuel', eur(mens) + '<span style="font-size:14px;letter-spacing:.02em">/mois</span>', mens_sub)}
    {imp_lev}
    {cap_lev}
  </div>
</div>
"""
    return shell(1, 0, inner, d)


# ------------------------------------------------------------------ page 2
def page2(d):
    s = d["situation"]
    prec, inv = s["precaution"]["montant"], s["investir"]["montant"]
    lab = s["precaution"]["label"]
    hp = d.get("has_per", True)
    hf = bool(d.get("financement"))
    n_env0 = 2 + (1 if hp else 0) + (1 if hf else 0)
    env_txt = {2: "Deux enveloppes, deux rôles", 3: "Trois enveloppes, trois rôles", 4: "Quatre enveloppes, quatre rôles"}[n_env0]
    tot = prec + inv
    W = 698
    cl, cr = 175, 523          # centres des deux blocs (épargne de précaution / épargne à investir)
    boxes = f"""
<div class="nb" style="left:249px;top:0;width:200px;height:68px;background:var(--text);color:#2a251f"><div class="a" style="font-size:23px">{eur(tot)}</div><div class="c" style="font-size:9px;letter-spacing:.14em;text-transform:uppercase;font-weight:600">ton épargne</div></div>
<div class="nb" style="left:{cl-135}px;top:150px;width:270px;height:96px;background:var(--card);border:1.5px solid {C['prec']}"><div class="a" style="color:{C['prec']}">{eur(prec)}</div><div class="b" style="color:{C['prec']}">Épargne de précaution</div><div class="c">{lab}, pour les imprévus, vacances et envies à court terme</div></div>
<div class="nb" style="left:{cr-135}px;top:150px;width:270px;height:96px;background:rgba(180,152,104,.16);border:1.5px solid {C['gold']}"><div class="a" style="color:{C['gold']}">{eur(inv)}</div><div class="b" style="color:{C['gold']}">Épargne à investir</div><div class="c">{env_txt}</div></div>
"""
    items = [
        (C["gold"], "Capitalisante", "Assurance-vie", eur(d["av"]["initial"]), "reste disponible"),
        (C["sage"], "Distribuante", "SCPI en direct", eur(d["scpi"]["initial"]), "verse des loyers"),
    ]
    if hp:
        items.append((C["blue"], "Économie d’impôt", "PER", eur(d["per"]["initial"]), "réduit ton impôt"))
    if hf:
        items.append((C["lev"], "Démultiplicatrice", "SCPI en financement", f"{eur(d['fin']['apport'])} d’apport", f"{eur(d['fin']['emprunte'])} financés"))
    n_env = len(items)
    bw = 160 if n_env == 4 else (190 if n_env == 3 else 220)
    gap = (W - n_env * bw) / (n_env - 1)
    xs = [i * (bw + gap) for i in range(n_env)]
    # titre : accord selon le nombre de fondations (2 premières enveloppes) et de leviers (les suivantes) actifs
    nf, nl = 2, n_env - 2
    parts_t = ["une épargne de précaution"]
    if nf: parts_t.append("des fondations" if nf > 1 else "une fondation")
    if nl: parts_t.append("des leviers" if nl > 1 else "un levier")
    titre = (", ".join(parts_t[:-1]) + " et " + parts_t[-1] if len(parts_t) > 1 else parts_t[0])
    titre = titre[0].upper() + titre[1:] + "."
    row3 = ""
    for x, (col, tag, name, amt, sub) in zip(xs, items):
        row3 += f"""<div class="nb" style="left:{x:.1f}px;top:360px;width:{bw}px;height:140px;background:rgba({int(col[1:3],16)},{int(col[3:5],16)},{int(col[5:7],16)},.16);border:1.5px solid {col};justify-content:flex-start;padding-top:34px">
<div class="b" style="color:{col};margin:0 0 8px;line-height:1.3;height:12px">{tag}</div><div style="font-size:12.5px;font-weight:600;height:16px">{name}</div><div class="a" style="color:{col};margin-top:7px;font-size:19px;height:24px;line-height:24px;white-space:nowrap">{amt}</div><div class="c" style="color:var(--muted);margin-top:4px">{sub}</div></div>"""
    ar = f'<svg style="position:absolute;left:0;top:0" width="{W}" height="560" viewBox="0 0 {W} 560"><defs><marker id="ah2" markerWidth="9" markerHeight="9" refX="6" refY="4.5" orient="auto"><path d="M1 1 L7 4.5 L1 8" fill="none" stroke="{C["gold"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
    for tx in (cl, cr):
        ar += f'<path d="M349 68 C349 108 {tx} 104 {tx} 148" fill="none" stroke="{C["gold"]}" stroke-width="1.6" marker-end="url(#ah2)" opacity=".9"/>'
    for x in xs:
        cx = x + bw / 2
        ar += f'<path d="M{cr} 246 C{cr} 310 {cx:.1f} 306 {cx:.1f} 358" fill="none" stroke="{C["gold"]}" stroke-width="1.6" marker-end="url(#ah2)" opacity=".9"/>'
    def brace(x1, x2, label, col):
        y = 520
        return f'<path d="M{x1} {y-8} V{y} H{x2} V{y-8}" fill="none" stroke="{col}" stroke-width="1.3"/><text x="{(x1+x2)/2}" y="{y+17}" text-anchor="middle" fill="{col}" font-size="9.5" letter-spacing="2.2" font-weight="600" font-family="Inter">{label}</text>'
    poss, poss1 = ("VOS", "VOTRE") if d["client"].get("registre") in ("vous", "couple") else ("TES", "TON")
    ar += brace(xs[0], xs[1] + bw, f"{poss} FONDATIONS PATRIMONIALES", C["tan"])
    if nl > 0:
        ar += brace(xs[2], xs[-1] + bw, f"{poss} LEVIERS" if nl > 1 else f"{poss1} LEVIER", C["tan"])
    ar += "</svg>"
    if nl > 0:
        lead2 = "Ton épargne de précaution couvre le court terme, tes fondations construisent un patrimoine qui rayonne sur le long terme, " + ("et les leviers l’amplifient." if nl > 1 else "et le levier l’amplifie.")
    else:
        lead2 = "Ton épargne de précaution couvre le court terme, et tes fondations construisent un patrimoine qui rayonne sur le long terme."
    inner = f"""
<h2 style="font-size:41px;line-height:1.04;text-wrap:balance">{titre}</h2>
<p class="lead">{lead2}</p>
<div class="rule"></div>
<div style="position:relative;width:{W}px;height:565px;margin-top:22px">{ar}{boxes}{row3}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:18px">
  <div class="card" style="--c:{C['prec']}"><div class="lbl" style="color:{C['prec']}">Épargne de précaution</div><p style="margin-top:6px">{eur(prec)} restent disponibles instantanément sur ton {lab}. C’est un matelas de sécurité, disponible tout de suite mais peu rémunéré.<br>C’est de l’épargne, pas un investissement.</p></div>
  <div class="card" style="--c:{C['gold']}"><div class="lbl" style="color:{C['gold']}">Épargner, puis investir</div><p style="margin-top:6px">Épargner, c’est mettre de côté. Investir, c’est donner un rôle précis à chaque euro, pour que ça rayonne sur ton quotidien, pour toi et tes proches.<br>Ici, {eur(prec)} sont épargnés et {eur(inv)} sont investis.</p></div>
</div>
"""
    return shell(2, 1, inner, d)


# ------------------------------------------------------------------ page 3
def donut(parts, cx, cy, R, r, total):
    import math
    out, ang = "", -math.pi / 2
    for val, col in parts:
        da = 2 * math.pi * val / total
        a2 = ang + da - (0.018 if len(parts) > 1 else 0)
        x1, y1, x2, y2 = cx + R * math.cos(ang), cy + R * math.sin(ang), cx + R * math.cos(a2), cy + R * math.sin(a2)
        x3, y3, x4, y4 = cx + r * math.cos(a2), cy + r * math.sin(a2), cx + r * math.cos(ang), cy + r * math.sin(ang)
        lg = 1 if da > math.pi else 0
        out += f'<path d="M{x1:.1f} {y1:.1f} A{R} {R} 0 {lg} 1 {x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f} A{r} {r} 0 {lg} 0 {x4:.1f} {y4:.1f} Z" fill="{col}"/>'
        ang += da
    return out


def page3(d):
    tmi = int(d["leviers"].get("tmi", 0) * 100)
    f = d["fin"]
    hf = bool(f)
    cards = [
        (C["gold"], "Capitalisante", "Assurance-vie", f"{eur(d['av']['initial'])} + {num(d['av']['mensuel'])}\u00a0€/mois",
         "Rentabiliser ton épargne, tout en la gardant disponible.",
         "Unités de compte : le capital n’est pas garanti."),
        (C["sage"], "Distribuante", "SCPI en direct", f"{eur(d['scpi']['initial'])} + {num(d['scpi']['mensuel'])}\u00a0€/mois",
         "Créer un complément de revenus passifs, grâce aux loyers perçus chaque mois.",
         "Loyers non garantis ; placement long terme, peu liquide."),
        (C["blue"], "Économie d’impôt", "PER", f"{eur(d['per']['initial'])} + {num(d['per']['mensuel'])}\u00a0€/mois",
         f"Transformer ton impôt sur le revenu en un avantage&nbsp;: profiter d’une rentabilité instantanée de {tmi} %.",
         "Bloqué jusqu’à la retraite (cas de déblocage prévus) ; imposé à la sortie."),
    ]
    if hf:
        cards.append((C["lev"], "Démultiplicatrice", "SCPI en financement", f"{eur(f['apport'])} + {num(f['effort'])}\u00a0€/mois",
                      "Une partie de ton effort d’épargne dope ton patrimoine grâce au levier du financement.",
                      f"Financement sur {f['duree']} ans."))
    if not d.get("has_per", True):
        cards = [x for x in cards if x[2] != "PER"]
    html = ""
    for i_c, (col, tag, name, key, role, lim) in enumerate(cards):
        span = ";grid-column:1/-1" if (len(cards) % 2 == 1 and i_c == len(cards) - 1) else ""
        html += f"""<div class="card top" style="--c:{col};padding:16px 20px 13px;display:flex;flex-direction:column{span}">
<div style="display:flex;justify-content:space-between;align-items:center"><span class="pill">{tag}</span><span style="font-family:'Bodoni Moda',serif;font-size:13px;color:{col}">{key}</span></div>
<div style="font-family:'Bodoni Moda',serif;font-size:25px;margin:10px 0 6px">{name}</div>
<p style="font-size:11.5px;line-height:1.55;color:var(--text);min-height:36px">{role}</p>
</div>"""
    # camembert : capital placé au départ par le client (hors financement, compensé par la dette)
    parts = [(d["av"]["initial"], C["gold"], "Assurance-vie"), (d["scpi"]["initial"], C["sage"], "SCPI en direct"),
             (d["per"]["initial"], C["blue"], "PER")]
    parts = [p for p in parts if p[0] > 0]
    tot = sum(p[0] for p in parts)
    pie = f'<svg width="230" height="230" viewBox="0 0 260 260">{donut([(v, c) for v, c, _ in parts], 130, 130, 120, 70, tot)}' \
          f'<text x="130" y="124" text-anchor="middle" fill="{C["text"]}" font-size="25" font-family="Bodoni Moda">{num(tot)}\u00a0€</text>' \
          f'<text x="130" y="144" text-anchor="middle" fill="{C["muted"]}" font-size="9.5" letter-spacing="1.6" font-family="Inter">CAPITAL PLACÉ</text></svg>'
    leg = "".join(f'<div style="display:flex;align-items:center;gap:8px;margin-top:7px"><span class="dc" style="background:{c};margin:0"></span><span style="font-size:11px;flex:1">{n}</span><span style="font-size:11px;color:var(--muted)">{eur(v)}</span></div>' for v, c, n in parts)
    rows = [("Assurance-vie", C["gold"], d["av"]["initial"], d["av"]["mensuel"]),
            ("SCPI en direct", C["sage"], d["scpi"]["initial"], d["scpi"]["mensuel"]),
            ("PER", C["blue"], d["per"]["initial"], d["per"]["mensuel"])]
    if hf:
        rows.append(("SCPI en financement", C["lev"], f["apport"], f["effort"]))
    if not d.get("has_per", True):
        rows = [r for r in rows if r[0] != "PER"]
    ti, tm = sum(r[2] for r in rows), sum(r[3] for r in rows)
    trs = "".join(f'<tr><td><span class="dc" style="background:{c}"></span>{n}</td><td>{eur(i)}</td><td>{eur(m)}</td></tr>' for n, c, i, m in rows)
    trs += f'<tr class="tot"><td>Total</td><td>{eur(ti)}</td><td>{eur(tm)}</td></tr>'
    note3 = (f"""  <div class="note" style="margin:10px 0 6px">Pour la SCPI en financement&nbsp;:
<ul style="margin:5px 0 0;padding-left:14px;list-style:disc;font-size:9px;line-height:1.45;color:var(--muted)">
<li class="note" style="margin-bottom:5px">Le montant mensuel est ta participation au financement au départ, qui pourra diminuer d’année en année du fait de la revalorisation des parts de SCPI financées.</li>
<li class="note">Tu possèdes {eur(f['emprunte'])} de parts, mais tu dois {eur(f['emprunte'])} à la banque&nbsp;: au départ, ça s’annule, donc ce n’est pas compté ici. À mesure que tu rembourses, la part qui t’appartient réellement grandit, jusqu’à la totalité.</li>
</ul></div>""" if hf else "")
    inner = f"""
<h2 style="font-size:41px;line-height:1.04;text-wrap:balance">À chaque enveloppe son rôle, au service de tes objectifs.</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:36px">{html}</div>
<div style="display:grid;grid-template-columns:290px 1fr;gap:30px;margin-top:40px;align-items:stretch">
  <div class="card" style="padding:16px 14px 14px"><div class="lbl" style="color:var(--gold);margin-bottom:6px">Répartition de ton patrimoine</div><div style="display:flex;justify-content:center">{pie}</div>{leg}</div>
  <div class="card" style="padding:16px 18px 12px;display:flex;flex-direction:column;justify-content:space-between"><div class="lbl" style="color:var(--gold)">Ce que tu mets dans chaque enveloppe</div>
  <table style="{'margin-top:6px' if hf else 'margin:auto 0'}"><tr><th>Enveloppe</th><th>Au départ</th><th>Par mois</th></tr>{trs}</table>
{note3}</div>
</div>
"""
    return shell(3, 1, inner, d)


# ------------------------------------------------------------------ page 4
def waterfall(v, hp=True, hf=True):
    W, base = 620, 340
    S = 280 / v["brut"]
    cw = 112
    ncol = 4 if hp else 3
    gap = (W - ncol * cw) / (ncol - 1)
    xs = [i * (cw + gap) for i in range(ncol)]
    t = lambda x, y, s, col=C["text"], sz=11, w=600, a="middle", ff="Inter": f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" fill="{col}" font-size="{sz}" font-weight="{w}" font-family="{ff}">{s}</text>'
    out = f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="{C["line"]}"/>'
    def rect(x, a, b, col):
        return f'<rect x="{x:.1f}" y="{base-b*S:.1f}" width="{cw}" height="{(b-a)*S:.1f}" rx="4" fill="{col}"/>'
    # colonne 1 : versements programmés (AV, SCPI, PER) + participation au financement, empilés
    a = 0
    stack = [("AV", v["av"], C["gold"]), ("SCPI", v["sc"], C["sage"])] + ([("PER", v["per"], C["blue"])] if hp else []) + ([("Financement", v["part"], C["lev"])] if hf else [])
    for lab, val, col in stack:
        out += rect(xs[0], a, a + val, col)
        out += t(xs[0] + cw / 2, base - (a + val / 2) * S + 3.5, f"{lab} {num(val)}", "#2a251f", 8.5, 700)
        a += val
    out += t(xs[0] + cw / 2, base - v["brut"] * S - 8, eur(v["brut"]), C["text"], 12)
    levels, cur, k = [v["brut"]], v["brut"], 1
    if hp:                                   # économie d'impôt du PER
        nxt = cur - v["eco"]
        out += rect(xs[k], nxt, cur, C["blue"])
        out += t(xs[k] + cw / 2, base - cur * S - 8, f"− {eur(v['eco'])}", C["blue"], 12)
        cur = nxt; levels.append(cur); k += 1
    nxt = cur - v["loy_dir"]                 # loyers de la SCPI en direct
    out += rect(xs[k], nxt, cur, C["sage"])
    out += t(xs[k] + cw / 2, base - cur * S - 8, f"− {eur(v['loy_dir'])}", C["sage"], 12)
    cur = nxt; levels.append(cur); k += 1
    out += rect(xs[k], 0, v["reel"], C["tan"])
    out += t(xs[k] + cw / 2, base - v["reel"] * S - 9, f"≈ {eur(v['reel'])}", C["tan"], 14, 700)
    for i, lv in enumerate(levels):
        y = base - lv * S
        out += f'<line x1="{xs[i]+cw:.1f}" y1="{y:.1f}" x2="{xs[i+1]:.1f}" y2="{y:.1f}" stroke="{C["muted"]}" stroke-dasharray="3 3"/>'
    labs = [(["Versement programmé", "mensuel"], C["text"])] + ([(["Économie d’impôt", "PER"], C["blue"])] if hp else []) + [(["Loyers perçus", "SCPI en direct"], C["sage"]), (["Effort réel", "mensuel"], C["text"])]
    for x, (lines, col) in zip(xs, labs):
        for k2, ln in enumerate(lines):
            out += t(x + cw / 2, base + 24 + 16 * k2, ln, col, 11.5, 700)
    return f'<svg width="{W+16}" height="{base+50-34}" viewBox="-16 34 {W+16} {base+50-34}" style="margin-left:{(698-W)//2-16}px;overflow:visible">{out}</svg>'


def page4(d):
    v = vases(d)
    per_i, per_m, tmi = d["per"]["initial"], d["per"]["mensuel"], d["leviers"].get("tmi", 0)
    te = d["per"]["taux_eco"]
    rows = f"""
<tr><td>Versement initial (avant le 31/12)</td><td>{eur(per_i)}</td><td>{eur(per_i*te)}</td></tr>
<tr><td style="white-space:nowrap">Versements programmés (12&nbsp;×&nbsp;{num(per_m)}&nbsp;€)</td><td>{eur(12*per_m)}</td><td>{eur(12*per_m*te)}</td></tr>
<tr class="tot"><td>Total 1<sup>re</sup> année</td><td>{eur(per_i+12*per_m)}</td><td>{eur((per_i+12*per_m)*te)}</td></tr>"""
    hp = d.get("has_per", True)
    lead4 = "L’économie d’impôt du PER et les loyers perçus de la SCPI en direct financent une partie de tes versements." if hp else "Les loyers perçus de la SCPI en direct financent une partie de tes versements."
    if hp:
        bas4 = f"""<div style="display:grid;grid-template-columns:1.45fr 1fr;gap:16px;margin-top:20px">
  <div class="card" style="padding:13px 15px 8px"><div class="lbl" style="color:{C['blue']}">Le PER, première année (tranche à {int(tmi*100)} %)</div>
    <table style="margin-top:4px"><tr><th>Versement</th><th>Montant</th><th>Économie</th></tr>{rows}</table></div>
  <div class="card" style="background:rgba(180,152,104,.12);border-color:rgba(180,152,104,.45)"><div class="lbl" style="color:var(--gold)">Comment ça marche</div>
    <p style="margin-top:6px">Lors de ta déclaration d’impôt au printemps suivant, je t’accompagne pour déclarer tes versements PER. L’économie d’impôt arrive ensuite sur ton compte courant, pendant l’été.</p>
    <p style="margin-top:6px">La première année, tu avances donc les versements avant le premier remboursement. Ici, on raisonne en effort lissé sur la durée.</p></div>
</div>"""
    else:
        fisc_pct = int(d["hyp"]["fiscalite_comptant"] * 100)
        bas4 = f"""<div class="card" style="margin-top:20px;background:rgba(180,152,104,.12);border-color:rgba(180,152,104,.45)"><div class="lbl" style="color:var(--gold)">Comment ça marche</div>
    <p style="margin-top:6px">Les loyers comptés ici correspondent à ton versement initial en SCPI en direct ({eur(d["scpi"]["initial"])}) : environ {eur(v["loy_dir"])} par mois, après impôt à {fisc_pct}&nbsp;%.</p>
    <p style="margin-top:6px">Tes versements mensuels en SCPI produisent à leur tour des loyers, qui s’ajoutent progressivement après un délai de jouissance. Ici, on raisonne en effort lissé sur la durée.</p></div>"""
    inner = f"""
<h2 style="font-size:41px;line-height:1.04;text-wrap:balance">Chaque mois, ton effort réel est inférieur à ce que tu verses.</h2>
<p class="lead">{lead4}</p>
<div class="rule"></div>
<div style="margin-top:22px">{waterfall(v, hp, bool(d.get('financement')))}</div>
{bas4}
"""
    return shell(4, 1, inner, d)


# ------------------------------------------------------------------ page 5
def pctfr(x):
    return f"{x*100:.1f}".replace(".", ",").replace(",0", "")



MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def docs_rows(d):
    """Pièces à préparer : (libellé, clé, statut). Mois et années calculés d'après la date du RDV."""
    j, mois, an = d["date_rdv"].split()
    mi, y = MOIS.index(mois), int(an)
    # 3 derniers mois pleins avant le mois du RDV, du plus récent au plus ancien
    ms = [((mi - k) % 12, y - 1 if mi - k < 0 else y) for k in (1, 2, 3)]
    parts = []
    for n, (mm, yy) in enumerate(ms):
        suffixe = f" {yy}" if (n == len(ms) - 1 or ms[n + 1][1] != yy) else ""
        parts.append(MOIS[mm] + suffixe)
    mois_txt = f"{parts[0]}, {parts[1]} et {parts[2]}"
    # avis d'imposition : l'avis de l'année est émis en été (à vérifier : fin juillet / août)
    ya = y if mi >= 7 else y - 1
    rows = [
        ("Pièce d’identité en cours de validité (recto verso)", "identite"),
        ("RIB du compte sur lequel tu souhaites être prélevé", "rib"),
        ("Justificatif de domicile (type facture) de moins de 2 mois", "domicile"),
    ]
    heb = d.get("logement", {}).get("statut") == "heberge"
    par = d.get("logement", {}).get("par", "la personne qui t’héberge")
    if heb:
        rows[2] = (f"Justificatif de domicile de {par} (type facture) de moins de 2 mois", "domicile")
    if d.get("financement"):
        rows += [
            (f"Bulletin de paie de décembre {y - 1}", "paie_dec"),
            (f"3 derniers bulletins de paie ({mois_txt})", "paie3"),
            (f"3 derniers relevés bancaires de tous tes comptes ({mois_txt})", "releves3"),
            (f"Avis d’imposition {ya} sur les revenus {ya - 1}, ainsi que celui de {ya - 1} sur les revenus {ya - 2}", "impots"),
            (f"Attestation sur l’honneur d’hébergement, signée par {par}", "hebergement") if heb else ("Bail du logement", "bail"),
        ]
    fournis = set(d.get("docs_fournis", []))
    out = [(lib, "Reçu" if k in fournis else "À fournir") for lib, k in rows]
    if d.get("financement"):
        out.append(("Mandat de recherche", "À signer"))
    return out


def hyp_rows(d, compact=False):
    h, f = d["hyp"], d["fin"]
    pc = lambda x: str(round(x * 100, 1)).replace(".", ",").replace(",0", "")
    if compact:
        return [
            ("Assurance-vie et PER", f"{pc(h['taux_av_per'])} %/an"),
            ("Loyers des SCPI", f"Taux de distribution des SCPI en direct : {pc(h['scpi_brut'])} %/an de loyers, imposés à {int(h['fiscalite_comptant']*100)} % (fiscalité européenne), revalorisation des parts de {pc(h['scpi_reval'])}&nbsp;% par&nbsp;an<br>SCPI en financement : {pc(f['loyers_taux_simu'])} % par an, non imposés (grâce aux charges déductibles) ; revalorisation des parts de {pc(h['scpi_reval'])} % par an"),
            ("Financement", f"{eur(f['emprunte'])} sur {f['duree']} ans, TAEG {pc(f['taux'])} %" + (f", assurance {pc(f['assurance'])} %" if f['assurance'] else "") + "."),
            ("Impôt", f"Économie d’impôt du PER calculée avec une tranche marginale (TMI) de {int(d['leviers']['tmi']*100)} %"),
            ("Sans financement", "Le même effort réel est investi chaque mois en SCPI en direct ; les loyers, perçus et non réinvestis, sont comptés dans le total (page 6)."),
        ]
    return [
        ("Assurance-vie et PER", f"{pc(h['taux_av_per'])} % par an, net de frais de gestion du contrat et des supports, avant fiscalité de sortie"),
        ("Loyers des SCPI", f"SCPI en direct : {pc(h['scpi_brut'])} % par an de loyers, imposés à {int(h['fiscalite_comptant']*100)} % (fiscalité forfaitaire), soit {pc(h['scpi_distribution'])} % perçus ; SCPI en financement : {pc(f['loyers_taux_simu'])} % par an, non imposés (charges déductibles) ; revalorisation des parts de {pc(h['scpi_reval'])} % par an ; hors frais d’entrée"),
        ("Financement", f"{eur(f['emprunte'])} sur {f['duree']} ans à {pc(f['taux'])} %, assurance {int(f['assurance']*100)} %"),
        ("Impôt", f"Tranche marginale à {int(d['leviers']['tmi']*100)} % ; économie d’impôt du PER dans la limite du plafond de déduction"),
    ]


def chart5(sim, d):
    W, base = 620, 300
    hzs = tuple(d.get("horizons", (10, 20, 30)))
    hz = {y: sim[y] for y in hzs}
    mx = max(v["total"] for v in hz.values())
    S = 250 / mx
    bw = 112
    step = 140 if len(hzs) >= 3 else 190
    xs = [30 + i * step for i in range(len(hzs))]
    t = lambda x, y, s, col=C["text"], sz=11, w=600, a="middle": f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" fill="{col}" font-size="{sz}" font-weight="{w}" font-family="Inter">{s}</text>'
    out = f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="{C["line"]}"/>'
    for x, (y, v) in zip(xs, hz.items()):
        a = 0
        for key, col in (("scpi", C["sage"]), ("fin", C["lev"]), ("per", C["blue"]), ("av", C["gold"])):
            if v[key] <= 0:
                continue                                 # enveloppe absente (sans PER, sans financement)
            h = v[key] * S
            out += f'<rect x="{x}" y="{base-(a+v[key])*S:.1f}" width="{bw}" height="{h:.1f}" fill="{col}" rx="2"/>'
            if h >= 9.5:
                out += t(x + bw / 2, base - (a + v[key] / 2) * S + 3.5, eur(round(v[key], -2)), "#2a251f", 9.5 if h >= 14 else 8, 700)
            a += v[key]
        out += t(x + bw / 2, base - v["total"] * S - 9, f"{round(v['total']/1000):,} k€".replace(",", "\u202f"), C["text"], 13, 700)
        yp = base - v["poche"] * S
        out += f'<line x1="{x-8}" y1="{yp:.1f}" x2="{x+bw+8}" y2="{yp:.1f}" stroke="{C["text"]}" stroke-width="1.6" stroke-dasharray="5 3"/>'
        out += t(x + bw / 2, base + 19, f"{y} ans", C["text"], 11.5, 600)
    lx = 468
    items = [("Assurance-vie", C["gold"]), ("PER", C["blue"]), ("SCPI en financement", C["lev"]), ("SCPI en direct", C["sage"])]
    if not d.get("has_per", True):
        items = [x for x in items if x[0] != "PER"]
    if not d.get("financement"):
        items = [x for x in items if x[0] != "SCPI en financement"]
    for i, (n, col) in enumerate(items):
        yy = 34 + i * 30
        out += f'<rect x="{lx}" y="{yy}" width="11" height="11" rx="2" fill="{col}"/>' + t(lx + 19, yy + 9.5, n, C["text"], 11, 600, "start")
    yy = 34 + len(items) * 30
    out += f'<line x1="{lx}" y1="{yy+5}" x2="{lx+11}" y2="{yy+5}" stroke="{C["text"]}" stroke-width="1.6" stroke-dasharray="4 2"/>' + t(lx + 19, yy + 9.5, "De ta poche", C["text"], 11, 600, "start")
    return f'<svg width="{W}" height="{base+10}" viewBox="0 20 {W} {base+10}">{out}</svg>'


def curve(sim, d):
    W, H = 620, 248
    L, R, T, B = 78, 20, 14, 30
    ser = sim["series"]
    yrs = sorted(ser)
    last = yrs[-1]
    top = max(ser[y]["total"] for y in yrs)
    gstep = next(g for g in (50000, 100000, 200000, 250000, 500000, 1000000) if top * 1.12 / g <= 6)
    ymax = (int(top * 1.12 / gstep) + 1) * gstep
    X = lambda y: L + (y - 1) / (last - 1) * (W - L - R)
    Y = lambda v: T + (1 - v / ymax) * (H - T - B)
    def path(key):
        return " ".join(("M" if i == 0 else "L") + f"{X(y):.1f} {Y(ser[y][key]):.1f}" for i, y in enumerate(yrs))
    out = ""
    for v in range(0, ymax + 1, gstep):
        out += f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W-R}" y2="{Y(v):.1f}" stroke="{C["line"]}" stroke-width="1"/>'
        if v:
            out += f'<text x="{L-10}" y="{Y(v)+4:.1f}" text-anchor="end" fill="{C["muted"]}" font-size="10" font-family="Inter">{num(v)}\u00a0€</text>'
    base = Y(0)
    out += f'<defs><linearGradient id="gA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["tan"]}" stop-opacity=".55"/><stop offset="1" stop-color="{C["tan"]}" stop-opacity=".08"/></linearGradient><linearGradient id="gB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["blue"]}" stop-opacity=".6"/><stop offset="1" stop-color="{C["blue"]}" stop-opacity=".1"/></linearGradient></defs>'
    out += f'<path d="{path("total")} L{X(last):.1f} {base:.1f} L{X(yrs[0]):.1f} {base:.1f} Z" fill="url(#gA)"/>'
    out += f'<path d="{path("poche")} L{X(last):.1f} {base:.1f} L{X(yrs[0]):.1f} {base:.1f} Z" fill="url(#gB)"/>'
    out += f'<path d="{path("total")}" fill="none" stroke="{C["tan"]}" stroke-width="2.6" stroke-linejoin="round"/>'
    out += f'<path d="{path("poche")}" fill="none" stroke="{C["blue"]}" stroke-width="2.2" stroke-linejoin="round"/>'
    tstep = 5 if last <= 50 else 10
    for y in [1] + list(range(tstep, last + 1, tstep)):
        out += f'<text x="{X(y):.1f}" y="{H-8}" text-anchor="middle" fill="{C["muted"]}" font-size="10.5" font-family="Inter">{y}</text>'
    out += f'<text x="{X(last)-6:.1f}" y="{Y(ser[last]["total"])-10:.1f}" text-anchor="end" fill="{C["tan"]}" font-size="11" font-weight="600" font-family="Inter">Patrimoine estimé</text>'
    py = Y(ser[last]["poche"])
    ly = py + 22 if (base - py) > 40 else py - 9
    out += f'<text x="{X(last)-6:.1f}" y="{ly:.1f}" text-anchor="end" fill="{C["blue"]}" font-size="11" font-weight="600" font-family="Inter">De ta poche</text>'
    return f'<svg width="{W}" height="{H+6}" viewBox="0 0 {W} {H+6}">{out}</svg>'


def page5(d):
    hzs = tuple(d.get("horizons", (10, 20, 30)))
    sim = simulate(d, hzs)
    sl = sim[hzs[-1]]
    fin = d["fin"]; duree = fin["duree"] if fin else None
    prog = d["av"]["mensuel"] + d["scpi"]["mensuel"] + d["per"]["mensuel"]
    effort_dernier = (fin["mensualite"] - fin["emprunte"] * (1 + d["hyp"]["scpi_reval"]) ** duree * fin["loyers_taux_simu"] / 12) if fin else 0
    extra = ""
    if fin and hzs[-1] > duree:
        loy_m = sim["series"][duree + 1]["loyers_mois"]
        couvert = loy_m >= prog
        extra = (f"<br>Passée la {duree}<sup>e</sup> année, le financement des parts de SCPI est entièrement remboursé. Ainsi, le montant des versements programmés passe de {eur(round(prog + effort_dernier))} à {eur(prog)}/mois."
                 + (f" Cet effort d’épargne est entièrement couvert par les loyers perçus à ce stade ({eur(round(loy_m, -1))}/mois)&nbsp;: le cash-flow mensuel est positif et le patrimoine continue de grandir sans effort d’épargne additionnel de ta part." if couvert else ""))
    note5 = (f'<div style="margin-top:18px"><div class="lbl" style="color:var(--gold);margin-bottom:5px">Pourquoi l’effort d’épargne diminue-t-il à partir de la {duree}<sup style="text-transform:none">e</sup> année&nbsp;?</div><p class="note">{extra[4:]}</p></div>' if extra else "")
    hz_txt = ", ".join(str(h) for h in hzs[:-1]) + f" et {hzs[-1]}"
    num_st = "font-family:'Bodoni Moda',serif;font-size:32px;margin-top:5px;line-height:1.05"
    kpi = f"""<div style="display:grid;grid-template-columns:1fr 1fr 1fr;border:1px solid var(--line);border-radius:14px;background:linear-gradient(90deg,#34414f 0%,#3b3a36 55%,#5a4c34 100%);padding:13px 0;box-shadow:0 2px 14px rgba(0,0,0,.25)">
  <div style="padding:0 6px 0 22px"><div class="lbl" style="color:#d6c3a0">Patrimoine estimé à {hzs[-1]} ans</div><div style="{num_st}">{eur(round(sl['total'],-3))}</div></div>
  <div style="padding:0 6px 0 22px;border-left:1px solid rgba(255,255,255,.16)"><div class="lbl" style="color:#a9bdd4">De ta poche</div><div style="{num_st}">{eur(round(sl['poche'],-3))}</div></div>
  <div style="padding:0 6px 0 22px;border-left:1px solid rgba(255,255,255,.16)"><div class="lbl" style="color:#e0c892">Écart</div><div style="{num_st};color:#e8d3a2">+{eur(round(sl['total'],-3) - round(sl['poche'],-3))}</div></div>
</div>"""
    inner = f"""
<h2 style="font-size:41px;line-height:1.04;text-wrap:balance">Ce que ton patrimoine peut devenir.</h2>
<p class="lead">Au-delà de ce que tu verses, la durée pendant laquelle tu restes investi joue un rôle central&nbsp;: voici {hz_txt}&nbsp;ans, à&nbsp;versements identiques.</p>
<div class="rule"></div>
<div style="width:620px;margin:30px auto 0">{kpi}
<div style="margin-top:20px">{chart5(sim, d)}</div>
<div style="margin-top:26px"><div class="lbl" style="margin-bottom:6px;font-size:11px">Évolution de <span style="color:var(--tan)">ton patrimoine</span> et de ce que tu mets <span style="color:var(--blue)">de ta poche</span>&nbsp;:</div>{curve(sim, d)}</div></div>
{note5}
"""
    return shell(5, 2, inner, d)


# ------------------------------------------------------------------ page 6
def page6(d):
    f = d["fin"]
    P = d.get("pertinence", {})
    # blocs 1 et 2 dans le même paragraphe (pas de retour à la ligne entre eux) ; bloc 3 à part
    b12 = []
    if P.get("revenus_stables"):
        b12.append("Tes revenus sont stables et ton taux d’endettement très faible.")
    if P.get("dossier_banque"):
        b12.append("Les revenus SCPI que tu vas percevoir renforceront ton dossier auprès des banques, pour de futures opérations immobilières en financement.")
    blocs = [" ".join(b12)] if b12 else []
    if P.get("negociation"):
        blocs.append("Je m’occupe de la négociation&nbsp;: tu fournis les documents, et je reviens vers toi avec les meilleures conditions obtenues auprès de mes partenaires bancaires.")
    pert_titre = '<div style="font-size:13px;font-weight:700;color:var(--text);margin-bottom:6px">Pourquoi c’est pertinent pour toi</div>' if blocs else ""
    pert_blocs = "".join(f'<p style="font-size:10.5px;margin-top:{0 if i == 0 else 4}px">{t}</p>' for i, t in enumerate(blocs))
    pert_card = f'<div class="card" style="margin-top:10px;padding:16px 20px">{pert_titre}{pert_blocs}</div>' if blocs else ""
    W = 650
    sch = f"""
<div style="position:relative;width:{W}px;height:298px;margin:0 auto;zoom:.88">
<svg style="position:absolute;left:0;top:0" width="{W}" height="298" viewBox="0 0 {W} 298"><defs><marker id="ah6" markerWidth="9" markerHeight="9" refX="6" refY="4.5" orient="auto"><path d="M1 1 L7 4.5 L1 8" fill="none" stroke="{C['gold']}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<path d="M180 41 H216" stroke="{C['gold']}" stroke-width="1.8" marker-end="url(#ah6)"/>
<path d="M406 41 H442" stroke="{C['gold']}" stroke-width="1.8" marker-end="url(#ah6)"/>
<path d="M548 82 V172 H453" fill="none" stroke="{C['gold']}" stroke-width="1.8" marker-end="url(#ah6)"/>
<path d="M195 172 H90 V86" fill="none" stroke="{C['gold']}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#ah6)"/>
<path d="M325 232 V210" stroke="{C['gold']}" stroke-width="1.8" marker-end="url(#ah6)"/>
<text x="100" y="130" fill="{C['muted']}" font-size="9.5" font-family="Inter">rembourse la banque</text>
</svg>
<div class="nb" style="left:0;top:0;width:180px;height:82px;background:{C['text']};color:#2a251f"><div class="a">La banque</div><div class="c">te prête {eur(f['emprunte'])}</div></div>
<div class="nb" style="left:220px;top:0;width:186px;height:82px;background:{C['lev']};color:#fff"><div class="a">Tes SCPI</div><div class="c">à ton nom dès le départ</div></div>
<div class="nb" style="left:446px;top:0;width:204px;height:82px;background:var(--card2);border:1.5px solid {C['lev']}"><div class="a" style="color:{C['lev']}">Tes loyers</div><div class="c">≈ {eur(f['loyers'])} par mois</div></div>
<div class="nb" style="left:230px;top:234px;width:190px;height:50px;background:{C['tan']};color:#2a251f"><div class="a" style="font-size:19px">Ton effort</div><div class="c">{f['effort']} € par mois</div></div>
<div class="nb" style="left:196px;top:140px;width:258px;height:64px;background:rgba(91,154,107,.14);border:1.5px solid {C['lev']}"><div class="a" style="font-size:19px">Mensualité {eur(f['mensualite'])}</div></div>
</div>"""
    # barres : effort d'épargne complété par le levier du financement / par les loyers perçus
    mx = max(f["patrimoine_avec"], f["patrimoine_sans"])
    S = 260 / mx
    base = 310
    # échelle volontairement non proportionnelle : bas de colonne (effort, loyers + valorisation) compressé,
    # sommet (levier) étiré, pour que l'effet de levier se lise d'un coup d'œil
    _k = 0.72
    _avv = f["patrimoine_avec"]; _saa = f["patrimoine_sans"]
    _S2 = (260 - _saa * _k * S) / (_avv - _saa)
    Y = lambda v: v * _k * S if v <= _saa else _saa * _k * S + (v - _saa) * _S2
    t = lambda x, y, s, col=C["text"], sz=11, w=600, a="middle": f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" fill="{col}" font-size="{sz}" font-weight="{w}" font-family="Inter">{s}</text>'
    ax, b1x, b2x, bw = 172, 198, 376, 118
    eff = f["effort_total"]
    av = f["patrimoine_avec"]; sa = f["patrimoine_sans"]
    xr = b2x + bw
    ch = f'<line x1="{b1x-14}" y1="{base}" x2="{xr+12}" y2="{base}" stroke="{C["line"]}"/>'
    def seg(x, a0, a1, col, lab=""):
        o = f'<rect x="{x}" y="{base-Y(a1):.1f}" width="{bw}" height="{Y(a1)-Y(a0):.1f}" fill="{col}" rx="2"/>'
        if lab and Y(a1) - Y(a0) >= 13:
            o += t(x + bw / 2, base - (Y(a0) + Y(a1)) / 2 + 4, lab, "#2a251f", 12, 700)
        return o
    for x in (b1x, b2x):
        ch += seg(x, 0, eff, C["tan"], num(eff)) + seg(x, eff, sa, C["sage"], num(sa - eff))
    ch += seg(b1x, sa, av, C["lev"])
    # axe des ordonnées : niveaux « effort » et « loyers + valorisation », repérés par des pointillés
    for v, lab, col in ((eff, "Effort", C["tan"]), (sa, "Loyers + valorisation", C["sage"])):
        yy = base - Y(v)
        ch += f'<path d="M{ax} {yy:.1f} H{xr}" stroke="{C["text"]}" stroke-width="1" stroke-dasharray="4 3" opacity=".6"/>'
        ch += t(ax - 9, yy + 4, lab, col, 11, 700, "end")
    # flèche d'effet de levier : du sommet de la colonne « sans » au sommet de la colonne « avec »
    ya, ys = base - Y(av), base - Y(sa)
    xa = (b1x + bw + b2x) / 2
    lv = C["lev"]
    ch += f'<path d="M{xa:.1f} {ys:.1f} V{ya+2:.1f}" stroke="{lv}" stroke-width="2.4" stroke-linecap="round"/>'
    ch += f'<path d="M{xa-7:.1f} {ya+10:.1f} L{xa:.1f} {ya+1:.1f} L{xa+7:.1f} {ya+10:.1f}" fill="none" stroke="{lv}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
    ch += f'<text x="{xa+13:.1f}" y="{ya+10:.1f}" fill="{lv}" font-size="9" font-weight="700" letter-spacing="1" font-family="Inter">EFFET DE LEVIER</text>'
    ch += f'<text x="{xa+13:.1f}" y="{ya+38:.1f}" fill="{C["text"]}" font-size="23" font-weight="700" font-family="Inter">+&#160;{eur(av-sa)}</text>'
    ch += f'<text x="{xa+13:.1f}" y="{ya+60:.1f}" fill="{lv}" font-size="15" font-weight="700" font-family="Inter">+&#160;{f["levier_pct"]}&#160;%</text>'
    ch += t(b1x + bw / 2, base - Y(av) - 10, eur(av), C["text"], 19, 700) + t(b2x + bw / 2, base - Y(sa) - 10, eur(sa), C["text"], 19, 700)
    ch += t(b1x + bw / 2, base + 20, "Avec financement", C["lev"], 11, 600) + t(b2x + bw / 2, base + 20, "Sans financement", C["sage"], 11, 600)
    chart = f'<svg width="540" height="{base+34-24}" viewBox="0 24 540 {base+34-24}">{ch}</svg>'
    facts = f"""
<div class="card" style="padding:18px 18px;border-color:{C['lev']}"><div class="lbl" style="color:{C['lev']}">Effet de levier</div><div class="big" style="margin:8px 0 5px;font-size:34px;line-height:1.1;color:{C['lev']}">+&nbsp;{num(f['levier'])}&nbsp;€<br>+&nbsp;{f['levier_pct']}&nbsp;%</div><p style="font-size:10px;color:var(--muted)">d’écart entre ce que tu atteins avec le financement et sans.</p></div>"""
    inner = f"""
<h2 style="font-size:41px;line-height:1.04;text-wrap:balance">Le même effort, avec ou sans financement.</h2>
<p class="lead">{num(f['effort'])}&nbsp;€ par mois au départ, dégressif ensuite&nbsp;: c’est l’effort que demande le financement. Voici ce que donnerait ce même montant investi au fil de l’eau.</p>
<div class="rule"></div>
<div style="margin-top:22px">{sch}</div>
<div style="display:flex;flex-direction:column;align-items:center;margin-top:12px"><div class="lbl" style="align-self:flex-start;margin-bottom:12px;font-size:12px;letter-spacing:.10em;white-space:nowrap">Ce que tu atteins après {f['duree']} ans, pour le même effort&nbsp;:</div>{chart}</div>
{pert_card}

"""
    return shell(6, 2, inner, d)


# ------------------------------------------------------------------ page 7
def page7(d):
    h = d["hyp"]
    f = d["fin"]
    hf = bool(f)
    W = 698
    ys = 118 if hf else 40            # sans financement : une seule ligne, la validation est à sa hauteur
    pc = lambda x: str(round(x * 100, 1)).replace(".", ",").replace(",0", "")
    # --- frise : deux lignes parallèles après la validation
    nodes = []   # (x, y, num, couleur, titre, sous-titre)
    hp = d.get("has_per", True)
    # frise toujours centrée sur la page : la validation et la dernière souscription sont à égale distance des bords,
    # les étapes intermédiaires sont réparties à intervalles réguliers (3 ou 4 étapes selon le PER)
    n_et = 1 + 1 + int(hp) + 1
    marge = 78
    px = [marge + k * (W - 2 * marge) / (n_et - 1) for k in range(n_et)]
    x1, xa = px[0], px[1:]
    nodes.append((x1, ys, 1, C["text"], "Validation", "de la stratégie<br>et des montants"))
    top = [(C["sage"], "SCPI en direct", f"{eur(d['scpi']['initial'])}<br>+ {num(d['scpi']['mensuel'])}\u00a0€/mois")]
    if hp:
        top.append((C["blue"], "PER", f"{eur(d['per']['initial'])}<br>+ {num(d['per']['mensuel'])}\u00a0€/mois<br><b style='color:{C['blue']}'>avant le 31/12</b>"))
    top.append((C["gold"], "Assurance-vie", f"{eur(d['av']['initial'])}<br>+ {num(d['av']['mensuel'])}\u00a0€/mois"))
    for i_t, (col_t, t1_t, t2_t) in enumerate(top):
        nodes.append((xa[i_t], 40, 2 + i_t, col_t, t1_t, t2_t))
    if hf:
        nodes.append((xa[0], 196, 2, C["lev"], "Étude du financement", "étude personnalisée,<br>sans engagement"))
        nodes.append((xa[1], 196, 3, C["lev"], "SCPI en financement", f"{eur(f['emprunte'])} financés<br>si l’étude est retenue"))
    H7 = 268 if hf else 120
    svg = f'<svg style="position:absolute;left:0;top:0" width="{W}" height="{H7}" viewBox="0 0 {W} {H7}"><defs><marker id="ah7" markerWidth="9" markerHeight="9" refX="6" refY="4.5" orient="auto"><path d="M1 1 L7 4.5 L1 8" fill="none" stroke="{C["gold"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
    svg += f'<path d="M{xa[0]} 40 H{xa[len(top) - 1]}" stroke="{C["line"]}" stroke-width="3"/>'
    if hf:
        svg += f'<path d="M{xa[0]} 196 H{xa[1]}" stroke="{C["line"]}" stroke-width="3"/>'
        svg += f'<path d="M{x1+18:g} 118 C{x1+82:g} 118 {x1+92:g} 40 {xa[0]-20:g} 40" fill="none" stroke="{C["gold"]}" stroke-width="1.6" marker-end="url(#ah7)"/>'
        svg += f'<path d="M{x1+18:g} 118 C{x1+82:g} 118 {x1+92:g} 196 {xa[0]-20:g} 196" fill="none" stroke="{C["gold"]}" stroke-width="1.6" marker-end="url(#ah7)"/>'
    else:                                                     # une seule flèche : de la validation vers la ligne des souscriptions
        svg += f'<path d="M{x1+20:g} 40 H{xa[0]-22:g}" fill="none" stroke="{C["gold"]}" stroke-width="1.6" marker-end="url(#ah7)"/>'
    for x, y, n, col, t1, t2 in nodes:
        svg += f'<circle cx="{x}" cy="{y}" r="17" fill="{col}"/><text x="{x}" y="{y+5}" text-anchor="middle" fill="#2a251f" font-size="14" font-weight="700" font-family="Bodoni Moda">{n}</text>'
    svg += "</svg>"
    frise = f'<div style="position:relative;width:{W}px;height:{270 if hf else 150}px">{svg}'
    for x, y, n, col, t1, t2 in nodes:
        top = y + 26 if n != 1 else y + 26
        frise += f'<div style="position:absolute;left:{x-72}px;top:{top}px;width:144px;text-align:center"><div style="font-size:12px;font-weight:600">{t1}</div><div style="font-size:9.5px;color:var(--muted);line-height:1.45;margin-top:3px">{t2}</div></div>'
    frise += "</div>"
    pct = lambda x: pc(x)
    pc2 = lambda x: ("%g" % round(x * 100, 2)).replace(".", ",")
    an_rdv = d["date_rdv"].split()[-1]
    per_lead = f" À retenir&nbsp;: le PER est à mettre en place avant le 31&nbsp;décembre pour compter dès tes impôts {an_rdv}." if hp else ""
    lead_fin = ", tandis que la recherche de financement avance en parallèle" if hf else ""
    fin_txt = (f"{eur(f['emprunte'])} sur {f['duree']} ans, " + (f"taux d’intérêt {pc2(f['taux'])}&nbsp;% (hors assurance), assurance {pc2(f['assurance'])}&nbsp;%/an" if f["assurance"] else f"TAEG {pc2(f['taux'])}&nbsp;%")) if hf else ""
    fin_h = f" SCPI en financement&nbsp;: {pct(f['loyers_taux_simu'])}&nbsp;%/an, non imposés (grâce aux charges déductibles)." if hf else ""
    fin_t = f" Financement&nbsp;: {fin_txt}." if hf else ""
    per_txt = f" Économie d’impôt du PER calculée avec une tranche marginale (TMI) de {int(d['leviers']['tmi']*100)}&nbsp;%." if hp else ""
    sav_items = [
        (None, "Ce document est une simulation pédagogique. Les rendements indiqués sont des hypothèses&nbsp;: ils ne sont pas garantis et les performances passées ne préjugent pas des performances futures."),
        ("Hypothèses", f"Assurance-vie{' et PER' if hp else ''}&nbsp;: {pct(h['taux_av_per'])}&nbsp;%/an. SCPI en direct&nbsp;: {pct(h['scpi_brut'])}&nbsp;%/an de loyers, imposés à {int(h['fiscalite_comptant']*100)}&nbsp;% (fiscalité européenne).{fin_h} Parts revalorisées de {pct(h['scpi_reval'])}&nbsp;%/an.{fin_t}{per_txt}"),
        ("Risques", f"Les unités de compte de l’assurance-vie{' et du PER' if hp else ''} présentent un risque de perte en capital. Les SCPI sont un placement immobilier de long terme&nbsp;: capital, revenus et liquidité non garantis."),
        ("Financement et souscription", "Toute opération de crédit est soumise à l’acceptation du prêteur ; aucun engagement de financement n’est pris dans ce document. Aucune souscription n’est réalisée sans ta validation préalable et la remise des documents réglementaires (document d’entrée en relation, recueil d’informations, profil investisseur)."),
    ]
    if not hf:
        sav_items[-1] = ("Souscription", "Aucune souscription n’est réalisée sans ta validation préalable et la remise des documents réglementaires (document d’entrée en relation, recueil d’informations, profil investisseur).")
    sav = "".join(f'<p style="margin-top:{0 if k == 0 else 6}px;font-size:9.5px;line-height:1.5">' + (f'<b style="color:var(--tan);font-weight:600">{t} · </b>' if t else '') + f'{x}</p>' for k, (t, x) in enumerate(sav_items))
    stcol = {"À fournir": "var(--gold)", "À signer": "var(--blue)", "Reçu": "#86a08a"}
    docs_html = "".join(f'<tr><td style="padding:3.5px 14px 3.5px 0;border-top:1px solid rgba(255,255,255,.08);font-size:10.5px">{a}</td><td style="padding:3.5px 0;border-top:1px solid rgba(255,255,255,.08);font-size:10px;font-weight:600;white-space:nowrap;color:{stcol[b]}">{"✓ " if b == "Reçu" else ""}{b}</td></tr>' for a, b in docs_rows(d))
    inner = f"""
<h2 style="font-size:41px;line-height:1.04;text-wrap:balance">Les prochaines étapes, dans l’ordre.</h2>
<p class="lead">Tout commence par ta validation de la stratégie, puis viennent les souscriptions{lead_fin}.{per_lead}</p>
<div class="rule"></div>
<div style="margin-top:18px">{frise}</div>
<div class="card" style="margin-top:34px;padding:14px 20px"><div class="lbl" style="color:var(--gold)">À préparer</div><table style="margin-top:6px;width:100%"><tr><td class="lbl" style="font-size:8.5px;padding-bottom:4px">Document</td><td class="lbl" style="font-size:8.5px;padding-bottom:4px;width:1%;white-space:nowrap">Statut</td></tr>{docs_html}</table></div>
<div class="card" style="margin-top:28px;padding:13px 20px;background:rgba(180,152,104,.08);border-color:rgba(180,152,104,.4)"><div class="lbl" style="color:var(--gold)">À savoir</div>
<div style="margin-top:8px">{sav}</div></div>
"""
    return shell(7 if hf else 6, 3, inner, d)



# ------------------------------------------------------------------ page 8
def page8(d):
    an = d["version"].split("/")[-1]
    conf = f"""<div style="width:560px;border:1px solid rgba(180,152,104,.45);background:rgba(180,152,104,.07);border-radius:16px;padding:26px 34px 24px">
<div class="lbl" style="color:var(--gold);letter-spacing:.22em">Confidentiel</div>
<p style="font-size:11px;line-height:1.7;color:rgba(241,238,231,.86);margin-top:14px">Ce document a été élaboré à partir de ta situation personnelle. Il est strictement confidentiel&nbsp;: il ne peut être communiqué à un tiers, notamment un établissement bancaire ou un autre conseiller, ni reproduit ou utilisé en tout ou partie, sans l’accord écrit préalable de son auteur.</p>
<p style="font-size:11px;line-height:1.7;color:rgba(241,238,231,.86);margin-top:8px">Les analyses, simulations et méthodes qu’il contient constituent un savoir-faire protégé au titre du droit d’auteur (art.&nbsp;L.111-1 et L.122-4 du Code de la propriété intellectuelle) et du secret des affaires (art.&nbsp;L.151-1 et suivants du Code de commerce).</p>
<p style="font-size:9px;line-height:1.5;color:var(--muted);margin-top:10px">© {an} Victor Kieny. Tous droits réservés.</p></div>"""
    g = lambda *lines, first=False: '<div style="margin-top:' + ('0' if first else '16') + 'px">' + "".join(f'<p style="font-size:{11.5 if (first and k == 0) else 10}px;line-height:1.7;color:{"var(--text)" if (first and k == 0) else "rgba(241,238,231,.74)"};{"font-weight:600;" if (first and k == 0) else ""}">{l}</p>' for k, l in enumerate(lines)) + '</div>'
    legal = (
        g("Victor Kieny – RSAC de Toulouse N°&nbsp;943277053",
          "Mécène de l’association EPIC – FinzzAct",
          "23 rue d’Amsterdam, 75008 Paris",
          "Inscrit à l’Orias n°&nbsp;25008348&nbsp;: <span style='color:var(--gold)'>https://www.orias.fr</span>", first=True)
        + g("Mandataire d’intermédiaire en opérations de banque et services de paiement",
            "Agent lié de prestataire de services d’investissement",
            "Mandataire d’intermédiaire d’assurance",
            "Transactions sur immeubles et fonds de commerce sans manipulation de fonds",
            "Carte Professionnelle Immobilières N°&nbsp;CPI31012015000001813 délivrée par la CCI de Toulouse")
        + g("Sous le contrôle de l’Autorité de Contrôle Prudentiel et de Résolution – 4 Place de Budapest 75436 PARIS",
            "Assurance Responsabilité Civile Professionnelle conforme au Code des Assurances&nbsp;: N°&nbsp;7400023129",
            "Compagnie ZURICH INSURANCE PLC – 112, avenue de Wagram 75017 PARIS")
    )
    inner = f"""
<div style="height:900px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center">
{conf}
<div style="width:56px;height:1px;background:var(--gold);opacity:.7;margin:34px 0 28px"></div>
<div style="max-width:600px">{legal}</div>
</div>"""
    return shell(8 if d.get('financement') else 7, -1, inner, d)


def build(d=DATA, out="out/maquette.html"):
    pages = [page1(d), page2(d), page3(d), page4(d), page5(d)] + ([page6(d)] if d.get('financement') else []) + [page7(d), page8(d)]
    # titres à ne pas laisser déborder (prénom long) : la taille se réduit à l'impression, sans effet si ça tient
    fit = "<script>document.fonts.ready.then(()=>document.querySelectorAll('[data-fit]').forEach(e=>{const m=e.parentElement.clientWidth;let f=parseFloat(getComputedStyle(e).fontSize);while(e.scrollWidth>m+4&&f>26){f-=0.5;e.style.fontSize=f+'px';}}));</script>"
    html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Stratégie patrimoniale</title><style>{CSS}</style></head><body>{"".join(pages)}{fit}</body></html>'
    open(out, "w", encoding="utf-8").write(html)
    return out


if __name__ == "__main__":
    print(build())

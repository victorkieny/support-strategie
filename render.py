import sys, os
from playwright.sync_api import sync_playwright

base = os.path.dirname(os.path.abspath(__file__))
html = os.path.join(base, "out", "maquette.html")
pdf = os.path.join(base, "out", "Strategie_patrimoniale_maquette.pdf")
# le HTML référence fonts/ et assets/ en relatif : on le sert depuis la racine du dossier
tmp = os.path.join(base, "maquette_render.html")
open(tmp, "w", encoding="utf-8").write(open(html, encoding="utf-8").read())
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 794, "height": 1123})
    pg.goto("file://" + tmp)
    pg.wait_for_timeout(600)
    pg.evaluate("document.fonts.ready")
    pg.pdf(path=pdf, prefer_css_page_size=True, print_background=True)
    b.close()
os.remove(tmp)
print(pdf)

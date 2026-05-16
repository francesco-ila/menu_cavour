import json
import os
import re

# =========================================================
# LOAD JSON
# =========================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================================================
# UTILS
# =========================================================

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


def index_categories(data):
    return {c["nome"]: c for c in data["menu"]["categorie"]}


# =========================================================
# ALLERGENI RENDER
# =========================================================

def render_allergeni(allergeni):
    if not allergeni:
        return ""

    badges = " ".join(
        f'<span class="allergene">{a}</span>' for a in allergeni
    )

    return f'<div class="allergeni">⚠ {badges}</div>'


# =========================================================
# ITEM RENDER
# =========================================================

def render_item(piatto):

    html = '<div class="item">'

    # LEFT
    html += '<div class="item-left">'

    html += f'<div class="item-name">{piatto["nome"]}</div>'

    # INGREDIENTI SOLO SE FLAG ATTIVO
    if piatto.get("ingredienti_espliciti", False):
        ing = ", ".join(piatto.get("ingredienti", []))
        html += f'<div class="ingredients">{ing}</div>'

    # ALLERGENI (SEMPRE VISIBILI)
    html += render_allergeni(piatto.get("allergeni", []))

    html += '</div>'

    # PRICE
    html += f'<div class="item-price">€ {piatto["prezzo"]:.2f}</div>'

    html += '</div>'

    return html


# =========================================================
# CATEGORY RENDER
# =========================================================

def render_category(cat):

    html = '<div class="category">'

    html += f'<div class="category-title">{cat["nome"]}</div>'

    for piatto in cat.get("piatti", []):
        html += render_item(piatto)

    html += '</div>'

    return html


# =========================================================
# PAGE RENDER
# =========================================================

def render_page(group_name, columns, categories, cat_index):

    html = f'<h2 class="group-title">{group_name}</h2>'
    html += f'<div class="grid cols-{columns}">'

    for cat_name in categories:

        cat = cat_index.get(cat_name)
        if not cat:
            continue

        html += render_category(cat)

    html += '</div>'
    return html


# =========================================================
# MAIN
# =========================================================

def render(path="menu.json"):

    data = load_json(path)

    visual = data["layout"]["web"]["visual"]

    if not visual:
        raise ValueError("❌ visual mancante")

    cat_index = index_categories(data)

    os.makedirs("render/pages", exist_ok=True)

    nav_buttons = ""

    for i, group in enumerate(visual):

        columns, name, categories = group
        slug = slugify(name)

        page_html = render_page(name, columns, categories, cat_index)

        with open(f"render/pages/{slug}.html", "w", encoding="utf-8") as f:
            f.write(page_html)

        active = "active" if i == 0 else ""

        nav_buttons += f'''
        <button class="nav-btn {active}" onclick="loadPage('{slug}.html', this)">
            {name}
        </button>
        '''

    with open("render/template.html", "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{NAV}}", nav_buttons)

    os.makedirs("render", exist_ok=True)

    with open("render/index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ Render web completato")


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    render()
import json
import os


# -------------------------
# LOAD
# -------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------
# UTILS
# -------------------------
def slugify(text):
    return text.lower().replace(" ", "-")


def index_categories(data):
    return {c["nome"]: c for c in data["menu"]["categorie"]}


# -------------------------
# RENDER SINGOLA PAGINA
# -------------------------
def render_page(group_name, columns, categories, cat_index):
    html = f'<h2 class="group-title">{group_name}</h2>'
    html += f'<div class="grid cols-{columns}">'

    for cat_name in categories:
        cat = cat_index.get(cat_name)
        if not cat:
            continue

        html += '<div class="category">'
        html += f'<div class="category-title">{cat["nome"]}</div>'

        for piatto in cat["piatti"]:
            html += '<div class="item">'

            html += '<div>'
            html += f'<div class="item-name">{piatto["nome"]}</div>'

            if "ingredienti" in piatto:
                ing = ", ".join(piatto["ingredienti"])
                html += f'<div class="ingredients">{ing}</div>'

            html += '</div>'
            html += f'<div class="item-price">€ {piatto["prezzo"]:.2f}</div>'
            html += '</div>'

        html += '</div>'

    html += '</div>'
    return html


# -------------------------
# MAIN
# -------------------------
def render(path="menu.json"):
    data = load_json(path)
    visual = data.get("visual")

    if not visual:
        raise ValueError("❌ visual mancante")

    cat_index = index_categories(data)

    os.makedirs("render/pages", exist_ok=True)

    nav_buttons = ""

    for i, group in enumerate(visual):
        columns, name, categories = group
        slug = slugify(name)

        page_html = render_page(name, columns, categories, cat_index)

        # salva pagina
        with open(f"render/pages/{slug}.html", "w", encoding="utf-8") as f:
            f.write(page_html)

        active = "active" if i == 0 else ""

        nav_buttons += f'''
        <button class="nav-btn {active}" onclick="loadPage('{slug}.html', this)">
            {name}
        </button>
        '''

    # genera index.html
    with open("render/template.html", "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{NAV}}", nav_buttons)

    with open("render/index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ Multi-page menu generato")


if __name__ == "__main__":
    render()
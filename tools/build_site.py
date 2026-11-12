"""Render cv-data/*.yml into the marked regions of site/index.html.

Usage: python tools/build_site.py [--preview [--no-open] | --dry-run | --check]

Regions look like <!-- cv:NAME --> ... <!-- /cv:NAME -->. Everything between
the markers is replaced; the rest of the HTML is left as is. --preview builds
a copy of the site in out/preview/ and opens it in the browser (site/ is not
touched). --dry-run prints the diff without writing. --check writes nothing
and exits 1 if the file would change.
"""
import calendar
import difflib
import html
import re
import shutil
import sys
import webbrowser
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "cv-data"
INDEX = ROOT / "site" / "index.html"


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def esc(text):
    return html.escape(str(text).strip(), quote=False).replace("'", "&rsquo;")


def on_site(item):
    return not (isinstance(item, dict) and item.get("site") is False)


def month_year(value):
    if value is None:
        return None
    value = str(value)
    if value == "present":
        return "present"
    year, month = value.split("-")
    return f"{calendar.month_name[int(month)]} {year}"


def about(profile):
    s = profile["summary"]
    parts = [s["long"], s["working_style"], s["personality"]]
    return "\n".join(f"      <p>{esc(p)}</p>" for p in parts)


def currently(profile):
    lines = ["      <ul>"]
    for group in profile["currently"]:
        lines.append(f"        <li><span>→</span>{esc(group['text'])}</li>")
        for item in group.get("items", []):
            lines.append(f'        <li class="sub"><span>↳</span>{esc(item)}</li>')
    lines.append("      </ul>")
    lines.append(f'      <p class="mood"><span>status:</span> {esc(profile["status"])}</p>')
    return "\n".join(lines)


def bullets(achievements, indent):
    pad = " " * indent
    return [
        f"{pad}<li><b>{esc(a['title'])}.</b> {esc(a['text'])}</li>"
        for a in achievements
        if on_site(a) and a.get("text")
    ]


def experience(data):
    out = []
    for emp in data["employers"]:
        roles = [r for r in emp["roles"] if on_site(r)]
        if not roles:
            continue
        starts = sorted(str(r["start"]) for r in roles if r.get("start"))
        ends = [r.get("end") for r in roles]
        end = "present" if "present" in ends else max((str(e) for e in ends if e), default=None)
        period = f"{month_year(starts[0])} – {month_year(end)}"
        out.append("    <li>")
        if len(roles) == 1:
            r = roles[0]
            out.append(
                f'      <div class="role"><h3>{esc(emp["company"])}</h3>'
                f"<p>{esc(r['title'])}</p><time>{period}</time></div>"
            )
            out.append("      <ul>")
            out += bullets(r["achievements"], 8)
            out.append("      </ul>")
        else:
            out.append(
                f'      <div class="role"><h3>{esc(emp["company"])}</h3><time>{period}</time></div>'
            )
            for r in roles:
                out.append('      <div class="phase">')
                out.append(f"        <h4>{esc(r['title'])}</h4>")
                out.append("        <ul>")
                out += bullets(r["achievements"], 10)
                out.append("        </ul>")
                out.append("      </div>")
        out.append("    </li>")
    return "\n".join(out)


def chips(items):
    return "".join(f"<li>{esc(i['name'] if isinstance(i, dict) else i)}</li>" for i in items if on_site(i))


def skills(data):
    return "\n".join(
        f'    <div class="card"><h3>{esc(g["name"])}</h3><ul class="chips">{chips(g["skills"])}</ul></div>'
        for g in data["groups"]
        if on_site(g)
    )


def certifications(data):
    cards = []
    for issuer in data["issuers"]:
        if not on_site(issuer):
            continue
        label = issuer.get("site_label", issuer["name"])
        items = [c["code"] for c in issuer["certifications"] if on_site(c)]
        cards.append(f'    <div class="card"><h3>{esc(label)}</h3><ul class="chips">{chips(items)}</ul></div>')
    return "\n".join(cards)


def education(edu, profile):
    cards = []
    for school in edu["education"]:
        lines = "".join(f"<p>{esc(d['field'])} — {esc(d['level'])}</p>" for d in school["degrees"])
        cards.append(f'    <div class="card"><h3>{esc(school["institution"])}</h3>{lines}</div>')
    langs = "".join(
        f"<p>{esc(l['language'])} — {esc(l['level'])}</p>" for l in profile["spoken_languages"]
    )
    cards.append(f'    <div class="card"><h3>Languages</h3>{langs}</div>')
    return "\n".join(cards)


def replace_region(text, name, body):
    pattern = re.compile(rf"(<!-- cv:{name} -->)\r?\n.*?\r?\n?(<!-- /cv:{name} -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"marker cv:{name} not found in {INDEX}")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", text, count=1)


def main():
    profile = load("profile.yml")
    regions = {
        "about": about(profile),
        "currently": currently(profile),
        "experience": experience(load("experience.yml")),
        "skills": skills(load("skills.yml")),
        "certifications": certifications(load("certifications.yml")),
        "education": education(load("education.yml"), profile),
    }
    with open(INDEX, encoding="utf-8", newline="") as f:
        original = f.read()
    newline = "\r\n" if "\r\n" in original else "\n"
    text = original.replace("\r\n", "\n")
    for name, body in regions.items():
        text = replace_region(text, name, body)
    text = text.replace("\n", newline)
    if "--preview" in sys.argv:
        preview = ROOT / "out" / "preview"
        shutil.rmtree(preview, ignore_errors=True)
        shutil.copytree(INDEX.parent, preview)
        with open(preview / "index.html", "w", encoding="utf-8", newline="") as f:
            f.write(text)
        print(f"Preview written to {preview / 'index.html'} (site/ untouched)")
        if "--no-open" not in sys.argv:
            webbrowser.open((preview / "index.html").as_uri())
        return 0
    if text == original:
        print("site/index.html already up to date")
        return 0
    if "--check" in sys.argv:
        print("site/index.html is out of date; run python tools/build_site.py")
        return 1
    if "--dry-run" in sys.argv:
        diff = difflib.unified_diff(
            original.splitlines(), text.splitlines(), "site/index.html", "site/index.html (generated)", lineterm=""
        )
        print("\n".join(diff))
        print("\nDry run: nothing written.")
        return 0
    with open(INDEX, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("site/index.html updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())

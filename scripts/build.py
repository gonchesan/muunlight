"""Genera themes/muunlight.json (Muunlight Dark + Light).

Uso: python scripts/build.py [ruta_salida]
"""
import json, sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "themes" / "muunlight.json"

DARK = dict(
    appearance="dark",
    bg="#222436", chrome="#1e2030", deep="#191a2a", elevated="#2f334d", line="#2f334d",
    fg="#c8d3f5", muted="#828bb8", faint="#444a73", comment="#7a88cf", ignored="#777fab",
    blue="#7cafff", blue2="#60bdff", cyan="#78dbff", teal="#3ad7c7", lteal="#7af8ca",
    green="#c3e88d", yellow="#ffc777", orange="#ff966c", red="#ff757f", error="#ff5370",
    violet="#c4a2ff", pink="#fca7ea", lconst="#ff98a4", regex="#b4f9f8",
    selection="#828bb850", black="#1b1d2b", white="#c8d3f5", bright_white="#ffffff",
)

LIGHT = dict(
    appearance="light",
    bg="#e8ecfb", chrome="#dde2f5", deep="#c5cbe6", elevated="#f4f6fd", line="#d3d9f1",
    fg="#222436", muted="#565f8f", faint="#9aa2c8", comment="#5d68a3", ignored="#8189b0",
    blue="#2e63d6", blue2="#1a65a8", cyan="#0b6c90", teal="#08756c", lteal="#08756c",
    green="#43681a", yellow="#8a5500", orange="#ad4310", red="#c0263e", error="#c0263e",
    violet="#7a4fd6", pink="#a32f88", lconst="#b0334e", regex="#096b66",
    selection="#7cafff40", black="#222436", white="#c5cbe6", bright_white="#e8ecfb",
)


def a(hex_, alpha="ff"):
    return hex_[:7] + alpha if len(hex_) == 7 else hex_


def s(color, style=None, weight=None):
    d = {"color": a(color), "font_style": style, "font_weight": weight}
    return d


def theme(name, p):
    dark = p["appearance"] == "dark"
    # Translúcidos: se distinguen tanto sobre el chrome como sobre superficies elevadas (modales, paleta de comandos)
    hover = a(p["fg"], "14") if dark else a(p["fg"], "12")
    selected = a(p["blue"], "38") if dark else a(p["blue"], "2b")
    status = {}
    for key, col in [("error", p["error"]), ("warning", p["yellow"]), ("info", p["blue2"]),
                     ("hint", p["comment"]), ("success", p["green"]), ("conflict", p["yellow"]),
                     ("created", p["green"]), ("modified", p["blue"]), ("deleted", p["error"]),
                     ("renamed", p["teal"]), ("hidden", p["ignored"]), ("ignored", p["ignored"]),
                     ("predictive", p["muted"]), ("unreachable", p["muted"])]:
        status[key] = a(col)
        status[f"{key}.background"] = a(col, "1a")
        status[f"{key}.border"] = a(col, "66")

    term = {
        "terminal.background": a(p["bg"]),
        "terminal.foreground": a(p["fg"]),
        "terminal.bright_foreground": a(p["bright_white"] if dark else "#000000"),
        "terminal.dim_foreground": a(p["muted"]),
        "terminal.ansi.background": a(p["bg"]),
    }
    ansi = dict(black=p["black"], red=p["red"], green=p["green"], yellow=p["yellow"],
                blue=p["blue"], magenta=p["pink"], cyan=p["cyan"], white=p["white"])
    bright = dict(ansi, black=p["muted"], white=p["bright_white"] if dark else p["fg"])
    for k, v in ansi.items():
        term[f"terminal.ansi.{k}"] = a(v)
        term[f"terminal.ansi.bright_{k}"] = a(bright[k])
        term[f"terminal.ansi.dim_{k}"] = a(v, "aa")

    style = {
        "background.appearance": "opaque",
        "background": a(p["chrome"]),
        "surface.background": a(p["chrome"]),
        "elevated_surface.background": a(p["elevated"]),
        "drop_target.background": a(p["blue"], "33"),
        "border": a(p["deep"]),
        "border.variant": a(p["line"]) if dark else a(p["deep"], "99"),
        "border.focused": a(p["blue"], "aa"),
        "border.selected": a(p["blue"], "aa"),
        "border.transparent": "#00000000",
        "border.disabled": a(p["faint"], "66"),
        "element.background": a(p["elevated"]),
        "element.hover": hover,
        "element.active": selected,
        "element.selected": selected,
        "element.disabled": a(p["faint"], "33"),
        "ghost_element.background": "#00000000",
        "ghost_element.hover": hover,
        "ghost_element.active": selected,
        "ghost_element.selected": selected,
        "ghost_element.disabled": a(p["faint"], "33"),
        "text": a(p["fg"]),
        "text.muted": a(p["muted"]),
        "text.placeholder": a(p["faint"]) if dark else a(p["muted"], "aa"),
        "text.disabled": a(p["faint"]),
        "text.accent": a(p["blue"]),
        "link_text.hover": a(p["cyan"]),
        "icon": a(p["fg"]),
        "icon.muted": a(p["muted"]),
        "icon.disabled": a(p["faint"]),
        "icon.placeholder": a(p["muted"]),
        "icon.accent": a(p["blue"]),
        "status_bar.background": a(p["chrome"]),
        "title_bar.background": a(p["chrome"]),
        "title_bar.inactive_background": a(p["chrome"]),
        "toolbar.background": a(p["bg"]),
        "tab_bar.background": a(p["chrome"]),
        "tab.inactive_background": a(p["chrome"]),
        "tab.active_background": a(p["bg"]),
        "search.match_background": a(p["yellow"], "44"),
        "search.active_match_background": a(p["orange"], "66"),
        "panel.background": a(p["chrome"]),
        "panel.focused_border": a(p["blue"], "aa"),
        "panel.indent_guide": a(p["line"]) if dark else a(p["deep"]),
        "panel.indent_guide_active": a(p["faint"]),
        "panel.indent_guide_hover": a(p["muted"]),
        "pane.focused_border": a(p["blue"], "aa"),
        "pane_group.border": a(p["deep"]),
        "scrollbar.thumb.background": a(p["muted"], "33"),
        "scrollbar.thumb.hover_background": a(p["muted"], "66"),
        "scrollbar.thumb.border": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.track.border": "#00000000",
        "editor.foreground": a(p["fg"]),
        "editor.background": a(p["bg"]),
        "editor.gutter.background": a(p["bg"]),
        "editor.subheader.background": a(p["chrome"]),
        "editor.active_line.background": a(p["line"], "80") if dark else a(p["line"], "aa"),
        "editor.highlighted_line.background": a(p["line"]),
        "editor.line_number": a(p["faint"]),
        "editor.active_line_number": a(p["muted"]),
        "editor.hover_line_number": a(p["muted"]),
        "editor.invisible": a(p["faint"], "aa"),
        "editor.wrap_guide": a(p["line"]) if dark else a(p["deep"], "99"),
        "editor.active_wrap_guide": a(p["faint"]),
        "editor.indent_guide": a(p["line"]) if dark else a(p["deep"], "99"),
        "editor.indent_guide_active": a(p["faint"]),
        "editor.document_highlight.read_background": a(p["blue"], "22"),
        "editor.document_highlight.write_background": a(p["blue"], "33"),
        "editor.document_highlight.bracket_background": a(p["cyan"], "33"),
        "version_control.added": a(p["green"], "aa"),
        "version_control.modified": a(p["blue"], "aa"),
        "version_control.deleted": a(p["error"], "aa"),
        "version_control.conflict": a(p["yellow"], "aa"),
        "version_control.renamed": a(p["teal"], "aa"),
        "version_control.ignored": a(p["ignored"]),
    }
    style.update(term)
    style.update(status)
    style["accents"] = [a(c) for c in (p["blue"], p["violet"], p["cyan"], p["yellow"], p["pink"], p["green"], p["orange"])]
    style["players"] = [{"cursor": a(p["blue"]), "background": a(p["blue"]), "selection": a(p["selection"])}] + [
        {"cursor": a(c), "background": a(c), "selection": a(c, "33")}
        for c in (p["violet"], p["green"], p["yellow"], p["pink"], p["teal"], p["orange"], p["red"])
    ]
    I = "italic"
    style["syntax"] = {
        "attribute": s(p["violet"], I),
        "boolean": s(p["orange"]),
        "comment": s(p["comment"], I),
        "comment.doc": s(p["comment"], I),
        "constant": s(p["lconst"]),
        "constructor": s(p["blue"]),
        "embedded": s(p["fg"]),
        "emphasis": s(p["red"], I),
        "emphasis.strong": s(p["red"], None, 700),
        "enum": s(p["yellow"]),
        "function": s(p["blue"]),
        "function.builtin": s(p["blue2"]),
        "hint": s(p["comment"], I),
        "keyword": s(p["violet"]),
        "label": s(p["yellow"]),
        "link_text": s(p["blue"]),
        "link_uri": s(p["violet"]),
        "namespace": s(p["yellow"]),
        "number": s(p["orange"]),
        "operator": s(p["cyan"]),
        "predictive": s(p["muted"], I),
        "preproc": s(p["violet"]),
        "primary": s(p["fg"]),
        "property": s(p["teal"]),
        "punctuation": s(p["cyan"]),
        "punctuation.bracket": s(p["cyan"]),
        "punctuation.delimiter": s(p["muted"]),
        "punctuation.list_marker": s(p["cyan"]),
        "punctuation.markup": s(p["cyan"]),
        "punctuation.special": s(p["cyan"]),
        "selector": s(p["yellow"]),
        "selector.pseudo": s(p["teal"]),
        "string": s(p["green"]),
        "string.escape": s(p["cyan"]),
        "string.regex": s(p["regex"]),
        "string.special": s(p["orange"]),
        "string.special.symbol": s(p["teal"]),
        "tag": s(p["red"]),
        "text.literal": s(p["cyan"]),
        "title": s(p["green"], None, 700),
        "type": s(p["yellow"]),
        "type.builtin": s(p["yellow"]),
        "variable": s(p["fg"]),
        "variable.member": s(p["teal"]),
        "variable.parameter": s(p["pink"]),
        "variable.special": s(p["red"], I),
        "variant": s(p["yellow"]),
        "diff.plus": s(p["green"]),
        "diff.minus": s(p["error"]),
    }
    return {"name": name, "appearance": p["appearance"], "style": style}


family = {
    "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
    "name": "Muunlight",
    "author": "Gonzalo Sánchez Garay",
    "themes": [theme("Muunlight Dark", DARK), theme("Muunlight Light", LIGHT)],
}

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(family, f, indent=2, ensure_ascii=False)
    f.write("\n")


# contrast check for light syntax colors
def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(x, y):
    l1, l2 = sorted((lum(x), lum(y)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


for label, p in (("dark", DARK), ("light", LIGHT)):
    for k in ("fg", "muted", "comment", "blue", "blue2", "cyan", "teal", "green", "yellow", "orange", "red", "violet", "pink", "lconst", "regex"):
        r = ratio(p[k], p["bg"])
        print(f"{label:5} {k:8} {p[k]} {r:5.2f}{'  <4.5' if r < 4.5 else ''}")

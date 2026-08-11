from __future__ import annotations

import sys
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk

_SRC_DIR = Path(__file__).resolve().parent

def apply_material_icons_font() -> None:
    font_path = _SRC_DIR / "fonts" / "MaterialIcons-Regular.ttf"

    if not font_path.exists():
        print(f"Material Icons font could not be found in path: {font_path}", file=sys.stderr)
        return

    try:
        import ctypes

        fc = ctypes.CDLL("libfontconfig.so.1")

        cfg = fc.FcInitLoadConfigAndFonts()
        ok = fc.FcConfigAppFontAddFile(cfg, str(font_path).encode("utf-8"))
        if not ok:
            print("Could not load material icons font via Fontconfig.")
            return

        if not fc.FcConfigSetCurrent(cfg):
            print(
                "Could not set Fontconfig config as current.",
                file=sys.stderr,
            )
    except Exception as ex:
        print(f"Error on material-icons config: {ex}")


def apply_global_css() -> None:
    try:
        css_path = _SRC_DIR / "style.css"
        if not css_path.exists():
            print(f"style.css file could not be found in path: {css_path}", file=sys.stderr)
            return

        provider = Gtk.CssProvider()
        provider.load_from_path(str(css_path))
        display = Gdk.Display.get_default()
        if display is not None:
            Gtk.StyleContext.add_provider_for_display(
                display,
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )
        else:
            print("Could not apply CSS.", file=sys.stderr)
    except Exception as e:
        print(f"Error applying CSS: {e}", file=sys.stderr)

#!/usr/bin/env python3
"""
simple gtk4 + libadwaita app using a .ui for the main window

runtime requirements (see Dockerfile):
- python3-gi, gir1.2-gtk-4.0, gir1.2-adw-1

run:
  python3 src/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, Gio, GLib
import ui_utils as ui


class SimpleAdwApp(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="com.example.SimpleAdwApp",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

        Adw.init()
        self.selected_header_title = ""

        try:
            ui.apply_material_icons_font()
        except Exception as e:
            # do not break startup on font load failure
            print(f"error applying material icons font at startup: {e}", file=sys.stderr)

    def do_activate(self) -> None:
        existing = self.props.active_window
        if existing is not None:
            existing.present()
            return

        try:
            ui.apply_global_css()
        except Exception as e:
            print(f"error applying global css: {e}", file=sys.stderr)

        # locate the main window ui next to this file
        ui_path = Path(__file__).with_name("main_window.ui")
        builder = Gtk.Builder()
        try:
            builder.add_from_file(str(ui_path))
        except GLib.Error as e:
            print(f"error loading ui '{ui_path}': {e}", file=sys.stderr)
            self.quit()
            return

        window = builder.get_object("main_window")

        window.set_application(self)

        view_stack = builder.get_object("view_stack")
        back_button = builder.get_object("back_button")
        header_title_label = builder.get_object("header_title_label")

        # small helper to update back button visibility
        def update_back_visibility() -> None:
            name = view_stack.props.visible_child_name

            back_button.set_visible(bool(name) and name != "main_menu")
            show_title = bool(name) and name != "main_menu"
            header_title_label.set_visible(show_title)
            header_title_label.set_label(self.selected_header_title or "")

        def on_back_clicked(_btn: Gtk.Button) -> None:
            view_stack.set_visible_child_name("main_menu")
            view_stack.props.visible_child_name = "main_menu"

        back_button.connect("clicked", on_back_clicked)

        view_stack.connect("notify::visible-child-name", lambda *_: update_back_visibility())

        # load pages (.ui + .py) and add to view stack
        try:
            from pages.main_menu.main_menu import MainMenuPage
        except Exception as e:
            print(f"error importing pages: {e}", file=sys.stderr)
            self.quit()
            return

        main_menu = MainMenuPage()
        main_menu.register_pages(view_stack)

        def on_open_page(_page: object, target_page: str, card_title: str) -> None:
            self.selected_header_title = card_title
            view_stack.props.visible_child_name = target_page

        main_menu.connect("open-page", on_open_page)

        # initial back button state
        update_back_visibility()

        window.present()


def main(argv: list[str] | None = None) -> int:
    app = SimpleAdwApp()
    return int(app.run(argv or sys.argv))


if __name__ == "__main__":
    raise SystemExit(main())

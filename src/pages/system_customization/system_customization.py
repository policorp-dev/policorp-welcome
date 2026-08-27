from __future__ import annotations

from pathlib import Path
from typing import Any

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, Gdk


_UI_FILE = str(Path(__file__).with_name("system_customization.ui"))


@Gtk.Template(filename=_UI_FILE)
class SystemCustomizationPage(Gtk.Box):
    __gtype_name__ = "SystemCustomizationPage"

    img_light: Gtk.Picture = Gtk.Template.Child()
    label_light: Gtk.Label = Gtk.Template.Child()
    img_dark: Gtk.Picture = Gtk.Template.Child()
    label_dark: Gtk.Label = Gtk.Template.Child()
    left_panel: Gtk.Box = Gtk.Template.Child()
    right_panel: Gtk.Box = Gtk.Template.Child()

    left_title: Gtk.Label = Gtk.Template.Child()
    left_desc: Gtk.Label = Gtk.Template.Child()
    btn_background: Gtk.Button = Gtk.Template.Child()

    right_title: Gtk.Label = Gtk.Template.Child()
    right_desc: Gtk.Label = Gtk.Template.Child()
    btn_display: Gtk.Button = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.init_template()

        # selected mode: 'light' or 'dark' (light by default)
        self._selected_mode = "light"

        # try to set images from project images folder
        try:
            proj_images = Path(__file__).resolve().parents[2] / "images"
            light_png = proj_images / "light-mode.png"
            dark_png = proj_images / "dark-mode.png"

            if light_png.exists():
                gfile = Gio.File.new_for_path(str(light_png))
                self.img_light.set_file(gfile)
                self.img_light.set_filename(str(light_png))

            if dark_png.exists():
                gfile2 = Gio.File.new_for_path(str(dark_png))
                self.img_dark.set_file(gfile2)
                self.img_dark.set_filename(str(dark_png))
        except Exception:
            # ignore image load errors
            pass

        # connect buttons to simple handlers (pages using this can override signals)
        try:
            self.btn_background.connect("clicked", self._on_btn_background_clicked)
            self.btn_display.connect("clicked", self._on_btn_display_clicked)
        except Exception:
            pass

        # make panels clickable: add gesture controllers
        try:
            left_gst = Gtk.GestureClick.new()
            left_gst.connect("released", lambda *_: self._select_mode("light"))
            self.left_panel.add_controller(left_gst)

            right_gst = Gtk.GestureClick.new()
            right_gst.connect("released", lambda *_: self._select_mode("dark"))
            self.right_panel.add_controller(right_gst)
        except Exception:
            # if gestures unavailable, ignore
            pass

        # apply initial selection
        self._apply_selection()

    def _on_btn_background_clicked(self, *_args) -> None:
        print("Open appearance settings (btn_background clicked)")

    def _on_btn_display_clicked(self, *_args) -> None:
        print("Open display settings (btn_display clicked)")

    def _select_mode(self, mode: str) -> None:
        if mode not in ("light", "dark"):
            return
        self._selected_mode = mode
        self._apply_selection()

    def _apply_selection(self) -> None:
        # ensure only the selected panel has the 'selected' style class
        try:
            lp_ctx = self.left_panel.get_style_context()
            rp_ctx = self.right_panel.get_style_context()
            if self._selected_mode == "light":
                lp_ctx.add_class("selected")
                rp_ctx.remove_class("selected")
            else:
                rp_ctx.add_class("selected")
                lp_ctx.remove_class("selected")
        except Exception:
            pass


def build() -> Gtk.Widget:
    return SystemCustomizationPage()

from __future__ import annotations

from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio


_UI_FILE = str(Path(__file__).with_name("admin_password.ui"))

@Gtk.Template(filename=_UI_FILE)
class AdminPasswordPage(Gtk.Box):
    __gtype_name__ = "AdminPasswordPage"

    security_image: Gtk.Picture = Gtk.Template.Child()
    left_info_label: Gtk.Label = Gtk.Template.Child()
    entry_password: Gtk.Widget = Gtk.Template.Child()
    entry_confirm: Gtk.Widget = Gtk.Template.Child()
    btn_save: Gtk.Button = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.init_template()
        self.btn_save.set_sensitive(False)
        self.entry_password.connect("notify::text", self._on_password_changed)
        self.entry_confirm.connect("notify::text", self._on_password_changed)
        try:
            proj_images = Path(__file__).resolve().parents[2] / "images"
            security_medium_png = proj_images / "security-medium.png"

            self.security_image.set_filename(str(security_medium_png))
            self.security_image.set_file(Gio.File.new_for_path(str(security_medium_png)))
        except Exception as ex:
            print(f"Error loading image : {ex}")

    def _on_password_changed(self, *_args) -> None:
        password = self.entry_password.get_text().strip()
        confirm = self.entry_confirm.get_text().strip()
        self.btn_save.set_sensitive(bool(password) and password == confirm)

def build() -> Gtk.Widget:
    # legacy helper kept for backward compatibility
    return AdminPasswordPage()

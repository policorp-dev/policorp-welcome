from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from typing import Any

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk


_UI_FILE = str(Path(__file__).with_name("users_management.ui"))


def _on_configure_users_clicked(*_args: object) -> None:
    try:
        subprocess.Popen(["gnome-control-center", "system", "users"], start_new_session=True)
    except OSError as error:
        print(f"Não foi possível abrir as configurações de usuários: {error}", file=sys.stderr)


@Gtk.Template(filename=_UI_FILE)
class UsersManagementPage(Gtk.Box):
    __gtype_name__ = "UsersManagementPage"

    users_image: Gtk.Picture = Gtk.Template.Child()
    configure_users_button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.init_template()

        self.configure_users_button.connect("clicked", _on_configure_users_clicked)

        image_path = Path(__file__).resolve().parents[2] / "images" / "tasks-users.png"
        if image_path.exists():
            self.users_image.set_file(Gio.File.new_for_path(str(image_path)))


def build() -> Gtk.Widget:
    return UsersManagementPage()
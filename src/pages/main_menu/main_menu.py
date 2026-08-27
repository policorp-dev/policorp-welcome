from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, Gio, Adw, GObject
from pages.admin_password.admin_password import AdminPasswordPage
from pages.system_customization.system_customization import SystemCustomizationPage

_UI_FILE = str(Path(__file__).with_name("main_menu.ui"))

@Gtk.Template(filename=_UI_FILE)
class MainMenuPage(Gtk.Box):
    __gtype_name__ = "MainMenuPage"
    __gsignals__ = {
        "open-page": (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
    }

    img_overlay: Gtk.Picture = Gtk.Template.Child()
    linkedin_avatar: Adw.Avatar = Gtk.Template.Child()
    youtube_avatar: Adw.Avatar = Gtk.Template.Child()
    password_title: Gtk.Label = Gtk.Template.Child()
    gst_password_window: Gtk.GestureClick = Gtk.Template.Child()
    gst_system_customization: Gtk.GestureClick = Gtk.Template.Child()
    video_link: Gtk.Button = Gtk.Template.Child()
    system_customization_title: Gtk.Label = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.init_template()
        self.gst_password_window.connect("released", self.on_password_window_released)
        try:
            self.gst_system_customization.connect("released", self.on_system_customization_released)
        except Exception:
            pass

        try:
            images_dir = Path(__file__).parents[2] / "images"

            bg_path = images_dir / "background-header.png"
            if bg_path.exists():
                self.img_overlay.set_filename(str(bg_path))

            def _set_avatar_image(widget: Adw.Avatar, filename: str) -> None:
                try:
                    path = images_dir / filename
                    if path.exists():
                        gfile = Gio.File.new_for_path(str(path))
                        texture = Gdk.Texture.new_from_file(gfile)
                        widget.set_custom_image(texture)
                except Exception:
                    # silent: just skip setting image
                    pass

            _set_avatar_image(self.linkedin_avatar, "linkedin.png")
            _set_avatar_image(self.youtube_avatar, "youtube.png")
        except Exception:
            # do not break page construction
            pass

        # example of conditional visibility if optional ids exist
        use_a = os.environ.get("USE_COND_A", "").strip() in ("1", "true", "True", "A")
        try:
            btn_cond_a = self.get_template_child(self.__class__, "btn_cond_a")
            btn_cond_b = self.get_template_child(self.__class__, "btn_cond_b")
            btn_cond_a.set_visible(use_a)
            btn_cond_b.set_visible(not use_a)
        except Exception:
            # ignore if ids do not exist in .ui
            pass

    def card_titles(self) -> Dict[str, str]:
        mapping = {
            "gst_password_window": self.password_title
            , "gst_system_customization": self.system_customization_title
        }
        titles: Dict[str, str] = {}
        for key, label in mapping.items():
            titles[key] = (label.get_label() or "").strip()
        return titles

    def register_pages(self, view_stack: Adw.ViewStack) -> None:
        page = view_stack.add_titled(self, "main_menu", "Principal")
        page.set_icon_name("go-home-symbolic")

        admin_page = AdminPasswordPage()
        view_stack.add_titled(admin_page, "admin_password", "Administrador")

        sys_page = SystemCustomizationPage()
        view_stack.add_titled(sys_page, "system_customization", "Customização do Sistema")

    def on_password_window_released(self, *_args: object) -> None:
        title = (self.password_title.get_label() or "").strip()
        self.emit("open-page", "admin_password", title)

    def on_system_customization_released(self, *_args: object) -> None:
        title = (self.system_customization_title.get_label() or "").strip()
        self.emit("open-page", "system_customization", title)


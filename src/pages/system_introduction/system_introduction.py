from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk


_UI_FILE = str(Path(__file__).with_name("system_introduction.ui"))
_VIDEO_FILES = (
    "policorp-tour.mp4",
    "policorp-tour-oem.mp4",
    "policorp-tour-compaq.mp4",
    "policorp-tour-positivo.mp4",
    "policorp-tour-vaio.mp4",
)
_MANUAL_PATH = "/opt/manual.pdf"
_FALLBACK_MANUAL_PATH = "/usr/share/policorp-linux-welcome/files/Manual-Policorp-Linux-Not-OEM.pdf"


class PolicorpImageAspectFrame(Gtk.AspectFrame):
    __gtype_name__ = "PolicorpImageAspectFrame"

    def do_measure(
        self, orientation: Gtk.Orientation, for_size: int
    ) -> tuple[int, int, int, int]:
        if orientation == Gtk.Orientation.VERTICAL and for_size >= 0:
            height = round(for_size / self.get_ratio())
            return 0, height, -1, -1

        measurement = Gtk.AspectFrame.do_measure(self, orientation, for_size)
        if orientation == Gtk.Orientation.HORIZONTAL:
            return measurement[0], measurement[1], -1, -1
        return measurement


def _video_command() -> list[str]:
    for filename in _VIDEO_FILES:
        video_path = f"/opt/{filename}"
        if os.path.isfile(video_path):
            browser = shutil.which("x-www-browser")
            if browser is None:
                raise FileNotFoundError("O aplicativo x-www-browser não está disponível.")
            return [browser, video_path]

    raise FileNotFoundError("Nenhum arquivo de vídeo foi encontrado em /opt/.")


def _manual_command() -> list[str]:
    if os.path.isfile(_MANUAL_PATH):
        launcher = shutil.which("manual-launcher")
        if launcher is None:
            raise FileNotFoundError("O aplicativo manual-launcher não está disponível.")
        return [launcher]

    if not os.path.isfile(_FALLBACK_MANUAL_PATH):
        raise FileNotFoundError("O arquivo PDF do manual não foi encontrado.")

    opener = shutil.which("xdg-open")
    if opener is None:
        raise FileNotFoundError("O aplicativo xdg-open não está disponível.")
    return [opener, _FALLBACK_MANUAL_PATH]


def _open_video() -> None:
    subprocess.Popen(_video_command())


def _open_manual() -> None:
    subprocess.Popen(_manual_command())


@Gtk.Template(filename=_UI_FILE)
class SystemIntroductionPage(Gtk.Box):
    __gtype_name__ = "SystemIntroductionPage"

    video_image: Gtk.Picture = Gtk.Template.Child()
    pdf_image: Gtk.Picture = Gtk.Template.Child()
    video_button: Gtk.Button = Gtk.Template.Child()
    pdf_button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.init_template()
        self.video_button.connect("clicked", self.on_video_button_clicked)
        self.pdf_button.connect("clicked", self.on_pdf_button_clicked)

        images_dir = Path(__file__).resolve().parents[2] / "images"
        for picture, filename in (
            (self.video_image, "video-manual.png"),
            (self.pdf_image, "pdf-manual.png"),
        ):
            image_path = images_dir / filename
            if image_path.exists():
                picture.set_file(Gio.File.new_for_path(str(image_path)))

    def on_video_button_clicked(self, *_args: object) -> None:
        self._run_action(_open_video, "Não foi possível abrir o vídeo.")

    def on_pdf_button_clicked(self, *_args: object) -> None:
        self._run_action(_open_manual, "Não foi possível abrir o manual.")

    def _run_action(self, action: Any, heading: str) -> None:
        try:
            action()
        except OSError as error:
            root = self.get_root()
            parent = root if isinstance(root, Gtk.Window) else None
            dialog = Adw.MessageDialog.new(parent, heading, str(error))
            dialog.add_response("close", "Fechar")
            dialog.set_default_response("close")
            dialog.set_close_response("close")
            dialog.present()


def build() -> Gtk.Widget:
    return SystemIntroductionPage()
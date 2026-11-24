from __future__ import annotations

import math
import os
import subprocess
import threading
from pathlib import Path
from typing import Any

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk


_UI_FILE = str(Path(__file__).with_name("system_specifications.ui"))
_NOT_AVAILABLE = "Não disponível"
_VALUE_IDS = {
    "distribution": "distro_value",
    "kernel": "kernel_value",
    "company": "company_value",
    "cpu_model": "cpu_model_value",
    "cpu_cores": "cpu_cores_value",
    "architecture": "architecture_value",
    "motherboard": "motherboard_value",
    "memory": "memory_value",
    "graphics": "graphics_value",
    "root_directory": "root_directory_value",
    "filesystem": "filesystem_value",
    "capacity": "capacity_value",
}
_STORAGE_SEGMENTS = (
    # Keep these colors in sync with the legacy storage bar in data/scss/_geting-started.scss.
    # Used: #87A556, Free: #C2D3A6, Other: #484848.
    ("used", "Usado", (135 / 255, 165 / 255, 86 / 255)),
    ("free", "Livre", (194 / 255, 211 / 255, 166 / 255)),
    ("other", "Outros", (72 / 255, 72 / 255, 72 / 255)),
)


def _read_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return ""


def _command_output(arguments: list[str]) -> str:
    try:
        result = subprocess.run(
            arguments,
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "LC_ALL": "C", "LANG": "C"},
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _df_size_gb(value: str) -> tuple[float, str] | None:
    if not value:
        return None

    if value[-1].isdigit():
        try:
            size_gb = float(value.replace(",", "."))
        except ValueError:
            return None
        if not math.isfinite(size_gb) or size_gb < 0:
            return None
        return size_gb, f"{value.replace(',', '.')} GB"

    unit = value[-1].upper()
    try:
        number = float(value[:-1].replace(",", "."))
    except ValueError:
        return None

    unit_factors = {
        "B": 1 / 1024**3,
        "K": 1 / 1024**2,
        "M": 1 / 1024,
        "G": 1,
        "T": 1024,
        "P": 1024**2,
        "E": 1024**3,
    }
    factor = unit_factors.get(unit)
    if factor is None or number < 0:
        return None

    size_gb = number * factor
    if not math.isfinite(size_gb):
        return None
    if unit == "G":
        display_value = value[:-1].replace(",", ".")
    elif unit == "M" and number.is_integer():
        display_value = str(int(number) / 1024)
    else:
        display_value = f"{size_gb:.1f}"
    return size_gb, f"{display_value} GB"


def _lscpu_values() -> dict[str, str]:
    values: dict[str, str] = {}
    for line in _command_output(["lscpu"]).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values.setdefault(key.strip().lower(), value.strip())
    return values


def _memory_size() -> str:
    for line in _command_output(["free", "-b"]).splitlines():
        fields = line.split()
        if fields and fields[0] == "Mem:" and len(fields) > 1:
            try:
                memory = int(fields[1])
            except ValueError:
                return _NOT_AVAILABLE
            if round(memory / 1024 / 1024) < 1024:
                return f"{round(memory / 1_000_000, 1):.1f} MB"
            return f"{round(memory / 1_000_000_000, 1):.1f} GB"
    return _NOT_AVAILABLE


def _graphics_name() -> str:
    for line in _command_output(["lspci"]).splitlines():
        if "VGA" in line:
            _device, separator, name = line.partition("controller:")
            if separator and name.strip():
                return name.strip()
    return _NOT_AVAILABLE


def _oem_profile() -> str:
    output = _command_output(["dpkg", "-l"])
    installed = set()
    for line in output.splitlines():
        fields = line.split()
        if len(fields) > 1 and fields[0] == "ii":
            installed.add(fields[1].lower())
    if any("oem-vaio" in package for package in installed):
        return "vaio"
    if any("oem-positivo" in package for package in installed):
        return "positivo"
    return "policorp"


def _company_name() -> str:
    profile = _oem_profile()
    if profile == "vaio":
        return "VAIO"
    if profile == "positivo":
        return "Positivo Tecnologia SA"

    vendor = _read_file("/sys/class/dmi/id/sys_vendor")
    if "VAIO" in vendor.upper():
        return "VAIO"
    if "POSITIVO" in vendor.upper():
        return "Positivo Tecnologia SA"
    return vendor or "Policorp Tecnologia"


def _storage_values() -> dict[str, Any]:
    root_directory = _NOT_AVAILABLE
    filesystem = _NOT_AVAILABLE
    for line in _command_output(["mount"]).splitlines():
        partition, separator, details = line.partition(" on / type ")
        if separator:
            root_directory = partition.strip() or _NOT_AVAILABLE
            filesystem = details.partition(" (")[0].strip() or _NOT_AVAILABLE
            break

    output = _command_output(["df", "-h", "/"])
    lines = output.splitlines()
    if len(lines) < 2:
        return {
            "root_directory": root_directory,
            "filesystem": filesystem,
            "capacity": _NOT_AVAILABLE,
            "storage_statuses": None,
            "storage_proportions": None,
        }

    fields = lines[1].split()
    if len(fields) < 5:
        return {
            "root_directory": root_directory,
            "filesystem": filesystem,
            "capacity": _NOT_AVAILABLE,
            "storage_statuses": None,
            "storage_proportions": None,
        }

    if root_directory == _NOT_AVAILABLE:
        root_directory = fields[0]

    sizes = [_df_size_gb(value) for value in fields[1:4]]
    if any(size is None for size in sizes):
        return {
            "root_directory": root_directory,
            "filesystem": filesystem,
            "capacity": _NOT_AVAILABLE,
            "storage_statuses": None,
            "storage_proportions": None,
        }

    total, used, free = (size[0] for size in sizes if size is not None)
    capacity_display, used_display, free_display = (size[1] for size in sizes if size is not None)
    try:
        used_percent = int(fields[4].removesuffix("%"))
    except ValueError:
        return {
            "root_directory": root_directory,
            "filesystem": filesystem,
            "capacity": _NOT_AVAILABLE,
            "storage_statuses": None,
            "storage_proportions": None,
        }
    if not 0 <= used_percent <= 100:
        return {
            "root_directory": root_directory,
            "filesystem": filesystem,
            "capacity": _NOT_AVAILABLE,
            "storage_statuses": None,
            "storage_proportions": None,
        }

    if total == 0:
        return {
            "root_directory": root_directory,
            "filesystem": filesystem,
            "capacity": capacity_display,
            "storage_statuses": None,
            "storage_proportions": None,
        }

    other = total - used - free
    other_percent = int((other / total) * 100)
    free_percent = 100 - (used_percent + other_percent)
    statuses = {
        "used": f"Usado: {used_display} ({used_percent}%)",
        "free": f"Livre: {free_display} ({free_percent}%)",
        "other": f"Outros: {other:.1f} GB ({other_percent}%)",
    }
    return {
        "root_directory": root_directory,
        "filesystem": filesystem,
        "capacity": capacity_display,
        "storage_statuses": statuses,
        "storage_proportions": (used_percent / 100, free_percent / 100, other_percent / 100),
    }


def collect_system_specifications() -> dict[str, Any]:
    cpu = _lscpu_values()
    values = {
        "distribution": _command_output(["lsb_release", "-ds"]).strip('"') or _NOT_AVAILABLE,
        "kernel": _command_output(["uname", "-r"]) or _NOT_AVAILABLE,
        "company": _company_name(),
        "cpu_model": cpu.get("model name") or _NOT_AVAILABLE,
        "cpu_cores": cpu.get("cpu(s)") or _NOT_AVAILABLE,
        "architecture": cpu.get("architecture") or _NOT_AVAILABLE,
        "motherboard": _read_file("/sys/devices/virtual/dmi/id/board_name") or _NOT_AVAILABLE,
        "memory": _memory_size(),
        "graphics": _graphics_name(),
    }
    values.update(_storage_values())
    return {
        key: value if key in ("storage_proportions", "storage_statuses") else value or _NOT_AVAILABLE
        for key, value in values.items()
    }


def _storage_subtitle(
    statuses: dict[str, str],
    proportions: tuple[float, float, float],
) -> str:
    normalized = tuple(
        value if math.isfinite(value) and value > 0 else 0.0
        for value in proportions
    )
    total = sum(normalized)
    if total <= 0:
        return _NOT_AVAILABLE

    cell_count = 30
    exact_counts = [value / total * cell_count for value in normalized]
    cell_counts = [math.floor(value) for value in exact_counts]
    remaining_cells = cell_count - sum(cell_counts)
    for index in sorted(
        range(len(exact_counts)),
        key=lambda item: exact_counts[item] - cell_counts[item],
        reverse=True,
    )[:remaining_cells]:
        cell_counts[index] += 1

    def color_hex(color: tuple[float, float, float]) -> str:
        return "#" + "".join(f"{round(channel * 255):02x}" for channel in color)

    bar = "".join(
        f'<span foreground="{color_hex(color)}">{"█" * count}</span>'
        for count, (_key, _label, color) in zip(cell_counts, _STORAGE_SEGMENTS)
        if count
    )
    lines = [f'<span font_family="monospace">{bar}</span>']
    for key, _label, color in _STORAGE_SEGMENTS:
        value = GLib.markup_escape_text(str(statuses.get(key) or _NOT_AVAILABLE))
        lines.append(
            f'<span foreground="{color_hex(color)}">■</span> '
            f"{value}"
        )
    return "\n".join(lines)


@Gtk.Template(filename=_UI_FILE)
class SystemSpecificationsPage(Gtk.Box):
    __gtype_name__ = "SystemSpecificationsPage"

    distro_value: Adw.ActionRow = Gtk.Template.Child()
    kernel_value: Adw.ActionRow = Gtk.Template.Child()
    company_value: Adw.ActionRow = Gtk.Template.Child()
    cpu_model_value: Adw.ActionRow = Gtk.Template.Child()
    cpu_cores_value: Adw.ActionRow = Gtk.Template.Child()
    architecture_value: Adw.ActionRow = Gtk.Template.Child()
    motherboard_value: Adw.ActionRow = Gtk.Template.Child()
    memory_value: Adw.ActionRow = Gtk.Template.Child()
    graphics_value: Adw.ActionRow = Gtk.Template.Child()
    root_directory_value: Adw.ActionRow = Gtk.Template.Child()
    filesystem_value: Adw.ActionRow = Gtk.Template.Child()
    capacity_value: Adw.ActionRow = Gtk.Template.Child()
    allocated_row: Adw.ActionRow = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.init_template()

        self._value_rows = {
            name: getattr(self, widget_id)
            for name, widget_id in _VALUE_IDS.items()
        }
        threading.Thread(target=self._load_values, daemon=True).start()

    def _load_values(self) -> None:
        try:
            values = collect_system_specifications()
        except Exception:
            values = {key: _NOT_AVAILABLE for key in _VALUE_IDS}
            values["storage_statuses"] = None
            values["storage_proportions"] = None
        GLib.idle_add(self._update_values, values)

    def _update_values(self, values: dict[str, Any]) -> bool:
        for name, row in self._value_rows.items():
            text = values.get(name) or _NOT_AVAILABLE
            row.set_subtitle(text)
        statuses = values.get("storage_statuses")
        proportions = values.get("storage_proportions")
        has_storage_data = statuses is not None and proportions is not None
        if has_storage_data:
            self.allocated_row.set_subtitle(_storage_subtitle(statuses, tuple(proportions)))
        else:
            self.allocated_row.set_subtitle(_NOT_AVAILABLE)
        return GLib.SOURCE_REMOVE


def build() -> Gtk.Widget:
    return SystemSpecificationsPage()
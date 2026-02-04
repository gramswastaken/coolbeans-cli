from typing import List
import subprocess
import shutil
import os
import re

from coolbeans.utils import locations


def rofi_theme_switcher(da_list: List[str]):
    tlist = subprocess.Popen(
        ["echo", "\n".join(t for t in da_list)], stdout=subprocess.PIPE, text=True
    )
    result = subprocess.check_output(
        ["rofi", "-dmenu", "-sep", "\n", "-i", "-p", "Themes", "-disable-history"],
        stdin=tlist.stdout,
        text=True,
    ).strip()

    swap_theme_syms(result)


def swap_theme_syms(sel_theme: str):
    current_theme_dir = locations.currents_dir / "theme"

    # Remove existing symlink or directory
    if current_theme_dir.is_symlink() or current_theme_dir.exists():
        if current_theme_dir.is_dir() and not current_theme_dir.is_symlink():
            shutil.rmtree(current_theme_dir)
        else:
            current_theme_dir.unlink()
    # Create new symlink: current/theme -> /path/to/theme-name
    current_theme_dir.symlink_to(
        locations.themes_dir / ugly(sel_theme), target_is_directory=True
    )


def themes_list() -> List[str]:
    themes = [pretty(theme) for theme in os.listdir(locations.themes_dir)]
    return themes


def pretty(text) -> str:
    # replace hyphens with spaces, capitalize first letter of each word
    text = re.sub(r"(^|-)([a-z])", lambda m: m.group(1) + m.group(2).upper(), text)
    text = re.sub(r"-", " ", text)
    return text


# I wish I had good rofi bindings
def ugly(text):
    text = re.sub(r" ", "-", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1-\2", text)
    text = text.lower()
    return text

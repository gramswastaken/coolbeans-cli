import os
import sys
import re
import subprocess
import shutil
import typer
from typing import Annotated, List

import coolbeans.utils.locations as locations
from coolbeans.defaults import defaulttheme

cli = typer.Typer(pretty_exceptions_enable=False)
theme = typer.Typer(pretty_exceptions_enable=False)
cli.add_typer(theme)


@theme.command("theme_switcher")
def theme_switcher(
    sel_theme: Annotated[str, typer.Argument()] = defaulttheme,
    list_themes: Annotated[bool, typer.Option("--list")] = False,
    rofi: Annotated[bool, typer.Option("--rofi")] = False,
):
    dalist: List[str] = themes_list()

    if rofi:
        rofi_theme_switcher(dalist)
        sys.exit(0)
    if list_themes:
        print(*dalist, sep="\n")
        sys.exit(0)
    if sel_theme not in dalist:
        print("umm this one aint here boss o_O")
        sys.exit(1)

    swap_theme_syms(sel_theme)


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


if __name__ == "__main__":
    cli()
# @cli.command()
# def clipboard(): ...
#
#
# @cli.command()
# def emoji(): ...
#
#
# @cli.command()
# def screenshot(): ...
#
#
# @cli.command()
# def screen_record(): ...
#
#
# @cli.command()
# def main():
#    print("hello")

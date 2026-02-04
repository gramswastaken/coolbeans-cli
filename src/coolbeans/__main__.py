import subprocess
import sys
import typer
from typing import Annotated, List
import datetime
import os

from coolbeans.defaults import defaulttheme
from coolbeans.utils.locations import screenshots_cache_dir, screenshots_dir
from coolbeans.cmds.theme_switch import (
    themes_list,
    rofi_theme_switcher,
    swap_theme_syms,
)

cli = typer.Typer(pretty_exceptions_enable=False)
theme = typer.Typer(pretty_exceptions_enable=False)
capture = typer.Typer(pretty_exceptions_enable=False)
cli.add_typer(theme)
cli.add_typer(capture)


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


@capture.command("screenshot")
def screenshot(
    region: Annotated[bool, typer.Option("--region", "-r")] = False,
    freeze: Annotated[bool, typer.Option("--freeze", "-f")] = False,
    save: Annotated[bool, typer.Option("--save", "-s")] = False,
    edit: Annotated[bool, typer.Option("--edit", "-e")] = False,
):
    cap_reg: bytes | None = None

    if freeze:
        subprocess.run(["hyprpicker", "-rz"])

    if region:
        cap_reg = subprocess.check_output(["slurp"])

    if cap_reg is None:
        # this gets both screens
        sc_data = subprocess.check_output(["grim", "-"])
    else:
        sc_data = subprocess.check_output(["grim", "-g", cap_reg.strip(), "-"])

    subprocess.run(["wl-copy"], input=sc_data)

    if edit:
        swappy = subprocess.Popen(
            ["swappy", "-f", "-"], stdin=subprocess.PIPE, start_new_session=True
        )
        assert swappy.stdin is not None, sys.exit(1)
        swappy.stdin.write(sc_data)
        swappy.stdin.close()

    dest = screenshots_cache_dir / datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    screenshots_cache_dir.mkdir(exist_ok=True, parents=True)
    dest.write_bytes(sc_data)

    if save:
        save_dest = (
            screenshots_dir / datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        ).with_suffix(".png")
        save_dest.parent.mkdir(exist_ok=True, parents=True)
        save_dest.write_bytes(sc_data)
        os.remove(dest)

    # if fullscreen then capture and send to wlcopy and save to cache
    # get user input for next part
    # open it in swappy, or save to somewhere
    # cs has a custom notification thing, they send a message through dbus to it and get the user response
    # For now all of those functions are explicit


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

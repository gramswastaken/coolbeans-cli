from pathlib import Path
import os


# cursed operator overloading
config_base = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
coolbeans_config_dir = config_base / "coolbeans"
themes_dir = Path("/home/anu/workspace/coolbeans/themes/")
currents_dir = Path("/home/anu/workspace/coolbeans/current/")

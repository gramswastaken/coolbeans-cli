from pathlib import Path
import os


# cursed operator overloading
config_base = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
coolbeans_config_dir = config_base / "coolbeans"
themes_dir = Path("/home/anu/workspace/coolbeans/themes/")
currents_dir = Path("/home/anu/workspace/coolbeans/current/")

cache_base = Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache"))
coolbeans_cache_dir = cache_base / "coolbeans"
screenshots_cache_dir = coolbeans_cache_dir / "screenshots"

pictures_base = Path(Path.home() / "pics")
screenshots_dir = pictures_base / "screenshots"

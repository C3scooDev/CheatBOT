"""
CheatBot: avvio minimizzato in system tray.
Carica config, registra hotkey se presente, avvia tray.
"""
import sys
import os

# Se packed con PyInstaller, la working directory è quella dell'exe
if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))

from config import load
import hotkey
from tray import run as run_tray


def main() -> None:
    cfg = load()
    hotkey_str = (cfg.get("HOTKEY") or "").strip().lower()
    if hotkey_str:
        hotkey.register(hotkey_str)
    run_tray()


if __name__ == "__main__":
    main()

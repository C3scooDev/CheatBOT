"""
Lettura e scrittura di config.txt (chiave=valore).
Il file si trova nella stessa cartella dell'exe o nella cartella corrente in sviluppo.
"""
import os
import sys

CONFIG_FILENAME = "config.txt"

# Chiavi supportate
KEYS = ("GEMINI_API_KEY", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "HOTKEY")


def get_config_dir() -> str:
    """Cartella dove cercare config.txt: stessa dell'exe se packed, altrimenti cwd."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.getcwd()


def get_config_path() -> str:
    return os.path.join(get_config_dir(), CONFIG_FILENAME)


def load() -> dict:
    """Carica config.txt e restituisce un dict chiave -> valore (stringhe)."""
    path = get_config_path()
    result = {k: "" for k in KEYS}
    if not os.path.isfile(path):
        return result
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KEYS:
                result[key] = value
    return result


def save_key(key: str, value: str) -> None:
    """Aggiorna una chiave nel config e riscrive il file."""
    if key not in KEYS:
        raise ValueError(f"Chiave non valida: {key}")
    path = get_config_path()
    current = load()
    current[key] = value
    lines = [f"{k}={current[k]}\n" for k in KEYS]
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

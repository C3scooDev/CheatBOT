"""
Registrazione hotkey globale (libreria keyboard) e callback che esegue
screenshot -> Gemini -> Telegram in un thread separato.
Errori inviati solo su Telegram, nessuna notifica tray (stealth).
"""
import threading
from typing import Callable, Optional

import keyboard

from config import load, save_key
from screenshot import take_screenshot
from gemini_client import get_answer_from_image
from telegram_client import send_message


_remove_hotkey: Optional[Callable[[], None]] = None


def _send_error_to_telegram(token: str, chat_id: str, msg: str) -> None:
    """Invia messaggio di errore su Telegram (silenzioso su host)."""
    if token and chat_id:
        try:
            send_message(token, chat_id, f"CheatBot — {msg}")
        except Exception:
            pass


def _run_pipeline() -> None:
    """Esegue screenshot -> Gemini -> Telegram. Errori solo su Telegram, niente tray."""
    cfg = load()
    api_key = (cfg.get("GEMINI_API_KEY") or "").strip()
    token = (cfg.get("TELEGRAM_BOT_TOKEN") or "").strip()
    chat_id = (cfg.get("TELEGRAM_CHAT_ID") or "").strip()
    if not api_key or not token or not chat_id:
        return
    try:
        screenshot_bytes = take_screenshot()
    except Exception as e:
        _send_error_to_telegram(token, chat_id, f"Screenshot: {e}")
        return
    try:
        answer = get_answer_from_image(api_key, screenshot_bytes)
    except Exception as e:
        _send_error_to_telegram(token, chat_id, f"Gemini: {e}")
        return
    if not answer:
        _send_error_to_telegram(token, chat_id, "Gemini non ha restituito una risposta.")
        return
    err = send_message(token, chat_id, answer)
    if err:
        _send_error_to_telegram(token, chat_id, f"Telegram: {err}")


def _on_hotkey_pressed() -> None:
    """Chiamato alla pressione dell'hotkey: avvia il pipeline in un thread."""
    threading.Thread(target=_run_pipeline, daemon=True).start()


def register(hotkey_str: str) -> bool:
    """
    Registra l'hotkey globale. Se già presente, la rimuove e ri-registra.
    hotkey_str: es. "f12" o "ctrl+shift+a" (minuscolo).
    Restituisce True se la registrazione è andata a buon fine.
    """
    global _remove_hotkey
    unregister()
    if not hotkey_str or not hotkey_str.strip():
        return False
    hotkey_str = hotkey_str.strip().lower()
    try:
        _remove_hotkey = keyboard.add_hotkey(hotkey_str, _on_hotkey_pressed)
        return True
    except Exception:
        return False


def unregister() -> None:
    """Rimuove l'hotkey globale se registrata."""
    global _remove_hotkey
    if _remove_hotkey is not None:
        try:
            _remove_hotkey()
        except Exception:
            pass
        _remove_hotkey = None


def set_error_callback(_callback: Optional[Callable[[str], None]]) -> None:
    """Ignorato: gli errori vanno solo su Telegram (stealth)."""
    pass


def record_hotkey() -> str:
    """
    Blocca finché l'utente non preme una combinazione di tasti, poi restituisce
    la stringa hotkey (es. "ctrl+shift+a"). Da chiamare da un thread secondario.
    """
    return keyboard.read_hotkey(suppress=True).lower()

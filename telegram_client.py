"""
Invio messaggio a Telegram tramite Bot API.
"""
from typing import Optional

import requests


def send_message(token: str, chat_id: str, text: str) -> Optional[str]:
    """
    Invia un messaggio di testo al chat_id tramite il bot.
    Restituisce None in caso di successo, altrimenti una stringa di errore.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=data, timeout=15)
        if r.status_code != 200:
            try:
                info = r.json()
                return info.get("description", r.text)
            except Exception:
                return r.text or f"HTTP {r.status_code}"
        return None
    except Exception as e:
        return str(e)

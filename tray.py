"""
Icona system tray (pystray) con menu: Registra tasto, Esci.
Gestisce la registrazione del tasto in un thread e notifiche.
"""
import threading
from typing import Optional

from PIL import Image
import pystray

from config import load, save_key
import hotkey


def _make_icon_image() -> Image.Image:
    """Crea un'icona 64x64 semplice per la system tray."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    # Cerchio/quadrato con iniziale C (CheatBot)
    margin = 8
    draw.rectangle([margin, margin, size - margin, size - margin], fill=(66, 133, 244), outline=(255, 255, 255, 200))
    # Lettera C semplificata
    draw.arc([margin + 6, margin + 6, size - margin - 6, size - margin - 6], start=60, end=300, fill=(255, 255, 255), width=4)
    return img


_icon_ref: Optional[pystray.Icon] = None


def _on_register(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    def _record():
        try:
            icon.notify("Premi il tasto da usare.", "CheatBot")
            key = hotkey.record_hotkey()
            save_key("HOTKEY", key)
            hotkey.register(key)
            icon.notify(f"Tasto registrato: {key}", "CheatBot")
        except Exception as e:
            icon.notify(f"Errore: {e}", "CheatBot")

    threading.Thread(target=_record, daemon=True).start()


def _on_quit(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    hotkey.unregister()
    icon.stop()


def run() -> None:
    """Avvia l'icona in system tray (bloccante). Nessuna notifica tray per errori (stealth)."""
    global _icon_ref
    image = _make_icon_image()
    menu = pystray.Menu(
        pystray.MenuItem("Registra tasto", _on_register, default=True),
        pystray.MenuItem("Esci", _on_quit),
    )
    _icon_ref = pystray.Icon("CheatBot", image, "CheatBot", menu)
    _icon_ref.run()

"""
Screenshot dello schermo intero. Restituisce bytes PNG per invio a Gemini.
"""
from PIL import ImageGrab
import io


def take_screenshot() -> bytes:
    """Cattura lo schermo intero e restituisce l'immagine in PNG come bytes."""
    img = ImageGrab.grab()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

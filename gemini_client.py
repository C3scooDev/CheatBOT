"""
Invio immagine a Gemini (vision) e estrazione della risposta testuale.
Risposta richiesta: solo la risposta corretta, senza spiegazioni.
"""
import io
from typing import Optional

import google.generativeai as genai
from PIL import Image


PROMPT = (
    "Guarda questa immagine. Rispondi SOLO con la risposta corretta, "
    "senza spiegazioni o testo aggiuntivo. Una sola riga se possibile."
)


def get_answer_from_image(api_key: str, image_png_bytes: bytes) -> Optional[str]:
    """
    Invia l'immagine (PNG bytes) a Gemini e restituisce il testo della risposta.
    In caso di errore restituisce None; le eccezioni possono essere propagate.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    img = Image.open(io.BytesIO(image_png_bytes))
    response = model.generate_content([PROMPT, img])
    if not response or not response.text:
        return None
    return response.text.strip()

# CheatBot

Tool Windows che in background (solo icona in system tray) alla pressione di un tasto fa screenshot, lo invia a Gemini per la risposta corretta e manda il risultato su Telegram.

## Sviluppo (Linux / Arch–Manjaro)

Su sistemi con Python “externally managed” (es. Arch, Manjaro) usa un virtual environment:

```bash
cd /path/to/CheatBot
python -m venv .venv
source .venv/bin/activate   # su Windows: .venv\Scripts\activate
pip install -r requirements.txt
# oppure senza attivare il venv:
# .venv/bin/python3 -m pip install -r requirements.txt
```

Poi per eseguire: `python main.py`. Per la build dell’exe usa Windows (vedi sotto).

## Utilizzo (utente finale)

1. Metti **CheatBot.exe** e **config.txt** nella stessa cartella.
2. Modifica **config.txt**: inserisci `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`. Opzionale: `HOTKEY` (es. `f12`) oppure lascialo vuoto e registra il tasto dal menu.
3. Avvia **CheatBot.exe**. L’app parte senza finestra (solo icona nella system tray).
4. Tasto destro sull’icona: **Registra tasto** (per impostare/modificare l’hotkey) oppure **Esci**.
5. Quando premi l’hotkey: viene fatto uno screenshot, Gemini elabora l’immagine e la risposta viene inviata su Telegram.

## Build dell’exe

- **Requisiti:** Python 3.10+, Windows.
- Dalla cartella del progetto:
  ```bat
  pip install -r requirements.txt
  pip install pyinstaller
  pyinstaller --onefile --noconsole --name CheatBot main.py
  ```
- L’eseguibile sarà in `dist\CheatBot.exe`. Copia `config.txt` (o rinomina `config.txt.example`) nella cartella `dist\` insieme all’exe.

In alternativa usa **build.bat** (doppio clic o da cmd nella cartella CheatBot).

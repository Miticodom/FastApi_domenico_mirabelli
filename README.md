# Catalogo Libri (FastAPI)

Mini progetto con path parameters, query parameters, request body e validazione.

## Avvio con VS Code (consigliato)
Poi vai su http://127.0.0.1:8000/docs

## Avvio (Windows / PowerShell)
    .\avvia.ps1

Se PowerShell blocca lo script, lancia una volta sola:
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Poi apri http://127.0.0.1:8000/docs e prova gli endpoint con "Try it out".

## Avvio manuale
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    uvicorn main:app --reload

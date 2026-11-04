# Script di avvio: crea il venv (solo la prima volta), installa le librerie e fa partire il server.
# Uso: tasto destro su questo file -> "Esegui con PowerShell", oppure da terminale:  .\avvia.ps1

if (-not (Test-Path ".venv")) {
    Write-Host "Creo l'ambiente virtuale..."
    python -m venv .venv
}

.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Write-Host ""
Write-Host "Server su http://127.0.0.1:8000  (documentazione: http://127.0.0.1:8000/docs)"
uvicorn main:app --reload

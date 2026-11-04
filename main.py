from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Catalogo Libri")


# ---------------------------------------------------------------
# PDF 4 - REQUEST BODY: i modelli Pydantic descrivono la forma dei dati
# ---------------------------------------------------------------
class Genere(str, Enum):  # PDF 2 - Enum: solo questi valori sono ammessi
    romanzo = "romanzo"
    saggio = "saggio"
    poesia = "poesia"


class Libro(BaseModel):
    titolo: str = Field(min_length=1, max_length=100)
    autore: str
    genere: Genere
    prezzo: float = Field(gt=0)             # PDF 5: gt=0 -> deve essere > 0
    iva: float | None = None                # opzionale (None come default)
    descrizione: str | None = None


# "Database" finto: una lista in memoria (si resetta a ogni riavvio)
libri_db: list[dict] = [
    {"id": 1, "titolo": "Il Gattopardo", "autore": "Tomasi di Lampedusa", "genere": "romanzo", "prezzo": 14.5},
    {"id": 2, "titolo": "Se questo e un uomo", "autore": "Primo Levi", "genere": "saggio", "prezzo": 12.0},
    {"id": 3, "titolo": "Ossi di seppia", "autore": "Eugenio Montale", "genere": "poesia", "prezzo": 9.9},
]


@app.get("/")  # PDF 1: l'app minima
async def root():
    return {"message": "Catalogo libri attivo"}


# ---------------------------------------------------------------
# PDF 3 + 5 - QUERY PARAMETERS (con validazione tramite Query)
# ---------------------------------------------------------------
@app.get("/libri")
async def lista_libri(
    skip: int = 0,                                              # default -> opzionale
    limit: Annotated[int, Query(gt=0, le=50)] = 10,             # validato: 1..50
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,  # ricerca nel titolo
):
    risultati = libri_db
    if q:
        risultati = [l for l in risultati if q.lower() in l["titolo"].lower()]
    return risultati[skip: skip + limit]


# ---------------------------------------------------------------
# PDF 2 - ORDINE DEI PATH: i percorsi fissi vanno PRIMA di quelli variabili
# ---------------------------------------------------------------
@app.get("/libri/economici")
async def libri_economici(max_prezzo: float = 10):
    return [l for l in libri_db if l["prezzo"] <= max_prezzo]


# PDF 2 + 5 - PATH PARAMETER tipizzato e validato (id >= 1)
@app.get("/libri/{libro_id}")
async def dettaglio_libro(libro_id: Annotated[int, Path(title="ID del libro", ge=1)]):
    for l in libri_db:
        if l["id"] == libro_id:
            return l
    return {"errore": "Libro non trovato"}


# PDF 2 - Enum nel path: /generi/romanzo, /generi/saggio...
@app.get("/generi/{genere}")
async def libri_per_genere(genere: Genere):
    return [l for l in libri_db if l["genere"] == genere.value]


# ---------------------------------------------------------------
# PDF 4 - POST con request body
# ---------------------------------------------------------------
@app.post("/libri")
async def crea_libro(libro: Libro):
    nuovo = libro.model_dump()                      # da oggetto Pydantic a dizionario
    nuovo["id"] = max(l["id"] for l in libri_db) + 1
    if libro.iva:
        nuovo["prezzo_con_iva"] = round(libro.prezzo * (1 + libro.iva / 100), 2)
    libri_db.append(nuovo)
    return nuovo


# ---------------------------------------------------------------
# PDF 5 - Modello Pydantic per GRUPPI di query parameters + extra="forbid"
# ---------------------------------------------------------------
class FiltriRicerca(BaseModel):
    model_config = {"extra": "forbid"}              # parametri non previsti -> errore
    limit: int = Field(10, gt=0, le=50)
    offset: int = Field(0, ge=0)
    ordina_per: str = "titolo"


@app.get("/ricerca")
async def ricerca(filtri: Annotated[FiltriRicerca, Query()]):
    ordinati = sorted(libri_db, key=lambda l: l.get(filtri.ordina_per, ""))
    return ordinati[filtri.offset: filtri.offset + filtri.limit]

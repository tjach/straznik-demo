"""STRAŻNIK — prosty silnik oceny ryzyka transakcji.

Materiał szkoleniowy (AI-Assisted SDLC). Logika jest celowo uproszczona
i fikcyjna — to nie jest produkcyjny system antyfraud. Chodzi o to, żeby
pipeline miał co budować i testować, a kod był czytelny dla nie-developerów.
"""
from __future__ import annotations

import datetime

# Progi decyzyjne (spójne z case study):
#   score < PROG_WERYFIKUJ        -> PRZEPUŚĆ
#   PROG_WERYFIKUJ..PROG_ZABLOKUJ -> WERYFIKUJ
#   score > PROG_ZABLOKUJ         -> ZABLOKUJ
PROG_WERYFIKUJ = 40
PROG_ZABLOKUJ = 70

_PL_WARIANTY = {"PL", "POL", "POLSKA"}


def _norm_kraj(v) -> str:
    """Normalizuje zapis kraju (dane od klienta bywają niespójne: PL/Polska/POL)."""
    s = str(v or "").strip().upper()
    return "PL" if s in _PL_WARIANTY else s


def _bool(v) -> bool:
    """Akceptuje warianty z bałaganu w danych: tak/TAK/true/1/Y."""
    return str(v or "").strip().lower() in {"tak", "true", "1", "t", "y", "yes"}


def _godzina(tx: dict):
    """Godzina z pola 'godzina' albo wyłuskana z 'czas_transakcji'."""
    if tx.get("godzina") not in (None, ""):
        try:
            return int(tx["godzina"])
        except (ValueError, TypeError):
            pass
    czas = str(tx.get("czas_transakcji", "")).strip()
    if " " in czas:
        czesc = czas.split(" ")[1]
        if ":" in czesc:
            try:
                return int(czesc.split(":")[0])
            except ValueError:
                return None
    return None


def _czy_weekend(tx: dict) -> bool:
    """Zwraca True, gdy data z 'czas_transakcji' wypada w sobotę lub niedzielę.

    Akceptuje formaty z datą na początku, np. 'YYYY-MM-DD HH:MM:SS' lub samo
    'YYYY-MM-DD'. Gdy pole jest brakujące lub nieparsowalne — zwraca False.
    """
    czas = str(tx.get("czas_transakcji", "")).strip()
    if not czas:
        return False
    data_str = czas.split(" ")[0]
    try:
        data = datetime.date.fromisoformat(data_str)
        return data.weekday() >= 5  # 5 = sobota, 6 = niedziela
    except (ValueError, TypeError):
        return False


def _float(v):
    """Liczba zmiennoprzecinkowa, tolerująca pusty string i przecinek dziesiętny."""
    if v in (None, ""):
        return None
    try:
        return float(str(v).replace(",", "."))
    except (ValueError, TypeError):
        return None


def ocen_transakcje(tx: dict) -> dict:
    """Zwraca {'score', 'decyzja', 'powody'} dla pojedynczej transakcji.

    Pojedynczy sygnał rzadko wystarcza — dopiero złożenie kilku podnosi ryzyko.
    Dzięki temu np. klient płacący z zagranicy (sama niezgodność kraju) nie jest
    od razu blokowany (unikamy fałszywych pozytywów).
    """
    score = 0
    powody: list[str] = []

    kraj_karty = _norm_kraj(tx.get("kraj_karty"))
    kraj_ip = _norm_kraj(tx.get("kraj_ip"))
    if kraj_karty and kraj_ip and kraj_karty != kraj_ip:
        score += 35
        powody.append(f"Kraj karty ({kraj_karty}) różny od kraju IP ({kraj_ip})")

    try:
        licz = int(tx.get("liczba_transakcji_10min") or 0)
    except (ValueError, TypeError):
        licz = 0
    if licz >= 5:
        score += 30
        powody.append(f"{licz} transakcji w 10 minut — możliwe card testing")

    ratio = _float(tx.get("kwota_vs_srednia_klienta"))
    if ratio is not None and ratio >= 4:
        score += 20
        powody.append(f"Kwota {ratio:.1f}x wyższa niż średnia klienta")

    godz = _godzina(tx)
    if godz is not None and 2 <= godz <= 5 and not _bool(tx.get("karta_obecna")):
        score += 15
        powody.append("Transakcja w nocy z kartą nieobecną")

    if _bool(tx.get("nowy_odbiorca")):
        score += 10
        powody.append("Nowy odbiorca")

    if _czy_weekend(tx):
        score += 10
        powody.append("Transakcja w weekend")

    score = min(score, 100)

    if score < PROG_WERYFIKUJ:
        decyzja = "PRZEPUŚĆ"
    elif score <= PROG_ZABLOKUJ:
        decyzja = "WERYFIKUJ"
    else:
        decyzja = "ZABLOKUJ"

    if not powody:
        powody.append("Brak sygnałów ryzyka")

    return {"score": score, "decyzja": decyzja, "powody": powody}

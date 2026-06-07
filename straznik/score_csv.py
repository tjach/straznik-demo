"""Demo: przepuszcza próbkę transakcji przez STRAŻNIKA i podsumowuje decyzje.

Uruchom: python -m straznik.score_csv [ścieżka_do_csv]
Domyślnie czyta data/transakcje-sample.csv.
"""
import csv
import os
import sys
from collections import Counter

from straznik.scoring import ocen_transakcje


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    decyzje = Counter()
    fraudy = 0
    wychwycone = 0
    for r in rows:
        wynik = ocen_transakcje(r)
        decyzje[wynik["decyzja"]] += 1
        if str(r.get("czy_fraud", "")).strip().lower() == "tak":
            fraudy += 1
            if wynik["decyzja"] in ("ZABLOKUJ", "WERYFIKUJ"):
                wychwycone += 1

    print(f"Transakcji: {len(rows)}")
    for d in ("PRZEPUŚĆ", "WERYFIKUJ", "ZABLOKUJ"):
        print(f"  {d}: {decyzje.get(d, 0)}")
    if fraudy:
        print(f"Fraudów w danych: {fraudy} | wychwyconych (WERYFIKUJ/ZABLOKUJ): {wychwycone}")
        print("Uwaga: to celowo NIE jest 100% — pokazuje napięcie fałszywy pozytyw vs negatyw.")


if __name__ == "__main__":
    domyslna = os.path.join(os.path.dirname(__file__), "..", "data", "transakcje-sample.csv")
    main(sys.argv[1] if len(sys.argv) > 1 else domyslna)

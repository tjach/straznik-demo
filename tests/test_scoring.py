"""Testy silnika STRAŻNIK — to one uruchamiają się w pipeline (build → test)."""
from straznik.scoring import ocen_transakcje


def test_legalna_zwykla_przepusc():
    tx = {"kraj_karty": "PL", "kraj_ip": "PL", "liczba_transakcji_10min": 1,
          "kwota_vs_srednia_klienta": 1.0, "godzina": 13, "karta_obecna": "nie",
          "nowy_odbiorca": "nie"}
    w = ocen_transakcje(tx)
    assert w["decyzja"] == "PRZEPUŚĆ"
    assert w["score"] < 40


def test_card_testing_zablokuj():
    tx = {"kraj_karty": "PL", "kraj_ip": "BR", "liczba_transakcji_10min": 14,
          "kwota_vs_srednia_klienta": 1.2, "godzina": 3, "karta_obecna": "nie",
          "nowy_odbiorca": "tak"}
    w = ocen_transakcje(tx)
    assert w["decyzja"] == "ZABLOKUJ"
    assert w["score"] > 70
    assert any("card testing" in p for p in w["powody"])


def test_klient_na_wakacjach_nie_jest_blokowany():
    # Sama niezgodność kraju nie wystarcza, by zablokować — unikamy false positive.
    tx = {"kraj_karty": "PL", "kraj_ip": "ES", "liczba_transakcji_10min": 1,
          "kwota_vs_srednia_klienta": 1.4, "godzina": 14, "karta_obecna": "nie",
          "nowy_odbiorca": "nie"}
    w = ocen_transakcje(tx)
    assert w["decyzja"] == "PRZEPUŚĆ"


def test_przypadek_graniczny_weryfikuj():
    tx = {"kraj_karty": "PL", "kraj_ip": "RU", "liczba_transakcji_10min": 1,
          "kwota_vs_srednia_klienta": 1.0, "godzina": 12, "karta_obecna": "nie",
          "nowy_odbiorca": "tak"}
    w = ocen_transakcje(tx)
    assert w["decyzja"] == "WERYFIKUJ"


def test_takeover_na_granicy_weryfikuj():
    # Score 55: niezgodność kraju (35) + kwota mocno odstająca (20).
    # Przy domyślnym progu (PROG_ZABLOKUJ=70) -> WERYFIKUJ.
    # To celowy przypadek do Ćwiczenia 3: obniżenie progu do 50 zamieni go
    # w ZABLOKUJ i ten test się wywróci (pokazuje koszt zaostrzenia progu).
    tx = {"kraj_karty": "PL", "kraj_ip": "RU", "liczba_transakcji_10min": 1,
          "kwota_vs_srednia_klienta": 8.0, "godzina": 12, "karta_obecna": "nie",
          "nowy_odbiorca": "nie"}
    w = ocen_transakcje(tx)
    assert w["decyzja"] == "WERYFIKUJ"
    assert 50 < w["score"] <= 70


def test_duzy_legalny_zakup_przepusc():
    tx = {"kraj_karty": "PL", "kraj_ip": "PL", "liczba_transakcji_10min": 1,
          "kwota_vs_srednia_klienta": 6.0, "godzina": 11, "karta_obecna": "nie",
          "nowy_odbiorca": "nie"}
    w = ocen_transakcje(tx)
    assert w["decyzja"] == "PRZEPUŚĆ"


def test_powody_zawsze_obecne():
    w = ocen_transakcje({})
    assert w["powody"]


def test_warianty_kraju_sa_normalizowane():
    # "Polska" i "PL" to ten sam kraj — nie powinno być sygnału niezgodności.
    tx = {"kraj_karty": "Polska", "kraj_ip": "PL", "liczba_transakcji_10min": 1}
    w = ocen_transakcje(tx)
    assert all("różny od kraju IP" not in p for p in w["powody"])

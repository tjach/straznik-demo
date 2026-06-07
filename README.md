# STRAŻNIK — serwis scoringu ryzyka + pipeline CI/CD

> Materiał szkoleniowy (AI-Assisted SDLC, Dzień 2). Mały, czytelny serwis oceny ryzyka transakcji z gotowym pipeline'em GitHub Actions i automatycznym przeglądem PR przez agenta AI. Wszystko fikcyjne (klient „Ryś Pay", projekt „STRAŻNIK"). Stack darmowy, bez płatnych zależności.
>
> **To repo jest szablonem.** Na szkoleniu każdy uczestnik tworzy własną kopię przez **Use this template** (instrukcja w preworku Dnia 2) i pracuje na niej niezależnie — może psuć i naprawiać bez wpływu na innych.

## Co tu jest

```
straznik/scoring.py     # logika: transakcja -> score, decyzja, powody
straznik/score_csv.py   # demo: przepuszcza próbkę danych przez scoring
tests/test_scoring.py   # testy (to one biegną w pipeline)
data/                   # próbka danych transakcji (oznaczona)
.github/workflows/ci.yml# pipeline: build -> test -> deploy(atrapa)
.coderabbit.yaml        # opcjonalna konfiguracja AI review
```

## Uruchomienie testów lokalnie

```
pip install -r requirements.txt
pytest -q
```

Demo na próbce danych:

```
python -m straznik.score_csv
```

## Jak działa pipeline

Plik `.github/workflows/ci.yml` uruchamia się przy każdym `push` na `main` i przy każdym **pull requeście**:

1. **BUILD** — konfiguracja Pythona i instalacja zależności.
2. **TEST** — `pytest` na testach z `tests/`.
3. **DEPLOY** — atrapa (tylko na `main`); na produkcję w szkoleniu nie wdrażamy.

Na repo **publicznym** minuty GitHub Actions są darmowe — dlatego repo (Twoje, z szablonu) robimy publiczne.

## Automatyczny przegląd PR przez AI (CodeRabbit)

Review kodu robi **CodeRabbit** — agent AI, który komentuje pull requesty. Na repo publicznym jest **darmowy** i **nie wymaga żadnego klucza API**.

Konfiguracja (raz):

1. Wejdź na **[coderabbit.ai](https://coderabbit.ai)** (albo od razu [github.com/apps/coderabbitai](https://github.com/apps/coderabbitai)) i zainstaluj go jako **GitHub App** — każdy uczestnik na **swoim** repo, na własnym prywatnym koncie GitHub (darmowo na repo publicznym).
2. Opcjonalnie zostaw `.coderabbit.yaml` (jest w repo) — bez niego działają ustawienia domyślne.
3. Od teraz każdy nowy PR dostaje automatyczny komentarz-przegląd od CodeRabbit.

Alternatywnie można użyć **GitHub Copilot code review** — też działa na repo publicznym, bez dodatkowego klucza.

## Dla uczestników — Ćwiczenie 3 (na WŁASNYM repo)

Każdy ma swoje repo z tego szablonu (założone w preworku) — wasza piaskownica, można psuć. Na nim:

1. **Zepsujcie** test (zmiana progu `PROG_ZABLOKUJ`) → czerwony pipeline.
2. **Naprawcie** → znów zielono.
3. **Dodajcie nową regułę** scoringu z pomocą Cursora (+ test) → PR → pipeline i przegląd CodeRabbit.
4. Interpretujcie jak PM.

Pełna instrukcja krok po kroku: `CWICZENIE-3-pipeline.md`.

## Uwaga

To uproszczony materiał dydaktyczny, nie produkcyjny system antyfraud. Logika scoringu jest celowo prosta i czytelna dla osób nietechnicznych.

## Licencja

MIT — patrz plik [`LICENSE`](LICENSE).

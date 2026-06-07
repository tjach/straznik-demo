# Ćwiczenie 3 — Twój pipeline: zepsuj, napraw, rozbuduj

> Karta dla uczestnika. Pracujecie **w parach**, na **WŁASNYM repo** (założonym z szablonu w preworku). To wasza piaskownica — **można psuć, o to chodzi**. Czas: ~35–40 min pracy, potem wspólne omówienie. CodeRabbit (AI-recenzenta) podpinacie wspólnie z prowadzącym tuż przed ćwiczeniem — to kilka kliknięć.

## Po co to robicie

Pipeline budował prowadzący — teraz wy nim **żyjecie**: psujecie, patrzycie jak świeci na czerwono, naprawiacie i dokładacie własną funkcję. Na koniec przejdziecie pełną pętlę „od pomysłu do (prawie) produkcji" na swoim repo.

## Krok 1 — ZEPSUJ test (zobacz czerwony pipeline)

1. W swoim repo otwórz `straznik/scoring.py` (ołówek).
2. Zmień `PROG_ZABLOKUJ = 70` na `PROG_ZABLOKUJ = 50`. **Commit** prosto na `main`.
3. Wejdź w **Actions** — pipeline robi się **czerwony**. Padnie test `test_takeover_na_granicy_weryfikuj`.
4. Zobacz dlaczego: transakcja graniczna (55 pkt), która przy progu 70 szła do **WERYFIKUJ**, przy 50 wpada w **ZABLOKUJ**. Obniżyliście próg → blokujecie ostrzej.

## Krok 2 — NAPRAW (znów zielono)

1. Wróćcie do `PROG_ZABLOKUJ = 70`. **Commit**.
2. Pipeline znów **zielony**. Wniosek: pipeline pilnuje, żeby zmiana nie weszła „po cichu" wbrew oczekiwaniom zapisanym w testach.

## Krok 3 — DODAJ nową regułę (z Cursorem) i otwórz PR

Wymyślcie nową regułę ryzyka (np. „transakcja w weekend podnosi ryzyko", „kwota powyżej 5000", „kraj IP z listy ryzykownych").

**Spróbuj sam.** Najpierw sami napiszcie Cursorowi, czego chcecie — pełnym zdaniem, z kontekstem (który plik, jak ma się zachować, że ma dopisać test i nie zepsuć istniejących). Dopiero potem zerknijcie na wzorzec.

<details markdown="1"><summary>🔓 Jeśli chcesz modelowy prompt — kliknij (ale spróbuj najpierw sam)</summary>

> Jesteś inżynierem pracującym nad serwisem oceny ryzyka transakcji w pliku `straznik/scoring.py`. Dodaj nową regułę scoringu: [opisz regułę, np. „jeśli transakcja jest w weekend — sobota/niedziela wg pola czas_transakcji — podnieś score o 10 i dopisz powód 'Transakcja w weekend'"].
>
> Wymagania:
> 1. regułę dodaj w funkcji `ocen_transakcje`, spójnie z istniejącym stylem (dodaje punkty do `score` i dopisuje czytelny powód do listy `powody`);
> 2. **obsłuż brak lub niepoprawne dane** — kod nie może się wywalić, gdy pola nie ma albo ma zły format;
> 3. dopisz **test** w `tests/test_scoring.py`, który sprawdza, że reguła działa, i nadaj mu opisową nazwę;
> 4. **nie zepsuj istniejących testów**;
> 5. pokaż zmienione fragmenty obu plików i krótko wyjaśnij po polsku, co zmieniłeś.

</details>

Otwórzcie **pull request** ze swoją zmianą i patrzcie na dwie rzeczy: czy **pipeline** jest zielony (czy nowy test przechodzi) i co napisał **CodeRabbit** w komentarzu do PR.

## Interpretacja jak PM

- **Krok 1:** „jedna liczba" (próg) to decyzja biznesowa, nie techniczna — przesuwa, ilu prawdziwych klientów zablokujecie.
- **Krok 3:** właśnie przeszliście pełną pętlę: pomysł → kod (z AI) → test → pipeline → review. To jest „od kodu do produkcji" w pigułce.
- **CodeRabbit:** trafił w sedno waszej zmiany, czy się czepił bez powodu (fałszywy alarm)? Czy zaufalibyście tylko jemu, czy chcecie jeszcze człowieka?

## Punkty kontrolne (powinniście mieć)

- [ ] czerwony pipeline po kroku 1 (i rozumiecie, który test padł i czemu)
- [ ] zielony po naprawie (krok 2)
- [ ] PR z nową regułą: nowy test + komentarz CodeRabbit (krok 3)

## Jeśli utkniecie

- Pipeline nie rusza? Odświeżcie po ~30 s; sprawdźcie, że Actions są włączone w waszym repo.
- Cursor „nie wie", gdzie dodać regułę? Wskażcie mu plik: „edytuj funkcję `ocen_transakcje` w `straznik/scoring.py`".
- Test od Cursora czerwony? Przeczytajcie komunikat — często to drobiazg (zła nazwa pola). Poproście Cursora: „popraw test, żeby przechodził".
- Żółte ostrzeżenie o „Node.js 20" w logach to **nie błąd** — pipeline i tak jest zielony.
- Nie tkwijcie dłużej niż 3 minuty — machnijcie na prowadzącego.

## Na wspólne omówienie przynieście

- co padło w kroku 1 i jak to zrozumieliście po ludzku,
- jaką regułę dodaliście i czy pipeline ją przyjął,
- jedno zdanie: czy bardziej ufacie zielonym testom, czy komentarzowi AI — i dlaczego.

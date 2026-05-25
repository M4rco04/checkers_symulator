# Checkers AI Engine ♟️

Zaawansowany silnik do gry w warcaby, napisany w języku Python. Projekt implementuje podejście obiektowe do reprezentacji stanu gry oraz zawiera zestaw klasycznych i nowoczesnych algorytmów sztucznej inteligencji służących do wyboru najlepszego ruchu.

## 🚀 Możliwości i Algorytmy

Projekt pozwala na zestawienie ze sobą różnych algorytmów AI (AI vs AI) lub grę gracza przeciwko maszynie. Zaimplementowano następujące algorytmy decyzyjne:

* **MinMax** – klasyczny algorytm przeszukiwania drzewa gry.
* **Negamax z cięciami Alfa-Beta** – zoptymalizowana wersja algorytmu MinMax, znacznie redukująca przestrzeń przeszukiwania.
* **Iterative Deepening** – algorytm typu *Anytime*, który stopniowo zwiększa głębokość przeszukiwania, co pozwala na przerwanie obliczeń w dowolnym momencie (np. po upływie limitu czasu), przy jednoczesnym zachowaniu najlepszego znalezionego ruchu.
* **Monte Carlo Tree Search (MCTS)** – algorytm heurystyczny oparty na losowych symulacjach (rollouts) z balansem eksploracji i eksploatacji za pomocą wzoru UCB1.

## 🧠 Heurystyka i Optymalizacje

* **Move Ordering:** Silnik inteligentnie sortuje możliwe ruchy przed ich analizą, znacznie przyspieszając działanie cięć Alfa-Beta. Premiowane są m.in. bicia, tworzenie łańcuchów obronnych, ruchy w stronę krawędzi oraz awanse na damki.
* **Ocena planszy:** Funkcja ewaluacyjna bierze pod uwagę nie tylko układ materiału (zwykłe pionki i damki), ale również stopień awansu pionków, bezpieczeństwo (pozycje przy krawędzi) oraz czas/liczbę ruchów, aby unikać przedłużających się gier.
* **Obsługa remisów:** Wbudowana zasada 40 ruchów bez bicia (zapobiegająca nieskończonym pętlom w fazie gry końcowej).

## 🛠️ Architektura Kodu

* `algorithm/` – implementacje algorytmów przeszukujących.
* `heuristic/` – funkcje oceniające stan planszy (klasyczna oraz sigmoidalna pod MCTS).
* `representation/` – klasy odpowiedzialne za logikę i zasady gry (`Board`, `Move`, `Pawn`, `Problem`). Obejmują m.in. logikę wielokrotnych bić oraz generowanie dozwolonych ruchów.
* `view/` – interfejs użytkownika (rysowanie planszy).

## 💻 Uruchomienie

Aby uruchomić silnik i rozpocząć grę, uruchom plik główny:

Gra dla dwóch graczy:
```bash
python main.py -o PvP
```

Gra z AI:
```bash
python main.py -o PvAI
```

Gra AI z AI:
```bash
python main.py -o AIvAI
```

Wszystkie ustawienia znajdują się w pliku **settings.json**
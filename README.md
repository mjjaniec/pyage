# Job scheduling problems - Computation intelligence

## Team

Michał Janiec <mjjaniec@gmail.com>

Wojciech Krzystek <wojciech.krzystek@gmail.com>

## Problem flow shop
http://www.flowshop.mfbiz.pl/sformulowanie-problemu.php

### Wejscie algorytmu:
* P - liczba procesorów (wynika z macierzy - patrz niżej)
* J - liczba zadań jw.
* `time_matrix` - macierz czasów potrzebnych do wykonania zadań: `time_matrix[processor][job]` to czas wykonania
 zadania `job` na procesorze `processor`. 

### Wyjście algorytmu:
* makespan - łączny czas przetworzenia wszystkich zadań
* permutacja zadań w której wykonaja się najszybciej
* tabela wyników - `results` - `results[processor][job]` to czas zejścia zadania `job` z processora `processor`

### Przykładowe problemy:
`input_data` zawiera benchmarki problemu flowshop, nie są znane dokładne ich rozwiązania, a jedynie widełki.
Mimo to świetnie się nadają do testowania aplikacji.


## Flowshop in pyage

### Implementacja
Implementacja problemu w pyage składa się z implementacji kilku interfejsów:

* `PerumtationGenotype` Definiuje osobnika - zawiera
 * `self.permutation` = list of int -  geny - tutaj permutacja zadań
 * `self.fitness` = float - fitness

* `Initializer` Inicjuje osobniki - w tym wypadku losowymi permutacjami o zadanej długości

* `FlowhsopEvaluation` Oblicza makespan dla tangeo osbnika w oparciu o macierz czasów. `fitness = -makespan`
 * `time_matrix` jest parametrem konstruktora
 * `def compute_makespan(self, permutation, compute_time_matrix = False)` - wylicza makespan i tabele wynków 

* `PermutationMutation` Wykonuje mutacje osobnika
 * `count` - parametr konstrukora
 * `def mutate(self, genotype)` - dokonuje `count` zamian losowych elementów permutacji
 
* `PermutationCrossover` Reprodukcja
 * `def cross(self, p1, p2)` - oblicza potomstwo osobników `p1`, `p2`, następujące działanie: znajduje minimalny set zamian elementów permutacji `p1`, taki że ich wykonanie na `p1` daje permutację `p2`. następnie wykonuje te zamiany z prawdopodobieństwem 1/2 (dla każdej zamiany z osobna), otrzymując w ten sposób permutację będącą "w połowie drogi" od `p1` do `p2`


### Uruchomienie
`flowshop_conf.py` zawiera podstawową konfigurację do uruchomienia - narazie lokalnie.
R
ozwiązuje nie wielki problem - pierwszy z pliku `tai20x5.txt`
Obliczenia są kończone po upływie 10 sekund - nalpeszy znaleźiony wynik jest zwracany

## Random solver - as reference solution
Aby pokazać że rozwiązanie dizała dobrze warto pokazać że daje lepsze wyniki niż 
losowe przeszukiwanie przestrzeni rozwiązań. Taką strategię implementuje `random_solver.py`
Operuje na tym samym problemie, i również przerywa obliczenia po upływie 10 sekund.

## Wyniki

Dla przykładowego problem (jw i 10 sekund obliczeń):
 
* algorytm evolucyjny: makespan: 1297 (zwraca prawie zawsze ten sam wynik, może jakieś optimum lokalne?)
* random: makespan: ~ 1312







 
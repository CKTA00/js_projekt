## Raport z wykonania projektu
#### Wstęp
#### Testy
#### Spełnione założenia projektowe:
##### klasy:

klasa ValuableThings i klasy z niej dziedziczące przyjmują wartośc w konstruktorze typu float, ale konwertują ją na wartość typu int z zadana precyzją. Dzięki temu możliwe są operacje na dokładnych wartościach bez błędów maszynowch bez potrzeby używania biblioteki Decimal.

##### elementy szczególne:

generator:

Użycie tu genratora nie jest przerostem formy nad treścią, bo dzięki niemu możemy się upewnić, że nie zostaną wygenerowane produkty z poza zakresu i nie musimy używać range(30,51) (które można by łatwo pomylić z range(30,50) i co zdażyło mi się w czasie procesu tworzenia aplikacji). Poprawia też czytelność kodu
Generator ten jest używany w dwóch miejscach:
- w metodzie klasowej filled
- w inicjalizaji testów


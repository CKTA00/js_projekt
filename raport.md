## Raport z wykonania projektu
#### Wstęp

Uznałem, że w przypadku braku produktu, accpet_transaction rzuci wyjątek zamiast zwracać czegoś innego od krotki produktu i reszty (np. string). Miałem pomysł aby accept_transaction zawsze zwracał string, który od razu byłby wyświetlany w meassageboxie, co zdjeło by część logiki z gui.py, ale z drugiej strony, gdyby pojawiła się potrzeba użycia modułu vending_machine w innym kontekscie, przydatne mogło by się okazać zwracanie produktu i reszty w postaci obiektów a nie string, które mogły by być np. dodane do obiektu klasy Portfel albo cos w tym stylu. Dlatego postanowiłem zastosować jeden stały typ zwracany i wyjątek z wiadomością w przypadku braku.

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


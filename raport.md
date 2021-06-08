# Raport z wykonania projektu
## Wstęp

Uznałem, że w przypadku braku produktu, accpet_transaction rzuci wyjątek zamiast zwracać czegoś innego od krotki produktu i reszty (np. string). Miałem pomysł aby accept_transaction zawsze zwracał string, który od razu byłby wyświetlany w meassageboxie, co zdjeło by część logiki z gui.py, ale z drugiej strony, gdyby pojawiła się potrzeba użycia modułu vending_machine w innym kontekscie, przydatne mogło by się okazać zwracanie produktu i reszty w postaci obiektów a nie string, które mogły by być np. dodane do obiektu klasy Portfel albo cos w tym stylu. Dlatego postanowiłem zastosować jeden stały typ zwracany i wyjątek z wiadomością w przypadku braku.

## Opis klas
### moduł vending_utils:
1. Klasa ValuableThing

    Klasa ValuableThings i klasy z niej dziedziczące przyjmują wartośc w konstruktorze typu float, ale konwertują ją na wartość typu int z zadana precyzją. Dzięki temu możliwe są operacje na dokładnych wartościach bez błędów maszynowch bez potrzeby używania biblioteki Decimal.

    Jak każde przedmioty, można wziąść pewną ich ilość lub wszystkie za co odpoiwadając funkcje wirtualne take i take_all.

    (Są one wirtualne ponieważ klasy pochodne mogą wykazywać różne zachowanie jeśli podana ilośc do zabrania będzie większa od ilości.

    W przypadku monet, po prostu weźmie wszystkie monety jakie może. W przypadku produktów zwróci wyjątek o braku wymaganej ilości)

2. Klasa Coins
    
    Dziedziczy po klasie ValuableThings. Rozszerza ją o walute (nie jest ona używana, ale projekt można rozszerzyć np. o przyjmowanie różnych walut)

## Zaimplementowane testy
Wszystkie wymagane testy i jeden dodatkowy zostały zaimplementowane w jednej klasie testowej w pliku /test/test_vending_machine.py korzystającej z modułu wbudowanego unittest. Mogą wystąpić problemy z zaimportowaniem pakietu 'machine' z folderu src, ze względu na różne sposoby na importowanie ich za pomocą ścieżki relatywnej w różnych systemach operacyjnych. Nie miałem okazji przetestować projektu na innym systemie niż Windows 10, dlatego nie mam pewności czy import w tescie zadziała np. na MacOS lub Linux, dlatego kopia testów znajduje się w pliku src/reserve_test.py, która może bezpośrednio zaimportować odpowiednie moduły.

Dodatkowy test sprawdza odpowiedź automatu w przypadku gdy zabraknie monet do wydawania reszty.


## Elementy wyróżniające:

- **dodatkowy test** (opisany wyżej)

    [link]

- **generator** 

    [link]

    Użycie tu genratora nie jest przerostem formy nad treścią, bo dzięki niemu możemy się upewnić, że nie zostaną wygenerowane produkty z poza zakresu i nie musimy używać range(30,51) (które można by łatwo pomylić z range(30,50) i co zdażyło mi się w czasie procesu tworzenia aplikacji). Poprawia też czytelność kodu.

    Generator ten jest używany w dwóch miejscach:
    - w metodzie klasowej filled
    - w inicjalizaji testów

- **użycie wbudowanych dekoratorów**

    [link]

    Oznaczenie metod jako metody klasowe pozwoliło na wygodne tworzenie obiektów np. pustych lub wypełnionych produktami o losowych cenach bez stosowania list comprehension w każdym wywołaniu konstruktora danej klasy.

## Spełnione wymagania projektowe

1. Wyrażenia lambda:
    - [link]
    - [link]
    - [link]

2. List comprehensions:
    - [link]
    - [link]
    - [link]
    - [link]
    - [link]
    - [link]

3. Klasy (dokładniej opisne wyżej w dziale **Opis klas**):
    - 6 klas nie będących wyjątkami w module vending_utils (4 dziedziczą z pozostałych):
        - ValuableThings
        - Coins (dziedziczy z ValuableThings)
        - Products (dziedziczy z ValuableThings)
        - Container
        - Cash (dziedziczy z Container)
        - Assortment (dziedziczy z Container)
    - klasa VendingMachine korzystająca z modułu vending_utils w swoim własnym module
    - powyższa całość w postaci pakietu jest wykorzystywana przez klasę VendingMachineGUI odpowiedzialną za interfejs użytkownika
    - ten sam pakiet używany jest do testowania

    - metody wirtualne:
        - [link]
        - [link]

4. Wyjątki:
    - wyjątki niskiej warstwy (modułu venidng_utils)
        - NotEnoughMoney rzucany przez obiekt Cash w przypadku gdy podana wartość do wybrania przekracza jej zasoby
        
            [Link]

        - NotEnoughProduct rzucany przez obiekt Assortment gdy brakło dangeo produktu
                
            [Link]
            
    - wyjątki wyższej warstwy (modułu vending_machine) przechwytujące te niższej warstwy i generujące własne wyjątki z informacją dla użytkownika, które są przechwytywane i obsługiwane przez GUI lub testy:
        - IdOutOfRangeError rzucany gdy użytkownik wprowadzi nieprawidłowy numer

            [Link]

        - CannotGiveRest rzucany gdy automat nie może wydać reszty      

            [Link]
            
        - LackOfProduct rzucany gdy automat wykrył brak wybranego produktu
                
            [Link]
            
        - NotEnoughPayment rzucany gdy użytkownik próbuje zaakceptować transakcje za którą za mało zapłacił
                
            [Link]

    - poza tym liczne rzucane i nie przechwytywane wyjątki typu ValueError w przypadku podania nieprawidłowego typu danych do funkcji. Mają one informować developera o nieprawidłowym użyciu funkcji.
            
5. Moduły:
    Podział na moduł gui odpowiedzialnego za interfejs użytkownika oraz pakiet machine składający się z dwóch modółów. W sumie 3 oddzielne pliki .py nie licząc testów.




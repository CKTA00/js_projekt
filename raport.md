# Raport z wykonania projektu
## Wstęp

### Drobne zmiany od początkowych założeń projektu:

Uznałem, że w przypadku braku produktu, accpet_transaction rzuci wyjątek zamiast zwracać czoś innego od krotki produktu i reszty (np. string). Miałem pomysł aby accept_transaction zawsze zwracał string, który od razu byłby wyświetlany w meassageboxie, co zdjęło by część logiki z gui.py, ale z drugiej strony, gdyby pojawiła się potrzeba użycia modułu vending_machine w innym kontekscie, przydatne mogło by się okazać zwracanie produktu i reszty w postaci obiektów a nie string. Mogły by być np. dodane do obiektu portfela użytkownika albo coś w tym stylu. Dlatego postanowiłem zastosować jeden stały typ zwracany i wyjątek z wiadomością w przypadku braku.

Cały kod nigdy nie wspomina o napojach gdyż przez przypadek uogólniłem automat do produktów (raczej kwestia nazewnictwa)

Odeszłem od przyjetego nazewnictwa argumentu przechowującego obiekt z 'self' na rzecz krótszego 's'

### Inne trudności napotkane w czasie pracy nad projektem

Początowy kod był pisany przeze mnie po polsku, ale został przetłumaczony ze względu na troche pokraczne nazewnictwo getterów i setterów oraz mieszanie angielskiego syntaxu z nazwami zmiennych. Pozostawiłem jedynie stringi dokumentacyjne, komentarze i treści wyjątków oraz rezultaty funkcji takich jak __str__ po polsku.

Szczególną trudność sprawiły mi próby znalezienia niezależnego od platformy sposobu na zaimportowanie własnych modułów do testów, gdy znajdują się one w różnych folderach. Więcej o tym w dziele **Zaimplementowane testy**

Projekt na początku obsługiwał wartości pieniężne tylko za pomocą typu float, co później okazało się być przeszkodą ze względu na błędy maszynowe. Metody klas z modułu vending_utils operują na typach int i posiadają dodatkową zmienna precision określającą rząd najmniejszej jednostki pieniężnej. Z zewnątrz modułu można nadal używać jakby był zrobiony na floatach. Ze względu na to, w testach sprawdzanie niektórych wartości odbywa się z pomocą assertAlmostEqual zamiast assertEqual. GUI korzysta z jeszcze innych metod, które od razu formatują wartości do str tak aby nie dochodziło do wyświetlania wartości typu 2.000000000001

### Opis klas

1. Klasa ValuableThing, Coins i Products

    Przechowują one informacje o przedmiocie i ilości identycznych sztuk.
    Klasa ValuableThings i klasy z niej dziedziczące przyjmują wartość w konstruktorze typu float, ale konwertują ją na wartość typu int z zadana precyzją. Dzięki temu możliwe są operacje na dokładnych wartościach bez błędów maszynowych bez potrzeby używania biblioteki Decimal.

    Zawiera metodę wirtualną take() ponieważ klasy pochodne wykazują różne zachowanie jeśli podana ilość do zabrania będzie zbyt duża.
    W przypadku monet, po prostu weźmie wszystkie monety jakie są. W przypadku produktów zwróci wyjątek o braku.

    Klasa Coins dziedziczy po klasie ValuableThings. Rozszerza ją o walutę (nie jest ona używana, ale projekt można rozszerzyć np. o przyjmowanie różnych walut) oraz o dodatkowe funkcje np. add() oraz implementuje metodę wirtualna take.
    
    Klasa Products dziedziczy po klasie ValuableThings. Rozszerza ją o nazwę produktu oraz implementuje metodę wirtualna take.

2. Klasa Container, Cash i Assortment:

    Obiekty tej klasy są zdolne do przechowywania kilku rodzajów przedmiotów, czyli kilku instancji odpowiednio ValuableThings, Coins i Products. Informacja o ich ilości już znajduje się w tych obiektach

    Klasa Cash dziedziczy po Container i jest używana jako bank (pieniądze automatu), wrzucone pieniądze, a także obiekt ten jest zwracany jako reszta. Dodaje metody dodawania pieniędzy do obiektu, dodawania obiektów między sobą (operator + [Link])

    Klasa Asortment jest używana jako asortyment automatu. Na razie nie implementuje żadnego dodawania produktów, więc w przypadku wywołania dodawania operatorem lub funkcji add zostanie zwrócony wyjątek. Planowałem dodać uzupełnianie automatu w razie braku produktu, np. po podaniu hasła jako właściciel automatu, ale ostatecznie zrezygnowałem z tego, gdyż konsekwentnie wiązało by się to z dodaniem całkiem nowego systemu właściciela np. wyciągania zebranych przez automat pieniędzy i uzupełniania drobnych wraz zupełnie innym gui, co jest praktycznie drugim podobnej wielkości projektem.

3. Klasa VendingMachine i VendingMachineGUI:

    Klasa VendingMachine (vm) jest częścią pakietu machine i zawiera wszystkie funkcje potrzebne do działania automatu gdybyśmy chcieli go obsługiwać np. za pomocą skryptu (w tym testów jednostkowych). W celu obsłużenia GUI, które dodaje logikę programu (taką jak wprowadzanie cyfr, wyświetlanie odpowiednich danych w postaci wizualnej) nie kluczowej dla działania automatu samego w sobie.

## Zaimplementowane testy

Wszystkie wymagane testy i jeden dodatkowy zostały zaimplementowane w jednej klasie testowej w pliku /test/test_vending_machine.py korzystającej z modułu wbudowanego unittest. **Mogą wystąpić problemy z zaimportowaniem pakietu 'machine' z folderu src**, ze względu na różne sposoby na importowanie ich za pomocą ścieżki relatywnej w różnych systemach operacyjnych. Nie miałem okazji przetestować projektu na innym systemie niż Windows 10, dlatego nie mam pewności czy import w tescie zadziała np. na MacOS lub Linux, dlatego kopia testów znajduje się w pliku **src/reserve_test.py**, który może bezpośrednio zaimportować odpowiednie moduły. Wole jednak zachować uporządkowana strukturę nawet tego niewielkiego projektu, dlatego wszystkie testy powinny się znajdować w folderze test.

Dodatkowy test nr. 9 sprawdza odpowiedź automatu w przypadku gdy zabraknie monet do wydawania reszty.

## Elementy wyróżniające:

- **dodatkowy test** (opisany wyżej)

    [link]

- **generator** 

    [link]

    Użycie tu generatora nie jest tu przerostem formy nad treścią, bo dzięki niemu możemy się upewnić, że nie zostaną wygenerowane produkty z poza zakresu i nie musimy używać range(30,51) w wielu miejscach jednocześnie (które można by łatwo pomylić z range(30,50) i co zdażyło mi się w czasie procesu tworzenia aplikacji). Poprawia też czytelność kodu.

    Generator ten jest używany w dwóch miejscach:
    - w metodzie klasowej filled
    - w inicjalizacji testów

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

3. Klasy (dokładniej opisane wyżej w dziale **Opis klas**):
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
        - [link]

4. Wyjątki:
    - wyjątki niskiej warstwy (modułu venidng_utils)
        - NotEnoughMoney rzucany przez obiekt Cash w przypadku gdy podana wartość do wybrania przekracza jej zasoby
        
            [Link]

        - NotEnoughProduct rzucany przez obiekt Assortment gdy brakło danego produktu
                
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

    - poza tym liczne rzucane i nie przechwytywane wyjątki typu ValueError i TypeError w przypadku podania nieprawidłowych danych do funkcji. Mają one informować developera o nieprawidłowym użyciu funkcji.
            
5. Moduły:
    Podział na moduł gui odpowiedzialnego za interfejs użytkownika oraz pakiet machine składający się z dwóch modułów. W sumie 3 oddzielne pliki .py nie licząc testów i __init__.py.

## Autor:
#### Przemysław Kożuch

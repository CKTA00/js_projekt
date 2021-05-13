#import imp; imp.reload(modulename)
import copy

if __name__ == '__main__':
    print("Moduł wewnętrzny automatu z napojami")
    print(dir())
    #print(__doc__)
else:
    pass
    #moduł został zaimportowany, nie wypisuj nic

""" za pomocą #? oznaczyłem cechy nad którch ostateczną implementacją się jeszcze zastanawiam
    lub zamierzam usunąć jeśli nie zaistnieje potrzeba ich użycia
"""

nominały = (0.01,0.02,0.05,0.1,0.2,0.5,1,2,5)
"""predefiniowane wartości nominalne monet w PLN"""

class Przedmioty:
    """Klasa reprezentująca pewną ilość przedmiotów o identycznych cechach, w tym koniecznie wartości za sztuke w PLN.
        Jak każde przedmioty, można wziąść pewną ich ilość lub wszystkie
        za co odpoiwadając funkcje wirtualne weź i weź_wszystkie.
        W pewnym sensie jest to pojemnik, ale na identyczne przedmioty, w odróżnieniu do klasy Pojemnik"""
    def __init__(s,wartość,ilość=1):
        s._wartość_ = wartość
        s._ilość_ = 1
    def weź(s,ile):
        pass
    def weź_wszystkie(s):
        pass
    def łączna_wartosc(s):
        return s._ilość_ * s._wartość_

class Produkty(Przedmioty):
    """Przechowuje informacje o produkcie takie jak jego nazwa i cena za sztuke,
    ale również ilość sztuk tego produktu np. w asortymencie.
    Zatem tak na prawdę reprezentuję pewna ilość identycznych produktów, a nie sam rodzaj produktu.
    """
    def __init__(s,nazwa,cena,początkowa_ilość=0):
        s.nazwa=nazwa
        super.__init__(s,cena,początkowa_ilość)

    def zmień_ilość(s,ile):
        """Zmienia ilość produktu (dodaje argument 'ile' do ilości) jeśli to możliwe.
        Argument 'ile' może być ujemny.
        """
        s._ilość_ += ile
        if(s._ilość_<0):
            print("Brak Sztuk")
            #exception? komunikat o braku

    def weź(s,ile):
        """Zwraca prodkut w ilości 'ile' i odejmuje od ilości w tym produkcie (jeśli możliwe) 
        """
        s.zmień_ilość(-ile) # try catch
        sztuka = Produkty(s.nazwa,s._cena_,ile)
        # Alternatywny sposób (wybiore w przyszłości na podstawie jakiś testów czasowych może):
        #sztuka = copy.deepcopy(s)
        #sztuka._ilość_ = 1
        #jeśli błąd, przekaż go dalej (komunikat o braku)
        return sztuka

class Monety(Przedmioty):
    """Prosta klasa definująca ilość monet o podanym nominale
    Dziedziczy po Przedmioty, ale umożliwia dodanie monet do istniejącego już zbioru"""
    def __init__(s,nominał,ile):
        #s.__waluta__ = waluta #?
        super.__init__(s,nominał,ile)

    def zmień_ilość(s,ile):
        """Zmienia ilość monet (dodaje argument 'ile' do ilości) jeśli to możliwe.
        Argument 'ile' może być ujemny.
        """
        s._ilość_ += ile
        if(s._ilość_<0):
            print("Brak takiej monety")
            #exception? komunikat o braku

    def weź(s,ile):
        s.zmień_ilość(-ile) # try catch
        # jeśli nie ma błędu
        return Monety(s._wartość_,ile)

    def dodaj(s,ile):
        s.zmień_ilość(ile)

    #zaimplementować jakieś funkcje pomagające w liczeniu reszty?

class Pojemnik:
    """Klasa zawieracjąca definująca słownik zawierający identyfikatory rodzaju (key)
     oraz przedmioty (obiekty klasy Przedmiot) tego rodzaju (item).
     Dzięki temu może zawierać przedmioty posegregowane według ich rodzaju.
    """
    def __init__(s,rodzaje,przedmioty):
        s.poj = {rodzaje[i]:przedmioty[i] for i in range(len(przedmioty))}
    def weź(s,rodzaj,ile):
        """Bierze daną ilość przedmiotów określonego rodzaju i zwraca w postaci obiektu Przedmioty
        """
        return s.poj[rodzaj].weź(ile)
    def dodaj(s,rodzaj,ile):
        pass

    def weź_wszystko(s): #?
        """Wyjmuje wszystko z pojemnika i zwraca w postaci słownika
        """
        r = copy(s.poj)
        s.poj = {}
        return r

class Kasa(Pojemnik):
    """Klasa przechowywująca pieniądze w postaci posegregowanych według nominałów monet.
    """
    def __init__(s, monety=[100 for n in nominały]):
        """monety = lista ilości monet kolejnych nominałów, domyślnine po 100 monet każdego nominału"""
        super().__init__(nominały, monety)

    def dodaj(s,nominał,ile):
        """Dodaje daną ilość przedmiotów do odpowiej "przegródki"
        """
        if(isinstance(nominał,str)):
            nominał = float(nominał)
        s.poj[nominał].dodaj(ile)

    # zaimplementować funkcje wyliczająca reszte

class Asortyment(Pojemnik):
    """Klasa przechowywująca wszystkie produkty, posegregowane według ich numeru, wraz z ich ilościami 
    """
    def __init__(s,lista_produktów,numeruj_od):
        lista_nr=[i+numeruj_od for i in range(len(lista_produktów))]
        super().__init__(s,lista_nr,lista_produktów)

    def dodaj(*args):
        print("Nie można dodawać produktów do asortymentu (chyba że jesteś właścicelem") #?
        # Okazja do rozszerzenia projektu o uzupełnianie automatu gdy braknie towaru

class Automat:
    """Klasa obsługująca wydawanie produktów i reszty po przyjęciu monet
     od uzytkownika i zwracająca odpowiedni wyjątek w razie niepowodzenia (np. braku produktu)
     
    """
    #? Funkcje weź i dodaj zostają nadpisane metodami wrzucania monet i odbierania reszty (i/lub produktu)
    #? lub zdefiniowanie innych funkcji i zrezygnowanie z dziedziczenia w tym wypadku

    def _init_(s,lista_produktów,kasa=Kasa()):
        s._asortyment_ = Asortyment(lista_produktów,30)
        s._kasa_ = kasa
    
    def weź(s,nr_poduktu,ile=1):
        return s.poj[nr_poduktu].weź(ile) # nadpisać metodą sprawdzającą wrzucone monety i wybrany numer

    def dodaj(*args):
        pass
    


        


    

            


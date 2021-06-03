from typing import List
import math
#import copy


class ValuableThings:
    """Klasa reprezentująca pewną ilość przedmiotów o identycznych cechach, w tym koniecznie wartości za sztuke w PLN.
        Jak każde przedmioty, można wziąść pewną ich ilość lub wszystkie za co odpoiwadając funkcje wirtualne take i take_all.
        (Są one wirtualne ponieważ klasy pochodne mogą wykazywać różne zachowanie jeśli podana ilośc do zabrania będzie zbyt duża.
        W przypadku monet, po prostu weź wszystkie. W przypadku produktów zwróć wyjątek)
    """
    def __init__(s,wartość,ilość=1):
        s._value_ = wartość
        s._quantity_ = 1
    def take(s,q):
        raise(NotImplementedError("Funkcja take() nie została zaimplementowana!"))
    def take_all(s):
        raise(NotImplementedError("Funkcja take_all() nie została zaimplementowana!"))
    def cumulated_value(s):
        return s._quantity_ * s._value_
    def get_value(s):
        return s._value_
    def get_quantity(s):
        return s._quantity_

class NotEnoughProductError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Products(ValuableThings):
    """Przechowuje informacje o produkcie takie jak jego name i cena za sztuke,
    ale również ilość sztuk tego produktu np. w asortymencie.
    Zatem tak na prawdę reprezentuję pewna ilość identycznych produktów, a nie sam rodzaj produktu.
    """
    def __init__(s,name,price,initial_quantity=0):
        s.name=name
        super.__init__(s,price,initial_quantity)

    # def change_quantity(s,q):
    #     """Zmienia ilość produktu (dodaje argument 'q' do ilości) jeśli to możliwe.
    #     Argument 'q' może być ujemny.
    #     """
    #     s._quantity_ += q
    #     if(s._quantity_<0):
    #         print("Brak Sztuk")
    #         #exception? komunikat o braku

    def take(s,q):
        """Zwraca prodkut w ilości 'q' i odejmuje od ilości w tym produkcie.
        Jeśli nie ma na tyle, rzuca wyjątkiem NotEnoughProductError
        """
        if(q>s.get_quantity()):
            raise  NotEnoughProductError()
        s._quantity_-=q
        return Products(s.name,s._value_,q)

class Coins(ValuableThings):
    """Prosta klasa definująca ilość monet o podanym nominale"""
    def __init__(s,den,ile):
        #s.__waluta__ = waluta #?
        super.__init__(s,den,ile)

    # def change_quantity(s,ile):
    #     """Zmienia ilość monet (dodaje argument 'ile' do ilości) jeśli to możliwe.
    #     Argument 'ile' może być ujemny.
    #     """
    #     s._quantity_ += ile
    #     if(s._quantity_<0):
    #         print("Brak takiej monety")
    #         #exception? komunikat o braku

    def take(s,q):
        """Zwraca monety w ilości 'q' i odejmuje od ilości monet w tym obiekcie.
        Jeśli nie ma na tyle, bierze wszystkie możliwe monety.
        """
        if(q>s.get_quantity()):
            q = s.get_quantity()
        s._quantity_-=q
        return Coins(s._value_,q)

    def get_quantity(s):
        return s._quantity_

    def add(s,q):
        if(q<0):
             raise ValueError("Nie można dodać ujemnej ilości monet. Jęsli chcesz je odjąć użyj funkcji take()")
        s._quantity_+=q



#denominations = (0.01,0.02,0.05,0.1,0.2,0.5,1,2,5)
denominations = (5,2,1,0.5,0.2,0.1,0.05,0.02,0.01)
"""predefiniowane wartości nominalne monet w PLN"""

class Container:
    """Klasa zawieracjąca definująca słownik zawierający identyfikatory rodzaju (key)
     oraz ValuableThings (obiekty klasy Przedmiot) tego rodzaju (item).
     Dzięki temu może zawierać ValuableThings posegregowane według ich rodzaju.
    """
    def __init__(s,kinds,things):
        if(not isinstance(things,List)):
            raise ValueError("things musi być listą")
        if(not isinstance(kinds,List)):
            raise ValueError("kinds musi być listą")
        if(not all(isinstance(p,ValuableThings) for p in things)):
            raise ValueError("wszystkie elementy 'things' muszą być klasy ValuableItem")
        if(len(kinds) != len(things)):
            raise ValueError("listy things i kinds muszą mieć taką samą długość")
        s._content_ = {kinds[i]:things[i] for i in range(len(things))}

    def _get_thing_(s,kind):
        return s._content_.get(kind)

    def take(s,kind,q):
        """Bierze daną ilość przedmiotów określonego rodzaju i zwraca w postaci obiektu ValuableThings
        """
        return s._content_[kind].get(q)

    def add(s,kind,q): #?
        raise(NotImplementedError("funkcja dodaj nie została zaimplementowana"))

    def get_price(s,id):
        s._content_[id].get_value()

    def take_all(s):
        raise(NotImplementedError("funkcja take_all nie została zaimplementowana"))

class NotEnoughMoneyError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Cash(Container):
    """Klasa przechowywująca pieniądze w postaci posegregowanych według denów monet. Obsługuje tylko zdefiniowane denominations.
    """
    def __init__(s, coins):
        """monety = lista ilości monet kolejnych nominałów, domyślnine po 100 monet każdego nominałuu"""
        if(not isinstance(coins,list)):
            raise ValueError("Argument coins musi być listą.")
        if(not all(isinstance(c,Coins) for c in coins)):
            raise ValueError("Lista coins może składać się wyłącznie z obiektów Coins.")
        super().__init__(denominations, coins)

    @classmethod
    def empty(cls):
        """Tworzy obiekt Cash ze zdefiniowanymi denami, ale bez monet"""
        return cls([Coins(n,0) for n in denominations])

    @classmethod
    def equally_filled(cls,q):
        """Tworzy obiekt Cash z po_ile ilością monet"""
        return cls([Coins(n,q) for n in denominations])

    # def add(s,den,ile):
    #     """Dodaje daną ilość monet do odpowiej "przegródki"
    #     """
    #     if(isinstance(den,str)):
    #         den = float(den)
    #     s._content_[den].dodaj(ile)

    def __add__(s, o):
        for den in denominations:
            s._content_[den].add(o._content_[den].get_quantity())

    def total_value(s):
        """Zwraca sume wartości wszystkich monet"""
        suma = 0.0
        for m in super()._content_:
            suma += m.cumulated_value()
        return suma

    def take_all(s):
       return Cash(s._content_)

    def take_value(s,value):
        """Zwraca obiekt Cash zawierający odliczoną sume tak aby składała się ona z jak najmniejszej liczby monet
        """
        #assert suma>0
        if(value > s.cumulated_value()):
            raise NotEnoughMoneyError()
        rest = Cash.empty()
        den_index = 0                           #potencjał na zdefiniowanie obiektu z nominałami i funkcją iterującą?
        while (value>0):
            den = denominations[den_index]
            required_quantity_of_coins = math.floor(value/den)
            max_coins = s._content_[den].take(required_quantity_of_coins)
            rest = rest + max_coins
            den_index += 1
            #rest.add(den,max_coins.)


class Assortment(Container):
    """Klasa przechowywująca wszystkie produkty, posegregowane według ich numeru, wraz z ich ilościami 
    """
    def __init__(s,lista_produktów,numeruj_od):
        lista_nr=[i+numeruj_od for i in range(len(lista_produktów))]
        super().__init__(s,lista_nr,lista_produktów)

    def dodaj(*args):
        print("Nie można dodawać produktów do Assortmentu (chyba że jesteś właścicelem") #?
        # Okazja do rozszerzenia projektu o uzupełnianie automatu gdy braknie towaru


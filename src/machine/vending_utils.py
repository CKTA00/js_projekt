from typing import List, Tuple
import math
#import copy


class ValuableThings:
    """Klasa reprezentująca pewną ilość przedmiotów o identycznych cechach, w tym koniecznie wartości za sztuke w PLN.
        Jak każde przedmioty, można wziąść pewną ich ilość lub wszystkie za co odpoiwadając funkcje wirtualne take i take_all.
        (Są one wirtualne ponieważ klasy pochodne mogą wykazywać różne zachowanie jeśli podana ilośc do zabrania będzie zbyt duża.
        W przypadku monet, po prostu weź wszystkie. W przypadku produktów zwróć wyjątek)
    """
    def __init__(s,value: float, quantity: int=1,*,precision: int=2):
        s._quantity_ = quantity
        s._precision_ = precision
        s._value_ = int(round(value*10**precision))
    def take(s,q):
        raise(NotImplementedError("Funkcja take() nie została zaimplementowana!"))
    def take_all(s):
        raise(NotImplementedError("Funkcja take_all() nie została zaimplementowana!"))
    def cumulated_value(s)->float:
        return s._quantity_ * s._value_ / 10**s._precision_
    def cumulated_raw_value(s)->int:
        return s._quantity_ * s._value_
    def get_value(s)->float:
        return s._value_/10**s._precision_
    def get_raw_value(s)->int:
        return s._value_
    def get_quantity(s)->int:
        return s._quantity_
    def __repr__(s):
        return "{value="+str(s.get_value())+", quantity="+str(s.get_quantity())+"}"

class NotEnoughProductError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Products(ValuableThings):
    """Przechowuje informacje o produkcie takie jak jego name i cena za sztuke,
    ale również ilość sztuk tego produktu np. w asortymencie.
    Zatem tak na prawdę reprezentuję pewna ilość identycznych produktów, a nie sam rodzaj produktu.
    """
    def __init__(s,name,price,initial_quantity=0,*,precision=2):
        s.name=name
        super().__init__(price,initial_quantity,precision=precision)

    def __str__(s):
        return "Produkt o nazwie \""+s.name +"\" w ilości "+str(s._quantity_)


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
            raise NotEnoughProductError('Nie wystarczająca ilość produktu')
        s._quantity_-=q
        return Products(s.name,s._value_,q)

class Coins(ValuableThings):
    """Prosta klasa definująca ilość monet o podanym nominale, wartości są przechowywane w int"""
    def __init__(s,den: float, q: int,*,precision: int=2,waluta: str="PLN"):
        super().__init__(den,q,precision=precision)
        s._waluta_ = waluta

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
        s._quantity_-= q
        return Coins(s.get_value(),q)

    #def get_quantity(s):
        #return s._quantity_

    def add(s,q):
        if(q<0):
             raise ValueError("Nie można dodać ujemnej ilości monet. Jęsli chcesz je odjąć użyj funkcji take()")
        s._quantity_+=q

    def __str__(s):
        return "Moneta o nominale "+str(s.get_value()) +" "+str(s._waluta_)+" w ilości "+str(s._quantity_)



#denominations = (0.01,0.02,0.05,0.1,0.2,0.5,1,2,5)
denominations = (5,2,1,0.5,0.2,0.1,0.05,0.02,0.01)
"""predefiniowane wartości nominalne monet w PLN"""

class Container:
    """Klasa zawieracjąca definująca słownik zawierający identyfikatory rodzaju (key)
     oraz ValuableThings (obiekty klasy Przedmiot) tego rodzaju (item).
     Dzięki temu może zawierać ValuableThings posegregowane według ich rodzaju.
    """
    def __init__(s,kinds,things):
        if(not isinstance(things,(list,tuple))):
            raise ValueError("things musi być listą lub krotką")
        if(not isinstance(kinds,(list,tuple))):
            raise ValueError("kinds musi być listą lub krotką")
        if(not all(isinstance(p,ValuableThings) for p in things)):
            print(things)
            raise ValueError("wszystkie elementy 'things' muszą być klasy ValuableItem")
        if(len(kinds) != len(things)):
            raise ValueError("listy things i kinds muszą mieć taką samą długość")
        s._content_ = {kinds[i]:things[i] for i in range(len(things))}

    def _get_thing_(s,kind):
        return s._content_.get(kind)

    def take(s,kind,q):
        """Bierze daną ilość przedmiotów określonego rodzaju i zwraca w postaci obiektu ValuableThings
        """
        return s._content_[kind].take(q)

    def add(s,kind,q): #?
        raise(NotImplementedError("funkcja dodaj nie została zaimplementowana"))


    def take_all(s):
        raise(NotImplementedError("funkcja take_all nie została zaimplementowana"))

class NotEnoughMoney(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Cash(Container):
    """Klasa przechowywująca pieniądze w postaci posegregowanych według denów monet. Obsługuje tylko zdefiniowane denominations.
    """
    def __init__(s, coins,den=denominations):
        """monety = lista monet kolejnych nominałów, domyślnine po 100 monet każdego nominałuu"""
        if(not isinstance(coins,list)):
            raise ValueError("Argument coins musi być listą.")
        if(not all(isinstance(c,Coins) for c in coins)):
            raise ValueError("Lista coins może składać się wyłącznie z obiektów Coins.")
        super().__init__(den, coins)

    @classmethod
    def empty(cls):
        """Tworzy obiekt Cash ze zdefiniowanymi denami, ale bez monet"""
        return cls([Coins(n,0) for n in denominations])

    @classmethod
    def equally_filled(cls,q: int):
        """Tworzy obiekt Cash z ilością q monet dla każdego nominału"""
        return cls([Coins(n,q) for n in denominations])

    # def add(s,den,ile):
    #     """Dodaje daną ilość monet do odpowiej "przegródki"
    #     """
    #     if(isinstance(den,str)):
    #         den = float(den)
    #     s._content_[den].dodaj(ile)

    def __add__(s, o):
        if(not isinstance(o, Cash)):
            raise ValueError("Do obiektu Cash poeratorem można dodać tylko inny obiekt Cash. Typ innego obiektu: "+str(type(o)))
        r = Cash.empty()
        q_denom = len(s._content_.keys()) #ilośc nominałów w s
        if(q_denom != len(o._content_.keys())):
            raise ValueError("Nie można dodać obiektów Cash o różnej ilości nominałów")
        #if(all(s._content_.keys()[i] == o._content_.keys()[i] for i in range(q_denom))):
        if(list(s._content_.keys())!=list(o._content_.keys())):
            raise ValueError("Nie można dodać obiektów Cash o różnych zestawach nominałów")
        for den in denominations:
            r._content_[den].add(o._content_[den].get_quantity()+s._content_[den].get_quantity())
        return r

    def add_coins(s,coins: Coins):
        den = coins.get_value()
        q = coins.get_quantity()
        s._content_[den].add(q)

    def total_value(s):
        """Zwraca sume wartości wszystkich monet"""
        suma = 0.0
        for m in s._content_.values():
            suma += m.cumulated_value()
        return suma

    def take_all(s):
        return Cash(list(s._content_.values()))

    def take_value(s,value):
        """Zwraca obiekt Cash zawierający odliczoną sume tak aby składała się ona z jak najmniejszej liczby monet
        """
        #assert suma>0
        if(value > s.total_value()):
            raise NotEnoughMoney()
        value_gr = int(round(value*100)) #w groszach typu int
        rest = Cash.empty()
        den_index = 0 
        while (value_gr>0):
            if(den_index>=len(denominations)):
                print("Ten błąd nie powinien miec miejsca!")
                raise NotEnoughMoney()
            den = denominations[den_index]
            required_quantity_of_coins = math.floor(value_gr/100/den)
            max_coins = s._content_[den].take(required_quantity_of_coins) #maksymalna liczba monet jednego nominału jaką można wydać
            value_gr-=max_coins.cumulated_raw_value()
            rest.add_coins(max_coins)
            den_index += 1
        return rest

    def __str__(s):
        string = ""
        for n in s._content_.values():
            if(n.get_quantity()>0):
                string += str(n)+"\n"
        return string
            

class Assortment(Container):
    """Klasa przechowywująca wszystkie produkty, posegregowane według ich numeru, wraz z ich ilościami 
    """
    def __init__(s,product_list,number_from):
        """product_list - lista produktów, number_from - od jakiej liczby ma ponumerować"""
        list_nr=[i+number_from for i in range(len(product_list))]
        super().__init__(list_nr,product_list)

    def check_quantity(s, id: int) -> bool:
        return (s._content_[id].get_quantity()<=0)

    def get_price(s,id: int) -> float:
        return s._content_[id].get_value()


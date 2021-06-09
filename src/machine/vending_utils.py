#from typing import List, Tuple
import math

# Wyjątki:

class NotEnoughProduct(Exception):
    """Wyjątek oznaczający brak produktu w obiekcie Products"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotEnoughMoney(Exception):
    """Wyjątek oznaczajacy brak możliwości wyciągnięcia pewnej ilości monet."""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# Klasy właściwe:

class ValuableThings:
    """Klasa reprezentująca pewną ilość przedmiotów o identycznych cechach, w tym koniecznie wartości za sztuke.
        Wartość przechowywana jest za pomocą int w jednostce określonej przez precyzje, tak aby uniknąć błędów maszynowych,
        lecz może być inicjalizowana i zwracana w postaci float.
    """
    def __init__(s,value: float, quantity: int=1,*,precision: int=2):
        if(not isinstance(quantity, int)):
            raise TypeError("'quantity' musi być typu int.")
        if(quantity<0):
            raise ValueError("'quantity' musi być dodatnie.")
        s._quantity = quantity

        if(not isinstance(precision, int)):
            raise TypeError("'precision' musi być typu int.")
        s._precision_ = precision

        if(not isinstance(value, (int,float))):
            raise TypeError("'value' musi być typu float (lub int).")
        s._value = int(round(value*10**precision))

    def __repr__(s):
        return "{value="+str(s.get_value())+", quantity="+str(s.get_quantity())+"}"

    def take(s,q: int):
        """Metoda wirtualna. Powinna implemetować wyciąganie q ilości przedmiotów."""
        raise(NotImplementedError("Metoda take() nie została zaimplementowana!"))
        
    def get_total_value(s)->float:
        """Zwraca całkowitą wartość przedmiotów w postaci float."""
        return s._quantity * s._value / 10**s._precision_

    def get_total_raw_value(s)->int:
        """Zwraca całkowitą dokładną wartość przemiotów w jednostce przechowywania."""
        return s._quantity * s._value

    def get_value(s)->float:
        """Zwraca wartość jednej sztuki w postaci float."""
        return s._value/10**s._precision_
 
    def get_raw_value(s)->int:
        """Zwraca dokładną wartość jednej sztuki w jednostce przechowywania."""
        return s._value
 
    def get_quantity(s)->int:
        """Zwraca ilość przedmiotów."""
        return s._quantity
 
    def get_formated_value(s)->str:
        """Zwraca wartość jednej sztuki w postaci string z uwzględnieniem precyzji."""
        return ("{:."+str(s._precision_)+"f}").format(s.get_value())
 
    def get_formated_total_value(s)->str:
        """Zwraca całkowitą wartość w postaci string z uwzględnieniem precyzji."""
        return ("{:."+str(s._precision_)+"f}").format(s.get_total_value())



class Products(ValuableThings):
    """Przechowuje informacje o produkcie takie jak jego nazwa (name) i cena za sztuke,
    ale również ilość sztuk tego produktu np. w asortymencie.
    """
    def __init__(s,name,price,initial_quantity=0,*,precision=2):
        s.name=name
        super().__init__(price,initial_quantity,precision=precision)

    def __str__(s):
        return "Produkt o nazwie \""+s.name +"\" w ilości "+str(s._quantity)

    def take(s,q):
        """Zwraca prodkut w ilości 'q' i odejmuje od ilości w tym produkcie.
        Jeśli nie ma na tyle, rzuca wyjątkiem NotEnoughProduct.
        """
        if(q>s.get_quantity()):
            raise NotEnoughProduct('Nie wystarczająca ilość produktu.')
        s._quantity-=q
        return Products(s.name,s._value,q)


class Coins(ValuableThings):
    """Prosta klasa definująca ilość monet o podanym nominale, wartości są przechowywane w int."""
    def __init__(s,den: float, q: int,*,precision: int=2,currency: str="PLN"):
        super().__init__(den,q,precision=precision)
        s._currency = currency

    def take(s,q):
        """Zwraca monety w ilości 'q' i odejmuje od ilości monet w tym obiekcie.
        Jeśli nie ma na tyle, bierze wszystkie możliwe monety.
        """
        if(q>s.get_quantity()):
            q = s.get_quantity()
        s._quantity-= q
        return Coins(s.get_value(),q)

    def add(s,q):
        """Dodaje q sztuk tej moenty do obiektu"""
        if(q<0):
             raise ValueError("Nie można dodać ujemnej ilości monet. Jęsli chcesz je odjąć użyj funkcji take().")
        s._quantity+=q

    def __str__(s):
        return "Monety o nominale "+str(s.get_value()) +" "+str(s._currency)+" w ilości "+str(s._quantity)


denominations = (5,2,1,0.5,0.2,0.1,0.05,0.02,0.01)
"""Predefiniowane wartości nominalne monet w PLN."""


class Container:
    """Klasa zawieracjąca definująca słownik zawierający identyfikatory rodzaju (key)
     oraz ValuableThings (obiekty klasy Przedmiot) tego rodzaju (item).
     Dzięki temu może zawierać ValuableThings posegregowane według ich rodzaju.
    """
    def __init__(s,kinds,things):
        if(not isinstance(things,(list,tuple))):
            raise ValueError("'things' musi być listą lub krotką.")

        if(not all(isinstance(t,ValuableThings) for t in things)):
            raise ValueError("Lista lub krotka 'things' może składać się wyłącznie z obiektów ValuableThings.")

        if(not isinstance(kinds,(list,tuple))):
            raise ValueError("'kinds' musi być listą lub krotką.")
        
        if(len(kinds) != len(things)):
            raise ValueError("Listy things i kinds muszą mieć taką samą ilość elementów.")
        
        s._content_ = {kinds[i]:things[i] for i in range(len(things))}

    def take(s,kind,q: int) -> ValuableThings:
        """Bierze daną ilość przedmiotów określonego rodzaju i zwraca w postaci obiektu ValuableThings.
        """
        return s._content_[kind].take(q)

    def __add__(s, o):
        """Operator + wirtualny. Powinien implementować dodanie dwóch obiektów dziedziczacych z Container tego samego typu.
        """
        raise(NotImplementedError("Operator add nie został zaimplementowany!"))

    def add(s,kind,q):
        """Metoda wirtualna. Powinna implementować dodanie ilości 'q' do przedmiotów typu 'kind'.
        """
        raise(NotImplementedError("Metoda add nie została zaimplementowana!"))


class Cash(Container):
    """Klasa przechowywująca pieniądze w postaci posegregowanych według nominałów monet. Obsługuje tylko nominały przesłane w 'den'.
    """
    def __init__(s, coins,den=denominations):
        super().__init__(den, coins)
        if(not all(isinstance(c,Coins) for c in coins)):
            raise ValueError("Lista lub krotka 'coins' może składać się wyłącznie z obiektów Coins.")

    @classmethod
    def empty(cls):
        """Tworzy obiekt Cash ze zdefiniowanymi denami, ale bez monet."""
        return cls([Coins(n,0) for n in denominations])

    @classmethod
    def equally_filled(cls,q: int):
        """Tworzy obiekt Cash z ilością 'q' monet dla każdego nominału."""
        return cls([Coins(n,q) for n in denominations])

    def add(s,den: float,q: int):
        """Dodaje daną ilość monet do odpowiej "przegródki".
        """
        if(isinstance(den,str)):
            den = float(den)
        s._content_[den].add(q)

    def __add__(s, o):
        """Dodaje dwa obiekty cash do siebie dodając poszczególne ilości monet."""
        if(not isinstance(o, Cash)):
            raise ValueError("Do obiektu Cash operatorem można dodać tylko inny obiekt Cash. Typ innego obiektu: "+str(type(o)))
        r = Cash.empty()
        if(list(s._content_.keys())!=list(o._content_.keys())):
            raise ValueError("Nie można dodać obiektów Cash o różnych zestawach nominałów.")
        for den in denominations:
            r._content_[den].add(o._content_[den].get_quantity()+s._content_[den].get_quantity())
        return r

    def __eq__(s,o):
        """Porównuje dwa obiekty Cash uwzględniając ilości nominałów."""
        if(list(s._content_.keys())!=list(o._content_.keys())):
            raise False
        for den in denominations:
            if(s._content_[den].get_quantity()!=o._content_[den].get_quantity()):
                return False
        return True

    def add_coins(s,coins: Coins):
        """Dodaje do obiektu Cash monety w postaci obiektu Coins."""
        if(not isinstance(coins, Coins)):
            raise TypeError("'coins' musi być typu Coins.")
        den = coins.get_value()
        q = coins.get_quantity()
        s._content_[den].add(q)

    def total_value(s):
        """Zwraca sume wartości wszystkich monet wszystkich nominałów."""
        suma = 0.0
        for m in s._content_.values():
            suma += m.get_total_value()
        return suma

    def take_value(s,value):
        """Zwraca obiekt Cash zawierający odliczoną sume tak aby składała się ona z jak najmniejszej liczby dostępnych monet.
        Rzuca wyjątek NotEnoughMoney w przypadku braku możliwości odliczenia sumy.
        """
        if(not isinstance(value, (float,int))):
            raise TypeError("'value' musi być liczbą.")

        if(value < 0):
            raise ValueError("Nie można wybrać ujemnej ilości pieniędzy.")

        if(value > s.total_value()):
            raise NotEnoughMoney("Brak wystarcającej ilości pieniędzy.")
        value_gr = round(value*100) #dokładna wartość w groszach typu int
        rest = Cash.empty()
        den_index = 0 

        while (value_gr>0):
            if(den_index>=len(denominations)):
                raise NotEnoughMoney("Brak możliwości wybrania odpowiednich nominałów (brak drobnych, nie można wydać malutkiej wartości).")
            den = denominations[den_index]
            required_quantity_of_coins = math.floor(value_gr/100/den)
            max_coins = s._content_[den].take(required_quantity_of_coins) #max_coins zawiera maksymalną liczbę potrzebnych monet jednego nominału jaką można wydać
            value_gr -= max_coins.get_total_raw_value()
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
    """Klasa przechowywująca wszystkie produkty, posegregowane według ich numeru, wraz z ich ilościami.
    """
    def __init__(s,product_list: list,number_from: int):
        """product_list - lista produktów, number_from - od jakiej liczby ma ponumerować"""
        if(not isinstance(number_from, int)):
            raise TypeError("'number_from' musi być typu int.")
        if(not isinstance(product_list,list) and not all(isinstance(p,Products) for p in product_list)):
            raise TypeError("'product_list' musi być listą obiektów typy Products.")
        list_nr=[i+number_from for i in range(len(product_list))] #List comprehension
        super().__init__(list_nr,product_list)

    def check_quantity(s, id: int) -> bool:
        """Sprawdza czy dany produkt się nie skończył bez rzucania wyjątku."""
        return (s._content_[id].get_quantity()<=0)

    def get_price(s,id: int) -> float:
        """Zwraca cene produktu o podanym id."""
        if(not isinstance(id, int)):
            raise TypeError("'id' musi byc typu int.")
        return s._content_[id].get_value()

    def add(s,den: float,q: int):
        """Zwraca wyjątek. Nie jesteś właścicielem.
        """
        raise NotImplementedError("Nie jesteś właścielem. Nie możesz uzupełniać produktów w asortymencie.")

    def __add__(s, o):
        """Zwraca wyjątek. Nie jesteś właścicielem."""
        raise NotImplementedError("Nie jesteś właścielem. Nie możesz uzupełniać produktów w asortymencie.")


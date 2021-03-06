from . import vending_utils as v_utils
from typing import List, Tuple, Type
import random

denominations = v_utils.denominations

# Wyjątki:

class IdOutOfRangeError(Exception):
    """Wyjątek oznaczający wybranie złego id produktu"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CannotGiveRest(Exception):
    """Wyjątek oznaczający brak możlwiości wydania reszty"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class LackOfProduct(Exception):
    """Wyjatek oznaczający brak wybranego produktu"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotEnoughPayment(Exception):
    """Wyjątek oznaczający brak wystarczającej zapłaty"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# Klasa właściwa
        
class VendingMachine:
    """Klasa obsługująca wydawanie produktów i reszty po przyjęciu monet
     od uzytkownika i zwracająca odpowiedni wyjątek w razie niepowodzenia (np. braku produktu)
     
    """
    def __init__(s,lista_produktów,bank=v_utils.Cash.equally_filled(100)):
        s._assortment_ = v_utils.Assortment(lista_produktów,30)
        s._bank = bank
        s._inserted_ = v_utils.Cash.empty()
        s._selected_product = 0
    
    @staticmethod
    def random_priced_products_generator(quantity: int=5):
        """Generuje produkty o losowych cenach, każdy w ilości 'quantity'."""
        for i in range(30,51):
            r = random.randrange(150,750,5)/100
            yield v_utils.Products("Produkt nr. "+str(i),r,quantity)

    @classmethod
    def filled(cls,price_generator):
        """Tworzy obiekt VendingMachine o danycn produktach."""
        return cls([p for p in price_generator()])
        
    def inserted(s) -> str:
        """Zwraca wartość wrzuconych monet, sformatowaną, gotową do wyświetlenia na ekranie."""
        return "{:.2f}".format(s._inserted_.total_value())

    def insert_coin(s,den: float) -> Tuple[v_utils.Products,v_utils.Cash]:
        """Wruca 1 monete o nominale 'den' do automatu."""
        if(isinstance(den,str)):
            den = float(den)
        if(not isinstance(den,(int,float))):
            raise TypeError("nominał musi być typu float, int lub string")
        if(den not in v_utils.denominations):
            raise ValueError("Nie istnieje moneta o podanym nominale: "+den)
        s._inserted_.add_coins(v_utils.Coins(den,1))
        
    def accept_transaction(s):
        """Zatwierdza transakcje, czyli dokona wydania produktu i reszty jeśli wszystkie warunki zostaną spełnione"""
        if(s._selected_product!=0):
            inserted_value = s._inserted_.total_value()
            product_price = s._assortment_.get_price(s._selected_product)
            if(inserted_value>=product_price): 
                try:
                    p = s._assortment_.take(s._selected_product,1)
                    r = s._bank.take_value(inserted_value-product_price)
                    s._bank = s._bank + s._inserted_
                    s._inserted_ = v_utils.Cash.empty()
                    s._selected_product=0
                    return p, r
                except v_utils.NotEnoughMoney as e:
                    raise CannotGiveRest("Brak możliwośći wydania reszty. Prosze odliczyć sume.")
                except v_utils.NotEnoughProduct as e:
                    raise LackOfProduct("Ten produkt się skończył.")  
            else:
                raise NotEnoughPayment("Wrzucono za mało monet.")
        return None, None

    def cancel_transaction(s):
        """Anuluj transakcje. Zwraca wrzucone w ramach transakcji monety."""
        rest = s._inserted_
        s._inserted_ = v_utils.Cash.empty()
        s._selected_product= 0
        return rest

    def select_product(s, id: int) -> str:
        """Wybiera produkt o danym id i zwraca jego cenę w postaci sformatowanej gotowej do wyświetlenia."""
        if(not isinstance(id,int)):
            raise ValueError("Id produktu musi być cyfrą.")
        if(id<30 or id>50):
            raise IdOutOfRangeError("Nieprawidlowy numer produktu.")
        s._selected_product = id
        if(s._assortment_.check_quantity(id)): #można teoretycznie sprawdzać dostępność produktu tutaj, ale według projektu informacja ta ma się pojawić po zapłacie, która potem zostanie zwrócona
            pass
            #raise LackOfProduct("Brak produktu.")
        return "{:.2f}".format(s._assortment_.get_price(id))


if __name__ == '__main__':
    print("Moduł wewnętrzny automatu z napojami. Aby go użyć - utwórz skrypt a w nim obiekt typu VendingMachine")
else:
    pass
    #moduł został zaimportowany, nie wypisuj nic

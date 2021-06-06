#import imp; imp.reload(modulename)
import vending as ven
from typing import List
import random

if __name__ == '__main__':
    print("Moduł wewnętrzny automatu z napojami")
    print(dir())
else:
    pass
    #moduł został zaimportowany, nie wypisuj nic

""" za pomocą #? oznaczyłem cechy nad którch ostateczną implementacją się jeszcze zastanawiam
    lub zamierzam usunąć jeśli nie zaistnieje potrzeba ich użycia
"""

denominations = ven.denominations

class IdOutOfRangeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CannotGiveRest(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class LackOfProduct(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotEnoughPayment(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)



class VendingMachine:
    """Klasa obsługująca wydawanie produktów i reszty po przyjęciu monet
     od uzytkownika i zwracająca odpowiedni wyjątek w razie niepowodzenia (np. braku produktu)
     
    """#!!!
    def __init__(s,lista_produktów,bank=ven.Cash.equally_filled(100)):
        s._assortment_ = ven.Assortment(lista_produktów,30)
        s._bank_ = bank
        s._inserted_ = ven.Cash.empty()
        s._selected_product_ = 0
        
    @classmethod
    def filled_with_random_price(cls,quantity=5):
        def get_random_price():
            r = random.randrange(150,750,5)/100
            return r

        return cls([ven.Products("Produkt nr. "+str(i),get_random_price(),5) for i in range(30,51)])
    
    def get_product(s,product_id: int,q: int=1):
        if(s._inserted_.total_value()<s._assortment_.get_price(product_id)*q):
            pass
        try:
            prods = s._assortment_.take(product_id,q) 
        except ven.NotEnoughProductError as e:
            raise LackOfProduct("Ten produkt się skończył.")   
            #GUI: brak produktu
            pass
        
    def inserted(s):
        return round(s._inserted_.total_value(),2)

    def insert_coin(s,den: str) -> (ven.Products,ven.Cash):
        """den - nominał"""
        # UWAGA: string czy int
        if(isinstance(den,str)):
            den = float(str)
        if(den not in ven.denominations):
            raise ValueError("Nie istnieje moneta o podanym nominale: "+den)
        s._inserted_.add_coins(ven.Coins(den,1))
        
    def accept_transaction(s):
        if(s._selected_product_!=0):
            inserted_value = s._inserted_.total_value()
            product_price = s._assortment_.get_price(s._selected_product_)
            if(inserted_value>=product_price): 
                try:
                    p = s._assortment_.take(s._selected_product_,1)
                    r = s._bank_.take_value(inserted_value-product_price)
                    s._bank_ = s._bank_ + s._inserted_
                    #print("BANK: "+str(s._bank_))
                    s._inserted_ = ven.Cash.empty()
                    s._selected_product_=0
                    return p, r
                except ven.NotEnoughMoney as e:
                    raise CannotGiveRest("Brak możliwośći wydania reszty. Prosze odliczyć sume.")
                except ven.NotEnoughProductError as e:
                    print("Hello1")
                    raise LackOfProduct("Ten produkt się skończył.")  
            else:
                raise NotEnoughPayment("Wrzucono za mało monet.")
        return None, None

    def cancel_transaction(s):
        reszta = s._inserted_.take_all()
        s._inserted_ = ven.Cash.empty()
        s._selected_product_= 0
        return reszta

    def select_product(s, id: int) -> float:
        """Wybiera produkt o danym id i zwraca jego cene"""
        if(not isinstance(id,int)):
            raise ValueError("Id produktu musi być cyfrą.")
        if(id<30 or id>50):
            raise IdOutOfRangeError("Nieprawidlowy numer produktu.")
        s._selected_product_ = id
        if(s._assortment_.check_quantity(id)):
            raise LackOfProduct("Brak produktu.")
        return s._assortment_.get_price(id)

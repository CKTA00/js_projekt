#import imp; imp.reload(modulename)
from . import vending_utils as v_utils
from typing import List, Tuple
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

denominations = v_utils.denominations

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
    def __init__(s,lista_produktów,bank=v_utils.Cash.equally_filled(100)):
        s._assortment_ = v_utils.Assortment(lista_produktów,30)
        s._bank_ = bank
        s._inserted_ = v_utils.Cash.empty()
        s._selected_product_ = 0
    
    @staticmethod # TODO: przenieś tą metode do v_utils?? chyba nie bo mamy 30,51
    def random_priced_products_generator(quantity: int=5):
        for i in range(30,51):
            r = random.randrange(150,750,5)/100
            yield v_utils.Products("Produkt nr. "+str(i),r,quantity)
    # Użycie tu genratora nie jest przerostem formy nad treścią, bo dzięki niemu możemy się upewnić, że nie zostaną wygenerowane
    #  produkty z poza zakresu i nie musimy używać range(30,51) (które można by łatwo pomylić z range(30,50) i co zdażyło mi się 
    #  w czasie procesu tworzenia aplikacji).
    #  Poprawia też czytelność kodu
    #  Generator ten jest używany w dwóch miejscach:
    #  - w metodzie klasowej filled
    #  - w inicjalizaji testów

    @classmethod
    def filled(cls,price_generator,quantity=5):
        return cls([p for p in price_generator()])
    
    # def get_product(s,product_id: int,q: int=1):
    #     if(s._inserted_.total_value()<s._assortment_.get_price(product_id)*q):
    #         pass
    #     try:
    #         prods = s._assortment_.take(product_id,q) 
    #     except v_utils.NotEnoughProductError as e:
    #         raise LackOfProduct("Ten produkt się skończył.")   
    #         #GUI: brak produktu
    #         pass
        
    def inserted(s) -> str:
        return "{:.2f}".format(s._inserted_.total_value())

    def insert_coin(s,den: float) -> Tuple[v_utils.Products,v_utils.Cash]:
        """den - nominał"""
        # UWAGA: string czy int
        if(isinstance(den,str)):
            den = float(den)
        if(den not in v_utils.denominations):
            raise ValueError("Nie istnieje moneta o podanym nominale: "+den)
        s._inserted_.add_coins(v_utils.Coins(den,1))
        
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
                    s._inserted_ = v_utils.Cash.empty()
                    s._selected_product_=0
                    return p, r
                except v_utils.NotEnoughMoney as e:
                    raise CannotGiveRest("Brak możliwośći wydania reszty. Prosze odliczyć sume.")
                except v_utils.NotEnoughProductError as e:
                    raise LackOfProduct("Ten produkt się skończył.")  
            else:
                raise NotEnoughPayment("Wrzucono za mało monet.")
        return None, None

    def cancel_transaction(s):
        reszta = s._inserted_.take_all()
        s._inserted_ = v_utils.Cash.empty()
        s._selected_product_= 0
        return reszta

    def select_product(s, id: int) -> str:
        """Wybiera produkt o danym id i zwraca jego cene"""
        if(not isinstance(id,int)):
            raise ValueError("Id produktu musi być cyfrą.")
        if(id<30 or id>50):
            raise IdOutOfRangeError("Nieprawidlowy numer produktu.")
        s._selected_product_ = id
        if(s._assortment_.check_quantity(id)):
            pass
            #raise LackOfProduct("Brak produktu.")
        return "{:.2f}".format(s._assortment_.get_price(id))

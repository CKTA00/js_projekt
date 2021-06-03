#import imp; imp.reload(modulename)
import vending as ven
from typing import List

if __name__ == '__main__':
    print("Moduł wewnętrzny automatu z napojami")
    print(dir())
else:
    pass
    #moduł został zaimportowany, nie wypisuj nic

""" za pomocą #? oznaczyłem cechy nad którch ostateczną implementacją się jeszcze zastanawiam
    lub zamierzam usunąć jeśli nie zaistnieje potrzeba ich użycia
"""



class VendingMachine:
    """Klasa obsługująca wydawanie produktów i reszty po przyjęciu monet
     od uzytkownika i zwracająca odpowiedni wyjątek w razie niepowodzenia (np. braku produktu)
     
    """
    #? Funkcje get i dodaj zostają nadpisane metodami wrzucania monet i odbierania reszty (i/lub produktu)
    #? lub zdefiniowanie innych funkcji i zrezygnowanie z dziedziczenia w tym wypadku

    def _init_(s,lista_produktów,bank=ven.Cash.napełniona_kasa()):
        s._assortment_ = ven.Assortment(lista_produktów,30)
        s._bank_ = bank
        s._inserted_ = ven.Cash.pusta_kasa()
    
    def get_product(s,product_id,q=1):
        if(s._inserted_.total_value()<s._assortment_.get_price(product_id)*q):
            #GUI: wrzucono niewystarczającą liczbę monet
            pass
        try:
            prods = s._assortment_.take(product_id,q) 
        except ven.NotEnoughProductError():
            #GUI: brak produktu
            pass
        
    def product_price(s,numer):
        return s._assortment_.get_price(numer)

    def insert_coin(s,den):
        """den - nominał"""
        # UWAGA: string czy int
        if(isinstance(den,str)):
            den = float(str)
        if(den not in ven.denominations):
            raise ValueError("Nie istnieje moneta o podanym nominale: "+den)
        s._inserted_.add(den,1)
        # UWAGA: update label

    def cancel_transaction(s):
        reszta = s._inserted_.take_all()
        s._inserted_ = ven.Cash.pusta_kasa()
        return reszta

        

    


        


    

            


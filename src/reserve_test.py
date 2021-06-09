# UWAGA: Te testy są tu na wszelki wypadek, gdyby nie udało się zaimportować pakitu machine w pliku z katalogu test
# Więcej informacji w raporcie w dziale "zaimplementowane testy"

import unittest
import machine.vending_machine as vm
import machine.vending_utils as v_utils

class TestMachine(unittest.TestCase):
    def __init__(s, *args, **kargs):
        s.product_list = [p for p in vm.VendingMachine.random_priced_products_generator()]
        s.max_precision = 3
        super().__init__(*args, **kargs)
    
    def get_product(s,id: int) -> v_utils.Products:
        """Funkcja pomocnicza, zwraca dany produkt"""
        return s.product_list[id-30]

    def set_product(s,id: int,new_product: v_utils.Products) -> None:
        """Funkcja pomocnicza, podmienia produkt na nowy"""
        s.product_list[id-30] = new_product
        
    def test_1(s):
        """Sprawdzenie ceny jednego towaru - oczekiwana informacja o cenie."""
        v = vm.VendingMachine(s.product_list)
        s.assertEqual(s.get_product(35).get_formated_value(),v.select_product(35))

    def test_2(s):
        """Wrzucenie odliczonej kwoty, zakup towaru - oczekiwany brak reszty."""
        s.set_product(35, v_utils.Products("produkt testowy o znanej cenie",6.5,5))
        v = vm.VendingMachine(s.product_list)
        # przy okazji testowanie różnych typów danych:
        v.insert_coin("5")
        v.insert_coin(1) 
        v.insert_coin(0.5)
        v.select_product(35)
        product, rest = v.accept_transaction()
        s.assertIsNotNone(product)
        s.assertAlmostEqual(rest.total_value(),0.0,s.max_precision)

    def test_3(s):
        """Wrzucenie większej kwoty, zakup towaru - oczekiwana reszta."""
        s.set_product(35, v_utils.Products("produkt testowy o znanej cenie",2.2,5))
        v = vm.VendingMachine(s.product_list)
        v.select_product(35)
        # przy okazji testowanie różnych typów danych:
        v.insert_coin(2)
        v.insert_coin("0.5")
        product, rest = v.accept_transaction()
        s.assertIsNotNone(product)
        s.assertAlmostEqual(rest.total_value(),0.3,s.max_precision)

    def test_4(s):
        """Wykupienie całego asortymentu, próba zakupu po wyczerpaniu towaru -oczekiwana informacja o braku."""
        v = vm.VendingMachine(s.product_list)
        for i in range(5):
            v.select_product(35)
            v.insert_coin(5)
            v.insert_coin(5)
            v.accept_transaction()
        
        v.select_product(35)
        v.insert_coin(5)
        v.insert_coin(5)
        s.assertRaises(vm.LackOfProduct,v.accept_transaction)
    
    def test_5(s):
        """Sprawdzenie ceny towaru o nieprawidłowym numerze (<30 lub >50) - oczekiwana informacja o błędzie."""
        v = vm.VendingMachine(s.product_list)
        s.assertRaises(vm.IdOutOfRangeError,v.select_product,25)

    def test_6(s):
        """Wrzucenie kilku monet, przerwanie transakcji - oczekiwany zwrot monet."""
        v = vm.VendingMachine(s.product_list)
        coins = v_utils.Cash.empty()
        coins.add(2,1)
        coins.add(0.2,1)
        coins.add(0.02,1)
        v.insert_coin(2)
        v.insert_coin(0.2)
        v.insert_coin(0.02)
        rest = v.cancel_transaction()
        s.assertEqual(coins,rest)

    def test_7(s):
        """Wrzucenie za małej kwoty, wybranie poprawnego numeru towaru, wrzucenie reszty monet do odliczonej kwoty,
         ponowne wybranie poprawnego numeru towaru - oczekiwany brak reszty."""
        s.set_product(35, v_utils.Products("produkt testowy o znanej cenie",4.5,5))
        v = vm.VendingMachine(s.product_list)
        # przy okazji testowanie różnych typów danych:
        v.insert_coin(2)
        v.insert_coin(2)
        v.select_product(35)
        v.insert_coin(0.5)
        product, rest = v.accept_transaction()
        s.assertIsNotNone(product)
        s.assertAlmostEqual(rest.total_value(),0.0,s.max_precision)

    def test_8(s):
        """Zakup towaru płacąc po 1 gr - suma stu monet ma być równa 1zł (dla floatów suma sto
         razy 0.01+0.01 +...+0.01 nie będzie równa 1.0). Płatności można dokonać za pomocą pętli for w interpreterze."""
        s.set_product(35, v_utils.Products("produkt za złotówke",1.0,5))
        v = vm.VendingMachine(s.product_list)
        v.select_product(35)
        for i in range(100):
            v.insert_coin(0.01)
        product, rest = v.accept_transaction()
        s.assertIsNotNone(product)
        s.assertAlmostEqual(rest.total_value(),0.0,s.max_precision)

    def test_cannot_give_rest(s):
        """Dodatkowy test: Utworzenie automatu z pustym bankiem. Zapłacenie za dużo za produkt - oczekiwana informacja o braku możliwości wydania reszty
        """
        s.set_product(35, v_utils.Products("produkt testowy o znanej cenie",4.0,5))
        v = vm.VendingMachine(s.product_list,v_utils.Cash.empty())
        v.insert_coin(5)
        v.select_product(35)
        s.assertRaises(vm.CannotGiveRest,v.accept_transaction)
        

if __name__ == '__main__':
    unittest.main()
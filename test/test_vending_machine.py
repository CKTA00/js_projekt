import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src") #windows
sys.path.append("../src") #pozostałe platformy
import machine.vending_machine as vm
#import machine.vending_utils as v_utils

class TestMachine(unittest.TestCase):
    def __init__(s):
        s.product_list = [p for p in vm.VendingMachine.random_priced_products_generator()]
        
    def test_1(s):
        """Sprawdzenie ceny jednego towaru - oczekiwana informacja o cenie."""
        v = vm.VendingMachine(s.product_list)

    def test_2(s):
        """Wrzucenie odliczonej kwoty, zakup towaru - oczekiwany brak reszty."""
        v = vm.VendingMachine(s.product_list)

    def test_3(s):
        """Wrzucenie większej kwoty, zakup towaru - oczekiwana reszta."""
        v = vm.VendingMachine(s.product_list)

    def test_4(s):
        """Wykupienie całego asortymentu, próba zakupu po wyczerpaniu towaru -oczekiwana informacja o braku."""
        v = vm.VendingMachine(s.product_list)
    
    def test_5(s):
        """Sprawdzenie ceny towaru o nieprawidłowym numerze (<30 lub >50) - oczekiwana informacja o błędzie."""
        v = vm.VendingMachine(s.product_list)

    def test_6(s):
        """Wrzucenie kilku monet, przerwanie transakcji - oczekiwany zwrot monet."""
        v = vm.VendingMachine(s.product_list)

    def test_7(s):
        """Wrzucenie za małej kwoty, wybranie poprawnego numeru towaru, wrzucenie reszty monet do odliczonej kwoty,
         ponowne wybranie poprawnego numeru towaru - oczekiwany brak reszty."""
        v = vm.VendingMachine(s.product_list)

    def test_2(s):
        """Zakup towaru płacąc po 1 gr - suma stu monet ma być równa 1zł (dla floatów suma sto
         razy 0.01+0.01 +...+0.01 nie będzie równa 1.0). Płatności można dokonać za pomocą pętli for w interpreterze."""
        v = vm.VendingMachine(s.product_list)

if __name__ == '__main__':
    unittest.main()
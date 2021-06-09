from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from machine import vending_machine as vm

LANG_PODAJ_NR = "wpisz nr. produktu" # stała używana w kilku miejscach

class VendingMachineGUI():
    """Klasa obsługująca GUI, łącząca je z funkcjami pakietu machine"""
    def __init__(s,wait_for_ok=False):
        s._root = Tk()
        s._root.title("Automat z napojami")
        s._root.minsize(300,400)
        s._screen_text = StringVar()
        s._screen_text.set("")
        s._price_text = StringVar()
        s._price_text.set(LANG_PODAJ_NR)
        s._numbers = ""
        s._wait_for_ok = wait_for_ok
        s._vending_machine = vm.VendingMachine.filled(vm.VendingMachine.random_priced_products_generator)
        s._denoms = vm.denominations
        s._layout(s._root)
        s._root.mainloop()

    def _layout(s,root: Tk):
        """Inicjalizacja elementów GUI i podpięcie pod nich funkcjonalności"""
        s._output_screen = Label(root, font=Font(size=40), fg="green", bg="black",textvariable=s._screen_text)
        s._output_screen.grid(column=0, row=0, columnspan=3,sticky="ew")
        s._price_screen = Label(root, font=Font(size=20), fg="green", bg="black",textvariable=s._price_text)
        s._price_screen.grid(column=0, row=1, columnspan=3,sticky="ew")
        s.number_panel = [Button(root,text=str(i+1),font=Font(size=16),pady=5,padx=10,command=lambda ii=i: s.number_click(ii+1)).grid(row=i//3+2,column=i%3,sticky="news") for i in range(9)] #List comprehensions
        s._zero_button = Button(root,text="0",font=Font(size=16),pady=5,padx=10,command=lambda: s.number_click(0)) #List comprehensions
        s._zero_button.grid(row=5,column=1,sticky="news")
        s.cancel_button = Button(root,text="Anuluj",font=Font(size=9),pady=5,command=s.cancel)
        s.cancel_button.grid(row=5,column=0,sticky="news")
        s.ok_button = Button(root,text="OK",font=Font(size=9),pady=5,command=s.ok)
        s.ok_button.grid(row=5,column=2,sticky="news")
        s.insert_coin_panel = [Button(root,text="Wrzuć "+str(s._denoms[i]),pady=1,command=lambda ii=i: s.insert_coin(s._denoms[ii])).grid(row=7+i,column=0,columnspan=3,sticky="ew") for i in range(len(s._denoms))] #List comprehensions
        s.insert_label = Label(root,text="\nWrzuć do automatu:")
        s.insert_label.grid(row=6,column=0,columnspan=3)
        root.grid_columnconfigure((0,1,2),weight=1)
        root.grid_rowconfigure((0,1),weight=0)
        root.grid_rowconfigure((2,3,4,5),weight=3)
        root.grid_rowconfigure((6,7,8,9,10,11,12,13,14,15),weight=1)

    def number_click(s,number: int):
        """Obsługa przycisków z numerami do wyboru produktu."""
        if(len(s._numbers)==0 or len(s._numbers)==2):
            s._numbers = str(number)
        elif(len(s._numbers)==1):
            s._numbers += str(number)
            try:
                price = s._vending_machine.select_product(int(s._numbers))
                s._price_text.set("cena: "+price)
            except vm.IdOutOfRangeError as e:
                messagebox.showinfo("Nieprawidłowy numer",e)
                s._numbers = ""
            except vm.LackOfProduct as e:
                pass #Nie ma prduktu ale kontynuuj! Wiadomość o barku ma się pojawić po zapłacie.
            if(not s._wait_for_ok):
                s.ok(False)
        s._screen_text.set(s._numbers)
        
    def insert_coin(s,den):
        """Osługa przycików do wrzucania monet"""
        s._vending_machine.insert_coin(den)
        if(not s._wait_for_ok):
            s.ok(False)
        s._screen_text.set(s._vending_machine.inserted())
        s._numbers="" #anuluj wprowadzanie numeru produktu

    def cancel(s):
        """Obsługa przycisku [Anuluj]"""
        rest = s._vending_machine.cancel_transaction()
        messagebox.showinfo("Transakcja anulowana","Automat zwrócił poniższe monety:\n"+str(rest))
        s._numbers = ""
        s._screen_text.set("")
        s._price_text.set(LANG_PODAJ_NR)
        pass

    def ok(s,inform_user=True):
        """Obsługa przycisku [OK]. Jeśli wait_for_ok jest False to funkcja ta jest automatycznie wołana w czasie innych akcji.
        """
        try:
            product, rest = s._vending_machine.accept_transaction()
            if(product is not None and rest is not None):
                messagebox.showinfo("Sukces","Automat wydał następujące rzeczy:\n"+str(product)+"\n"+str(rest))
                s._numbers = ""
                s._screen_text.set("")
                s._price_text.set(LANG_PODAJ_NR)
        except vm.LackOfProduct as e:
            messagebox.showinfo("Brak produktu",e)
            s.cancel()
        except vm.CannotGiveRest as e:
            messagebox.showinfo("Brak monet",e)
            s.cancel()
        except vm.NotEnoughPayment as e:
            if(s._wait_for_ok): #powoduje brak wykakującego okna informującego o niewystarczającej ilości monet za kazdym razem gdy użytkownik wrzuca monete
                messagebox.showinfo("Za mało",e)
            
# Rozpocznij skrypt:
if __name__ == '__main__':
    vgui = VendingMachineGUI()
    #vgui = VendingMachineGUI(wait_for_ok=True) # alternatywny tryb działania - czekaj aż użytkownik potwierdzi
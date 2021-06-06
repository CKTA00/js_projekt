from math import prod
from os import waitpid
from tkinter import *
from tkinter import messagebox
import time
from tkinter.font import Font, families

import vending_machine as vm

LANG_PODAJ_NR = "wpisz nr. produktu"

class VendingMachineGUI():
    def __init__(s,wait_for_ok=False):
        s.root = Tk()
        s.root.title("Automat z napojami")
        s.root.minsize(300,400)
        s.screen_text = StringVar()
        s.screen_text.set("")
        s.price_text = StringVar()
        s.price_text.set(LANG_PODAJ_NR)
        s.numbers = ""
        s.wait_for_ok = wait_for_ok
        s.transaction_mode = False
        s.vending_machine = vm.VendingMachine.filled_with_random_price()
        s.denoms = vm.denominations
        s.layout(s.root)
        s.root.mainloop()
        

    def layout(s,root: Tk):
        #s.outputScreenChars = ["0" for i in range(5)]
        #s.outputScreenChars[2] = "."
        #s.outputScreen = [Label(root, font=Font(size=40), fg="green", bg="black", text=s.outputScreenChars[i]).grid(column=i,row=0) for i in range(5)]
        s.output_screen = Label(root, font=Font(size=40), fg="green", bg="black",textvariable=s.screen_text)
        s.output_screen.grid(column=0, row=0, columnspan=3,sticky="ew")
        s.price_screen = Label(root, font=Font(size=20), fg="green", bg="black",textvariable=s.price_text)
        s.price_screen.grid(column=0, row=1, columnspan=3,sticky="ew")
        s.number_panel = [Button(root,text=str(i+1),font=Font(size=16),pady=5,padx=10,command=lambda ii=i: s.number_click(ii+1)).grid(row=i//3+2,column=i%3,sticky="news") for i in range(9)] #List comprehensions
        s.zero_button = Button(root,text="0",font=Font(size=16),pady=5,padx=10,command=lambda: s.number_click(0)) #List comprehensions
        s.zero_button.grid(row=5,column=1,sticky="news")
        s.cancel_button = Button(root,text="Anuluj",font=Font(size=9),pady=5,command=s.cancel)
        s.cancel_button.grid(row=5,column=0,sticky="news")
        s.ok_button = Button(root,text="OK",font=Font(size=9),pady=5,command=s.ok)
        s.ok_button.grid(row=5,column=2,sticky="news")
        s.insert_coin_panel = [Button(root,text="Wrzuć "+str(s.denoms[i]),pady=1,command=lambda ii=i: s.insert_coin(s.denoms[ii])).grid(row=7+i,column=0,columnspan=3,sticky="ew") for i in range(len(s.denoms))] #List comprehensions
        s.insert_label = Label(root,text="\nWrzuć do automatu:")
        s.insert_label.grid(row=6,column=0,columnspan=3)
        root.grid_columnconfigure((0,1,2),weight=1)
        root.grid_rowconfigure((0,1),weight=0)
        root.grid_rowconfigure((2,3,4,5),weight=3)
        root.grid_rowconfigure((6,7,8,9,10,11,12,13,14,15),weight=1)


    def number_click(s,number: int):
        if(len(s.numbers)==0 or len(s.numbers)==2):
            s.numbers = str(number)
        elif(len(s.numbers)==1):
            s.numbers += str(number)
            try:
                price = s.vending_machine.select_product(int(s.numbers))
                s.transaction_mode = True
                s.price_text.set("cena: "+str(price))
            except vm.IdOutOfRangeError as e:
                messagebox.showinfo("Nieprawidłowy numer",e)
                s.numbers = ""
            except vm.LackOfProduct as e:
                pass #Nie ma prduktu ale kontynuuj! Wiadomość o barku po zapłacie.
            if(not s.wait_for_ok):
                s.ok(False)
        s.screen_text.set(s.numbers)
        

    def insert_coin(s,den):
        s.vending_machine.insert_coin(den)
        if(not s.wait_for_ok):
            s.ok(False)
        s.screen_text.set("{:.2f}".format(s.vending_machine.inserted()))
        s.numbers="" #anuluj wprowadzanie numeru produktu

    def cancel(s):
        reszta = s.vending_machine.cancel_transaction()
        messagebox.showinfo("Transakcja anulowana","Automat zwrócił poniższe monety:\n"+str(reszta))
        s.numbers = ""
        s.screen_text.set("")
        s.price_text.set(LANG_PODAJ_NR)
        s.transaction_mode=False
        pass

    def ok(s,inform_user=True):
        try:
            if(not s.wait_for_ok):
                product, rest = s.vending_machine.accept_transaction()
                if(product is not None and rest is not None):
                    messagebox.showinfo("Sukces","Automat wydał następujące rzeczy:\n"+str(product)+"\n"+str(rest))
                    s.numbers = ""
                    s.price_text.set(LANG_PODAJ_NR)
                    s.transaction_mode=False
        except vm.LackOfProduct as e:
            print("Hello")
            messagebox.showinfo("Brak produktu",e)
            s.cancel()
        except vm.CannotGiveRest as e:
            messagebox.showinfo("Brak monet",e)
            s.cancel()
        except vm.NotEnoughPayment as e:
            if(inform_user):
                messagebox.showinfo("Za mało",e)
            

    

if __name__ == '__main__':
    vgui = VendingMachineGUI()
else:
    pass
    print("Moduł zaimportowany. Generowanie gui wyłączone.")
    v = vm.VendingMachine()
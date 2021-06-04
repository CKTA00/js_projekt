from tkinter import *
import tkinter
from tkinter.font import Font, families

from vending_machine import VendingMachine


class VendingMachineGUI():
    def __init__(s,vending_machine):
        s.root = Tk()
        s.root.title("Automat z napojami")
        s.layout(s.root)
        s.root.mainloop()
        s.vending_machine = vending_machine


    def layout(s,root):
        s.outputScreenChars = ["0" for i in range(5)]
        s.outputScreenChars[2] = "."
        s.outputScreen = [Label(root, font=Font(size=40), fg="green", bg="black", text=s.outputScreenChars[i]).grid(column=i,row=0) for i in range(5)]
    

if __name__ == '__main__':
    v = VendingMachine()
    vgui = VendingMachineGUI(v)
else:
    pass
    print("Moduł zaimportowany. Generowanie gui wyłączone.")
    v = VendingMachine()
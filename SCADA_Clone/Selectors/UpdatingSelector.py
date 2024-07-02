import tkinter as tk
from tkinter import ttk
from typing import Tuple, Callable, Any, List

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CustomElements.Element import Element
from IUpdatingSelector import IUpdatingSelector
from SelectorValues import SelectorValues

class UpdatingSelector(Element, IUpdatingSelector):
    def __init__(self, root : tk.Misc, value_changed_handler : Callable[[str], Any], selector_values : SelectorValues, height = 20):
        self.__root = root
        self.__value_changed_handler = value_changed_handler
        self.__selector_values = selector_values

        self.__selector = ttk.Combobox(self.__root, state="readonly", values=selector_values.get_values())
        self.__selector.bind("<<ComboboxSelected>>", self.__pin_changed)

        self.__prev_value = selector_values.get_values()[0]
        self.__new_value : str

        self.__selector.set(self.__prev_value)
        
        super().__init__(self.__selector, height=height)

        self.__selector_values.add_selector(self)

    def update_values(self, values : List[str]):
        self.__selector.configure(values=values)

    def __pin_changed(self, event):
        self.__root.focus()
        self.__new_value = self.__selector.get()
        self.__selector_values.swap_value(self.__prev_value, self.__new_value)
        self.__prev_value = self.__new_value
        self.__value_changed_handler(self.__new_value)

    def is_empty(self):
        return self.__selector.get() == "Empty"
    
    def get_value(self):
        self.__selector.get()

    def clear(self):
        self.__selector_values.add_value(self.__prev_value)
        self.__prev_value = "Empty"
        self.__selector.set(self.__prev_value)

def f(str : str):
    print(str)

if __name__ == "__main__":

    values = SelectorValues(["GPIO0", "GPIO1", "GPIO4", "GPIO17", "GPIO18", "GPIO22", "GPIO23", "GPIO27"], True)

    root = tk.Tk()
    app1 = UpdatingSelector(root, f, values)
    app1.set_coordinates(10, 10, 200)
    app1.place()
    app2 = UpdatingSelector(root, f, values)
    app2.set_coordinates(10, 40, 200)
    app2.place()
    app3 = UpdatingSelector(root, f, values)
    app3.set_coordinates(10, 70, 200, 20)
    app3.place()
    root.mainloop()
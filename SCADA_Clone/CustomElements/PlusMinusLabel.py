import tkinter as tk
from tkinter import ttk
from typing import Callable, Any

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from Element import Element

class PlusMinusLabel(Element):
    def __init__(self, root : tk.Misc, text : str, min_value : int, max_value : int, start_value : int, val_changed_hadler : Callable[[int], Any], height = 25, font = ("Arial", 12)):
        self.__root = root
        self.__val_changed_hadler = val_changed_hadler

        if (min_value > max_value):
            min_value, max_value=max_value, min_value

        self.__min_value = min_value
        self.__max_value = max_value
        self.__current_value = start_value
        self.__constrain_value()

        self.__font = font
        self.__text = text
        self.__container = ttk.Frame(self.__root)
        super().__init__(self.__container, height=height)

        self.__elements_margin = 5

        self.__create_elements()
        
    def __create_elements(self):
        max_value_len = max(len(str(self.__min_value)), len(str(self.__max_value)))
        max_text = self.__text + "0" * max_value_len
        self.__label = Element(ttk.Label(self.__container, anchor=tk.W, font=self.__font, text=max_text), height=self._height)
        self.__update_label()
        self.__plus_button = Element(ttk.Button(self.__container, text="+", command=self.__plus_hadler),
                                     self._height, self._height)
        self.__minus_button = Element(ttk.Button(self.__container, text="-", command=self.__minus_hadler),
                                      self._height, self._height)
        
        x, _ = self.__label.set_coordinates()
        x, _ = self.__plus_button.set_coordinates(x + self.__elements_margin)
        x, y = self.__minus_button.set_coordinates(x + self.__elements_margin)

        self.set_sizes(x, y)

    def __constrain_value(self):
        self.__current_value = min(self.__current_value, self.__max_value)
        self.__current_value = max(self.__current_value, self.__min_value)

    def __update_label(self):
        self.__label.get_element().configure(text=self.__text + str(self.__current_value))

    def __update_value(self):
        self.__root.focus()
        self.__constrain_value()
        self.__update_label()
        self.__val_changed_hadler(self.__current_value)

    def __plus_hadler(self):
        self.__current_value += 1
        self.__update_value()

    def __minus_hadler(self):
        self.__current_value -= 1
        self.__update_value()

    def place(self):
        super().place()
        self.__label.place()
        self.__plus_button.place()
        self.__minus_button.place()

    def change_value(self, new_value):
        self.__current_value = new_value
        self.__update_value()

    def get_value(self) -> int:
        return self.__current_value

def func(arg):
    print(arg)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlusMinusLabel(root, "Name: ", 1, 5, 3, func)
    app.set_coordinates(10, 20)
    app.place()
    root.mainloop()
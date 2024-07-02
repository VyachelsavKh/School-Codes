import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from enum import Enum, auto
from typing import Tuple, Callable, Any

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from CustomElements.Element import Element
from CustomElements.LabelEntry import LabelEntry
from Enums import *
from ExpannsionsModules.ExpansionModulePicker import ExpansionModulePicker

class Module(Element):
    __min_width = 200
    __min_height = 170

    def __init__(self, root):
        self.__root = root 
        
        super().__init__(ttk.Frame(self.__root, relief="groove"))
        
        self.__container = Element(ttk.Frame(self._element))

        self.__name = "Module"
        self.__state = SchemeState.USAGE

        self.__name_height = 20

        self.__enter_name = LabelEntry(self.__container.get_element(), "Name:", 20, self.__name, height=self.__name_height)
        self.__usage_name = Element(tk.Label(self.__container.get_element(), anchor=tk.CENTER, background="light grey", text=self.__name), height=self.__name_height)

        self.__gpio_expansion = ExpansionModulePicker(self.__container.get_element())

        self.__top_margin = 8
        self.__bottom_margin = 8
        self.__left_matgin = 8
        self.__right_margin = 8

        self.__elemnts_margin = 5

        self.__gpio_expansion.change_state(self.__state)

    @staticmethod
    def min_width():
        return Module.__min_width
    @staticmethod
    def min_height():
        return Module.__min_height
    
    def change_state(self, state : SchemeState):
        self.__state = state

        self.__gpio_expansion.change_state(state)

        if (state == SchemeState.USAGE):
            self.__name = self.__enter_name.get_entry()
            self.__usage_name.get_element().configure(text = self.__name)

        self.place()

    def set_coordinates(self, x : int, y : int, width : int, height : int) -> Tuple[int, int]:
        remain_width = width - self.__left_matgin - self.__right_margin
        remain_height = height - self.__top_margin - self.__bottom_margin

        self.__container.set_coordinates(self.__left_matgin, self.__top_margin, remain_width, remain_height)

        self.__usage_name.set_coordinates(width=remain_width)
        _, h = self.__enter_name.set_coordinates(width=remain_width)

        expansion_height = remain_height - h - self.__elemnts_margin

        self.__gpio_expansion.set_coordinates(0, h + self.__elemnts_margin, remain_width, expansion_height)

        return super().set_coordinates(x, y, width, height)
    
    def place(self):
        if self.__state == SchemeState.USAGE and self.__gpio_expansion.is_empty():
            super().place_forget()
            return
        
        super().place()
        self.__container.place()
        self.__gpio_expansion.place()

        if self.__state == SchemeState.SETTINGS:
            self.__enter_name.place()
        else:
            self.__enter_name.place_forget()

        if self.__state == SchemeState.USAGE:
            self.__usage_name.place()
        else:
            self.__usage_name.place_forget()
    
    def clear(self):
        self.__gpio_expansion.clear()
        self._element.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Module(root)
    app.set_coordinates(10, 10,  200, 160)
    app.place()
    app.change_state(SchemeState.SETTINGS)
    root.after(6000, lambda : app.change_state(SchemeState.USAGE))
    root.mainloop()
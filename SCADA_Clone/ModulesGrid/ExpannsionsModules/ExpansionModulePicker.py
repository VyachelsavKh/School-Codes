import tkinter as tk
from tkinter import ttk
from typing import Tuple, List, Type

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from CustomElements.Element import Element
from Enums import *
from GPIOExpansions.ExpansionsVariants import *

class ExpansionModulePicker(Element):
    def __init__(self, root : tk.Misc):
        self.__root = root

        self.__container = ttk.Frame(self.__root)
        super().__init__(self.__container)

        self.__usage_conntainer = ttk.Frame(self.__root)
        self.__usage = Element(self.__usage_conntainer)
        
        self.__gpio_expansions : List[Type[GPIOExpansion]] = [RaspberryExpansion]
        self.__gpio_expansions_names = ["Empty"] + [expansion.get_name() for expansion in self.__gpio_expansions]
        self.__current_expansion : GPIOExpansion | None = None

        self.__expansion_select_height = 20

        self.__expansion_select = Element(ttk.Combobox(self.__container, values=self.__gpio_expansions_names, state="readonly"), height=self.__expansion_select_height)
        self.__expansion_select.get_element().current(0)
        self.__expansion_select.get_element().bind("<<ComboboxSelected>>", self.__expansion_changed)

        self.__state = SchemeState.USAGE

        self.__last_expansion_id = 0

        self.__elements_margin = 5

    def __expansion_changed(self, event):
        self.__root.focus()

        id = self.__expansion_select.get_element().current()

        if self.__last_expansion_id == id:
            return

        if self.__current_expansion is not None:
            self.__current_expansion.clear()
            self.__current_expansion.place_forget()

        if id == 0:
            self.__current_expansion = None
        else:
            self.__current_expansion = self.__gpio_expansions[id - 1](self.__container, self.__usage_conntainer)
            self._set_current_expansion()
            self.__current_expansion.change_state(self.__state)
            self.__current_expansion.place()

        self.__last_expansion_id = id

    def change_state(self, state : SchemeState):
        self.__state = state

        if self.__current_expansion is not None:
            self.__current_expansion.change_state(state)

        self.place()

    def _set_current_expansion(self):
        if self.__current_expansion is not None:
            self.__current_expansion.set_coordinates(0, self._expansion_settings_y, self._width, self._expansion_settings_height)
            self.__current_expansion.set_usage_coordinates(width=self._width, height=self._height)

    def set_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        self.__usage.set_coordinates(x, y, width, height)

        _, h = self.__expansion_select.set_coordinates(width=width)

        self._expansion_settings_y = h + self.__elements_margin
        self._expansion_settings_height = height - self._expansion_settings_y

        self._set_current_expansion()

        return super().set_coordinates(x, y, width, height)

    def place(self):
        super().place()

        if self.__state == SchemeState.SETTINGS:
            self.__expansion_select.place()
        else:
            self.__expansion_select.place_forget()

        if self.__state == SchemeState.USAGE:
            self.__usage.place()
        else:
            self.__usage.place_forget()

        if self.__current_expansion is not None:
            self.__current_expansion.place()

    def is_empty(self) -> bool:
        if self.__current_expansion is None:
            return True
        
        return self.__current_expansion.is_empty()
    
    def clear(self):
        if self.__current_expansion is not None:
            self.__current_expansion.clear()
            del self.__current_expansion
            self.__current_expansion = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpansionModulePicker(root)
    app.set_coordinates(10, 10,  200, 160)
    app.place()
    root.after(3000, lambda : app.change_state(SchemeState.SETTINGS))
    root.mainloop()
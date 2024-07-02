import tkinter as tk
from tkinter import ttk
from typing import Tuple, Callable, Any, List

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from CustomElements.Element import Element
from GPIOModules.GPIOModules import *
from Enums import *

class GPIOExpansion(Element):
    @staticmethod
    def get_name():
        return "GPIOExpansion"
    
    def __init__(self, root : tk.Misc, usage_root : tk.Misc):
        self.__root = root

        self._usage_root = usage_root

        self._container = ttk.Frame(self.__root)
        super().__init__(self._container)
        
        self._set_GPIO_modules()
        
        self.__gpio_modules_names = ["Empty"] + [module.get_name() for module in self._gpio_modules]
        self.__current_module : BaseModule | None = None
        
        self.__module_select_height = 20
        
        self.__module_select = Element(ttk.Combobox(self._container, values=self.__gpio_modules_names, state="readonly"), height=self.__module_select_height)
        self.__module_select.get_element().current(0)
        self.__module_select.get_element().bind("<<ComboboxSelected>>", self.__module_changed)
        
        self.__last_module_id = 0

        self.__state = SchemeState.USAGE

        self.__elements_margin = 5


    def _set_GPIO_modules(self):
        self._gpio_modules : List[BaseModule]
        pass

    def __module_changed(self, event):
        self.__root.focus()

        id = self.__module_select.get_element().current()

        if self.__last_module_id == id:
            return

        if (self.__current_module is not None):
            self.__current_module.clear()

        if (id == 0):
            self.__current_module = None
        else:
            self.__current_module = self._gpio_modules[id - 1](self._container, self._usage_root)
            self._set_module_settings()
            self._set_module_usage()
            self.__current_module.change_state(self.__state)
            self.__current_module.place()

        self.__last_module_id = id

    def change_state(self, state : SchemeState):
        self.__state = state

        if self.__current_module is not None:
            self.__current_module.change_state(state)

    def _set_module_settings(self):
        if self.__current_module is not None:
            self.__current_module.set_coordinates(self._module_settings_x, self._module_settings_y, self._module_settings_width, self._module_settings_height)

    def set_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        _, h = self.__module_select.set_coordinates(width=width)

        self._module_settings_x = 0
        self._module_settings_y = h + self.__elements_margin
        self._module_settings_width = width
        self._module_settings_height = height

        self._set_module_settings()

        return super().set_coordinates(x, y, width, height)

    def _set_module_usage(self):
        if self.__current_module is not None:
            self.__current_module.set_usage_coordinates(self._module_usage_x, self._module_usage_y, self._module_usage_width, self._module_usage_height)
        
    def set_usage_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        self._module_usage_x = x
        self._module_usage_y = y
        self._module_usage_width = width
        self._module_usage_height = height

        self._set_module_usage()

        return x + width, y + width

    def place(self):
        super().place()

        if self.__state == SchemeState.SETTINGS:
            self.__module_select.place()
        else:
            self.__module_select.place_forget()

        if self.__current_module is not None:
            self.__current_module.place()

    def is_empty(self):
        if self.__current_module is None:
            return True
        
        return self.__current_module.is_empty()
    
    def clear(self):
        if self.__current_module is not None:
            self.__current_module.clear()
            del self.__current_module
            self.__current_module = None
        self._container.destroy()
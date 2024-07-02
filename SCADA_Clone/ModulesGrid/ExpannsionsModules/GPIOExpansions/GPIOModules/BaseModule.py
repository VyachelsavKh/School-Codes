import tkinter as tk
from tkinter import ttk
from typing import Tuple, Callable, Any, List

import sys
import os
from tkinter import Widget
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from CustomElements.Element import Element
from GPIOPins import *
from Enums import *

class BaseModule(Element):
    @staticmethod
    def get_name():
        return "Base"
    
    def __init__(self, root : tk.Misc, usage_root : tk.Misc, pins : SelectorValues = common_pins):
        self.__root = root
        self.__pins = pins
        self._usage_root = usage_root

        self._container = ttk.Frame(self.__root)
        super().__init__(self._container)

        self.__pin_selector_height = 20
        self.__pin_selector = UpdatingSelector(self._container, self.__pin_changed, self.__pins, self.__pin_selector_height)
        
        self._pin : str = self.__pin_selector.get_value()

        self._state = SchemeState.USAGE

        self._elemnts_margin = 5

    def __pin_changed(self, pin : str):
        self._pin = pin

    def _attach_pin(self, pin : str):
        print(pin)

    def _detach_pin(self):
        pass

    def change_state(self, state : SchemeState):
        self._state = state

        if self._pin is not None and self._pin != "Empty":
            if self._state == SchemeState.SETTINGS:
                self._detach_pin()
            elif self._state == SchemeState.USAGE:
                self._attach_pin(self._pin)

    def set_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        _, self._pin_selector_y = self.__pin_selector.set_coordinates(width=width)

        return super().set_coordinates(x, y, width, height)

    def set_usage_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        pass

    def _place_usage(self):
        pass
    def _forget_usage(self):
        pass

    def _place_settings(self):
        pass
    def _forget_settings(self):
        pass

    def place(self):
        super().place()

        if self._state == SchemeState.SETTINGS:
            self.__pin_selector.place()
            self._place_settings()
        else:
            self.__pin_selector.place_forget()
            self._forget_settings()

        if self._state == SchemeState.USAGE:
            self._place_usage()
        else:
            self._forget_usage()

    def is_empty(self):
        return self.__pin_selector.is_empty()
    
    def clear(self):
        self.__pin_selector.clear()
        self.__pins.remove_selector(self.__pin_selector)
        self._container.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app1 = BaseModule(root, root)
    app1.set_coordinates(10, 10,  200, 160)
    app1.change_state(SchemeState.SETTINGS)
    app1.place()
    app2 = BaseModule(root, root)
    app2.set_coordinates(10, 40,  200, 160)
    app2.change_state(SchemeState.SETTINGS)
    app2.place()
    root.after(3000, lambda : app1.clear())
    root.mainloop()
import tkinter as tk
from tkinter import ttk
from typing import Tuple, Callable, Any, List

import sys
import os
from tkinter import Misc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from CustomElements.Element import Element
from BaseModule import *
from Enums import *

class DiscreteOutputModule(BaseModule):
    @staticmethod
    def get_name():
        return "Discrete output"

    def __init__(self, root : tk.Misc, usage_root : tk.Misc, pins : SelectorValues = common_pins):
        super().__init__(root, usage_root, pins)

        self.__discrete_value : int = 0

        self.__colors = ["red", "green"]

        self._canvas = tk.Canvas(self._usage_root)
        self._button_canvas = Element(self._canvas)
        self._button = self._canvas.create_rectangle(0, 0, 10, 10, outline="black", width=10)
        self._canvas.tag_bind(self._button, "<Button-1>", self._toggle_click)

        self._paint_button()

    def _send_value(self, value : int):
        print(value)

    def _paint_button(self):
        self._canvas.itemconfig(self._button, fill = self.__colors[self.__discrete_value])

    def _toggle_click(self, event):
        self.__discrete_value += 1
        self.__discrete_value %= 2

        self._paint_button()

        self._send_value(self.__discrete_value)

    def set_usage_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        self._button_canvas.set_coordinates(x, y, width, height)
        self._canvas.coords(self._button, 0, 0, width, height)

    def _place_usage(self):
        self._button_canvas.place()

    def _forget_usage(self):
        self._button_canvas.place_forget()

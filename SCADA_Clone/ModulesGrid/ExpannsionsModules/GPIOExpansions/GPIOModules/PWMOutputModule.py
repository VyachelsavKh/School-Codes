import tkinter as tk
from tkinter import ttk
from typing import Tuple, Callable, Any, List

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
from CustomElements.Element import Element
from BaseModule import *
from Enums import *

class PWMOutputModule(BaseModule):
    @staticmethod
    def get_name():
        return "PWM output"

    def __init__(self, root : tk.Misc, usage_root : tk.Misc, pins : SelectorValues = common_pins):
        super().__init__(root, usage_root, pins)

        self.__discrete_value : int = 0

        self.__colors = ["red", "green"]

        self._canvas = tk.Canvas(self._usage_root)
        self._button_canvas = Element(self._canvas)
        self._button = self._canvas.create_rectangle(0, 0, 10, 10, outline="black", width=10)
        self._canvas.tag_bind(self._button, "<Button-1>", self._toggle_click)

        self._slider_height = 20
        self._slider = Element(ttk.Scale(self._usage_root, from_=0, to=100, orient=tk.HORIZONTAL, command=self._slider_change), height=self._slider_height)

        self._paint_button()

    def _send_duty(self, value : int):
        print(value)

    def _send_value(self, value : int):
        print(value)

    def _slider_change(self, value):
        value = int(float(value))
        self._send_duty(value)

    def _paint_button(self):
        self._canvas.itemconfig(self._button, fill = self.__colors[self.__discrete_value])

    def _toggle_click(self, event):
        self.__discrete_value += 1
        self.__discrete_value %= 2

        self._paint_button()

        self._send_value(self.__discrete_value)

    def set_usage_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        button_height = height - self._slider_height - self._elemnts_margin
        _, h = self._button_canvas.set_coordinates(x, y, width, button_height)
        self._canvas.coords(self._button, 0, 0, width, button_height)
        self._slider.set_coordinates(0, h + self._elemnts_margin, width)

    def _place_usage(self):
        self._button_canvas.place()
        self._slider.place()

    def _forget_usage(self):
        self._button_canvas.place_forget()
        self._slider.place_forget()

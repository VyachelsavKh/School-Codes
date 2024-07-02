import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from typing import Tuple

def get_str_sizes(text: str, font: Tuple[str, int]) -> Tuple[int, int]:
    label = ttk.Label(text=text, font=font)
    
    return label.winfo_reqwidth(), label.winfo_reqheight()

class CoordinatesUsager:
    def __init__(self, width : int = None, height : int = None):
        self._last_x = 0
        self._last_y = 0

        self._height = height
        self._width = width

    def set_coordinates(self, x : int = 0, y : int = 0, width : int = None, height : int = None) -> Tuple[int, int]:
        self._last_x = x
        self._last_y = y

        if (width is not None):
            self._width = width

        if (height is not None):
            self._height = height

        w, h = self.get_sizes()

        return x + w, y + h
    
    def set_sizes(self, width : int = None, height : int = None):
        if (width is not None):
            self._width = width

        if (height is not None):
            self._height = height

    def get_coordinates(self):
        return self._last_x, self._last_y

    def get_sizes(self):
        return self._width, self._height
    
    def place(self):
        pass

    def place_forget(self):
        pass

class Element(CoordinatesUsager):
    def __init__(self, element : tk.Widget, width: int = None, height: int = None):
        self._element = element

        width = width if width is not None else self._element.winfo_reqwidth()
        height = height if height is not None else self._element.winfo_reqheight()
        
        super().__init__(width, height)

    def get_element(self):
        return self._element

    def place(self):
        self._element.place(x=self._last_x, y=self._last_y, width=self._width, height=self._height)

    def place_forget(self):
        self._element.place_forget()

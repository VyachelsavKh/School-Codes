import tkinter as tk
from tkinter import ttk
from typing import Tuple, Callable, Any

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from CustomElements.Element import Element

class LabelEntry(Element):
    def __init__(self, root : tk.Misc, text, entry_max_len : int = 15, entry_start_text : str = "", height = 20, font = ("Arial", 10)):
        self.__root = root
        self.__entry_max_len = entry_max_len

        self.__font = font
        self.__text = text
        self.__container = ttk.Frame(self.__root)
        super().__init__(self.__container, height=height)
        
        self.__elements_margin = 5

        self.__create_elements()
        
        self.update_entry(entry_start_text)

    def __create_elements(self):
        self.__label = Element(ttk.Label(self.__container, text=self.__text, anchor=tk.CENTER, font=self.__font), height=self._height)

        self.__text_var = tk.StringVar()
        self.__text_var.trace_add('write', self.__limit_size)
        self.__entry = Element(ttk.Entry(self.__container, textvariable=self.__text_var), height=self._height)

        x, _ = self.__label.set_coordinates()
        self.__label_width = x
        x, _ = self.__entry.set_coordinates(x + self.__elements_margin)

    def __limit_size(self, *args):
        value = self.__text_var.get()
        if len(value) > self.__entry_max_len:
            self.__text_var.set(value[:self.__entry_max_len])

    def get_entry(self) -> str:
        return self.__text_var.get()

    def update_entry(self, text : str):
        text = text[:self.__entry_max_len]
        self.__text_var.set(text)

    def set_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        w, h = super().set_coordinates(x, y, width, height)

        x, y = self.__label.set_coordinates(height=height)
        self.__entry.set_coordinates(x + self.__elements_margin, width=width - x - self.__elements_margin)

        return w, h

    def place(self) -> None:
        super().place()
        self.__label.place()
        self.__entry.place()

if __name__ == "__main__":
    root = tk.Tk()
    app = LabelEntry(root, "Name:", 10, "01234567890123")
    app.set_coordinates(10, 10, 200)
    app.place()
    root.mainloop()
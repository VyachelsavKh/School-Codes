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

class GPIOModule(Element):
    def __init__(self, root : tk.Misc):
        self.__root = root

        self.__container = ttk.Frame(self.__root)
        super().__init__(self.__container)

    def _pin_changed(self, pin : str):
        print(pin)

    def set_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        self.__pin_selector.set_coordinates(width=width)

        return super().set_coordinates(x, y, width, height)
    
    def set_usage_coordinates(self, x: int = 0, y: int = 0, width: int = None, height: int = None) -> Tuple[int]:
        pass

    def place(self):
        super().place()


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from enum import Enum, auto
import math
import time
from typing import Tuple, Callable, Any, List

from Enums import SchemeState
from TopPanel.TopPannel import TopPannel
from ModulesGrid.ModulesGrid import ModulesGrid
from CustomElements.Element import Element
from InitializeConstans import *

class MainWindow:
    def __init__(self, root: tk.Tk):
        self.__root = root
        self.__root.title("SCADA")
        self.__root.state('normal')
        
        self.last_width = 0
        self.last_height = 0

        self.__root.bind('<Configure>', self.__on_resize)

        self.__top_pannel = TopPannel(self.__root, self.__scheme_changed, self.__save, self.__open, self.__clear, self.__size_changed)
        self.__modules_grid = ModulesGrid(self.__root, start_rows_count, start_cols_count)

        self.__top_margin = 8
        self.__bottom_margin = 8
        self.__left_margin = 8
        self.__right_margin = 8
        self.__elements_margin = 8

        self.__minsize()

        _, y = self.__top_pannel.set_coordinates(self.__left_margin, self.__top_margin)
        self.__modules_grid.set_coordinates(self.__left_margin, y + self.__elements_margin)
        
        self.__top_pannel.place()
        self.__modules_grid.place()

    def __get_grid_sizes(self) -> Tuple[int, int]:
        width = self.__root.winfo_width()
        height = self.__root.winfo_height()

        h = top_pannel_height

        width -= self.__left_margin + self.__right_margin
        height -= self.__top_margin + h + self.__elements_margin + self.__bottom_margin

        return width, height

    def __on_resize(self, event):
        new_width = self.__root.winfo_width()
        new_height = self.__root.winfo_height()
        
        if new_width != self.last_width or new_height != self.last_height:
            self.last_width = new_width
            self.last_height = new_height
            
            w, h = self.__get_grid_sizes()
            self.__modules_grid.resize(w, h)

    def __minsize(self):
        width, height = self.__top_pannel.get_sizes()
        mgw, mgh = self.__modules_grid.get_min_sizes()

        width = max(width, mgw)
        width += self.__left_margin + self.__right_margin
        height += self.__top_margin + self.__elements_margin + mgh + self.__bottom_margin

        self.__root.minsize(width, height)

    def __scheme_changed(self, state : SchemeState):
        self.__minsize()
        self.__modules_grid.change_state(state)

    def __save(self, path : str):
        print(path)

    def __open(self, path : str):
        print(path)

    def __clear(self):
        print("Clear")

    def __size_changed(self, rows : int, cols : int):
        self.__modules_grid.resize_grid(rows, cols)
        self.__minsize()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
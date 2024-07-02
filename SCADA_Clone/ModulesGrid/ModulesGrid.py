import tkinter as tk
from typing import Tuple, Any, List

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from InitializeConstans import *
from Module import Module
from Enums import SchemeState

class ModulesGrid:
    def __init__(self, root : tk.Misc, rows : int = 1, cols : int = 1):
        self.__root = root

        self.__modules : List[List[Module]] 
        self.__create_grid(rows, cols)

        self.__state = SchemeState.USAGE

        self.__last_x = 0
        self.__last_y = 0
        self.__width = -1
        self.__height = -1

        self.__modules_x_margin = 8
        self.__modules_y_margin = 8
    
    def __create_grid(self, rows : int, cols : int) -> List[List[Module]]:
        modules : List[List[Module]] = []

        for i in range(rows):
            row : List[Module] = []
            for j in range(cols):
                row.append(Module(self.__root))
            modules.append(row)

        self.__rows_count = rows
        self.__cols_count = cols
        self.__modules = modules
    
    def resize_grid(self, rows : int, cols : int):
        new_modules : List[List[Module]] = []

        for i in range(rows):
            row : List[Module] = []
            for j in range(cols):
                if i < self.__rows_count and j < self.__cols_count:
                    row.append(self.__modules[i][j])
                else:
                    new_module = Module(self.__root)
                    new_module.change_state(self.__state)
                    row.append(new_module)
            new_modules.append(row)

        for i in range(self.__rows_count):
            for j in range(self.__cols_count):
                if i >= rows or j >= cols:
                    self.__modules[i][j].clear()
        
        self.__rows_count = rows
        self.__cols_count = cols
        self.__modules = new_modules

        self.__resize()
        self.place()
 
    def __resize(self):
        x = self.__last_x
        y = self.__last_y

        modules_width = int((self.__width - (self.__cols_count - 1) * self.__modules_x_margin) / self.__cols_count)
        modules_height = int((self.__height - (self.__rows_count - 1) * self.__modules_y_margin) / self.__rows_count)

        for i in range(self.__rows_count):
            x = self.__last_x
            new_y = 0
            for j in range(self.__cols_count):
                x, new_y = self.__modules[i][j].set_coordinates(x, y, modules_width, modules_height)
                x += self.__modules_x_margin
            y = new_y + self.__modules_y_margin

        return self.__last_x + self.__width, self.__last_y + self.__height

    def min_height(self):
        return self.__rows_count * (Module.min_height() + self.__modules_y_margin) - self.__modules_y_margin
    def min_width(self):
        return self.__cols_count * (Module.min_width() + self.__modules_x_margin) - self.__modules_x_margin
    
    def get_min_sizes(self) -> Tuple[int, int]:
        return self.min_width(), self.min_height()

    def set_coordinates(self, x : int, y : int) -> Tuple[int, int]:
        self.__last_x = x
        self.__last_y = y
    
    def resize(self, width : int, height : int):
        self.__width = width
        self.__height = height

        self.__resize()
        self.place()

    def change_state(self, state : SchemeState):
        self.__state = state

        for i in range(self.__rows_count):
            for j in range(self.__cols_count):
                self.__modules[i][j].change_state(state)

    def get_coordinates(self) -> Tuple[int, int]:
        return self.__last_x, self.__last_y

    def get_sizes(self) -> Tuple[int, int]:
        return self.__width, self.__height

    def place(self):
        for i in range(self.__rows_count):
            for j in range(self.__cols_count):
                self.__modules[i][j].place()
    
    def place_forget(self) -> None:
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ModulesGrid(root, 2, 3)
    app.set_coordinates(10, 10)
    app.resize(800, 600)
    app.place()
    root.after(1000, lambda : app.change_state(SchemeState.SETTINGS))
    root.after(10000, lambda : app.resize_grid(3, 4))
    root.mainloop()
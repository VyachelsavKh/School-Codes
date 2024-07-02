import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Tuple, Callable, Any

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from InitializeConstans import *
from Enums import SchemeState
from CustomElements.Element import Element
from CustomElements.PlusMinusLabel import PlusMinusLabel

class TopPannel(Element):
    def __init__(self, root : tk.Misc, 
                scheme_changed_handler : Callable[[SchemeState], Any], 
                save_hadler : Callable[[str], Any], 
                open_hadler : Callable[[str], Any], 
                clear_handler : Callable[[Any], Any],
                size_changed_hadler : Callable[[int, int], Any]):
        
        self.__root = root
        self.__scheme_changed_handler = scheme_changed_handler
        self.__save_hadler = save_hadler
        self.__open_handler = open_hadler
        self.__clear_handler = clear_handler
        self.__size_changed_hadler = size_changed_hadler

        self.__container = ttk.Frame(self.__root)
        super().__init__(self.__container, height=top_pannel_height)

        self.__rows_count = start_rows_count
        self.__cols_count = start_cols_count

        self.__elements_margin = 5

        self.__create_elements()
    
    def __create_elements(self):
        self.__state_var = tk.IntVar(value=0)
        self.__scheme_mode = Element(ttk.Checkbutton(self.__container, text="Change scheme", variable=self.__state_var, command=self.__scheme_changed),
                                        110, self._height)
        self.__save_button = Element(ttk.Button(self.__container, text="Save", command=self.__save_pressed),
                                        40, self._height)
        self.__open_button = Element(ttk.Button(self.__container, text="Open", command=self.__open_pressed),
                                        40, self._height)
        self.__clear_button = Element(ttk.Button(self.__container, text="Clear", command=self.__clear_handler),
                                        40, self._height)
        self.__rows_label = PlusMinusLabel(self.__container, "Rows: ", min_rows_count, max_rows_count, start_rows_count, self.__rows_changed, self._height)
        self.__cols_label = PlusMinusLabel(self.__container, "Cols: ", min_cols_count, max_cols_count, start_cols_count, self.__cols_changed, self._height)

        x, _ = self.__scheme_mode.set_coordinates()
        self.__usage_width = x
        x, _ = self.__save_button.set_coordinates(x + self.__elements_margin)
        x, _ = self.__open_button.set_coordinates(x + self.__elements_margin)
        x, _ = self.__clear_button.set_coordinates(x + self.__elements_margin)
        x, _ = self.__rows_label.set_coordinates(x + self.__elements_margin)
        x, _ = self.__cols_label.set_coordinates(x + self.__elements_margin)
        self.__settings_width = x

        self.set_sizes(x)

    def __save_pressed(self):
        self.__container.focus()
        file_path = filedialog.asksaveasfilename(defaultextension=".scd", filetypes=[("Scheme files", "*.scd"), ("All files", "*.*")])
        self.__save_hadler(file_path)

    def __open_pressed(self):
        self.__container.focus()
        file_path = filedialog.askopenfilename(defaultextension=".scd", filetypes=[("Scheme files", "*.scd"), ("All files", "*.*")])
        self.__open_handler(file_path)

    def __rows_changed(self, val : int):
        self.__rows_count = val
        self.__size_changed_hadler(self.__rows_count, self.__cols_count)
        
    def __cols_changed(self, val : int):
        self.__cols_count = val
        self.__size_changed_hadler(self.__rows_count, self.__cols_count)
    
    def __scheme_changed(self):
        self.__container.focus()
        state = SchemeState(self.__state_var.get())

        if state == SchemeState.SETTINGS:
            self.__place_settings()
        elif state == SchemeState.USAGE:
            self.__forget_settings()

        self.__scheme_changed_handler(state)

    def __place_settings(self):
        self.__save_button.place()
        self.__open_button.place()
        self.__clear_button.place()
        self.__rows_label.place()
        self.__cols_label.place()

    def __forget_settings(self):
        self.__save_button.place_forget()
        self.__open_button.place_forget()
        self.__clear_button.place_forget()
        self.__rows_label.place_forget()
        self.__cols_label.place_forget()

    def get_grid_sizes(self) -> Tuple[int, int]:
        return self.__rows_count, self.__cols_count

    def place(self):
        super().place()
        self.__scheme_mode.place()

    def get_sizes(self) -> Tuple[int, int]:
        w = 0
        state = SchemeState(self.__state_var.get())
        if state == SchemeState.USAGE:
            w = self.__usage_width
        elif state == SchemeState.SETTINGS:
            w = self.__settings_width
        return w, self._height

def f1(val):
    print(val)

def f2(val):
    print(val)

def f3(val):
    print(val)

def f4():
    print("Clear")

def f5(val1, val2):
    print(str(val1) + " " + str(val2))

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(width=600, height=200)
    app = TopPannel(root, f1, f2, f3, f4, f5)
    app.set_coordinates(10, 20)
    app.place()
    root.mainloop()
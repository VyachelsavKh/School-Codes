import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from IUpdatingSelector import IUpdatingSelector
from typing import List

class SelectorValues:
    def __init__(self, values : List[str], use_empty : bool = False):
        self.__start_values = values
        self.__values = values
        self.__selectors : List[IUpdatingSelector] = []

    def add_selector(self, selector : IUpdatingSelector):
        self.__selectors.append(selector)

    def remove_selector(self, selector : IUpdatingSelector):
        self.__selectors.remove(selector)

    def get_start_values(self):
        return ["Empty"] + self.__start_values
    
    def get_values(self):
        return ["Empty"]  + self.__values

    def update_selectors(self):
        for selector in self.__selectors:
            selector.update_values(self.get_values())

    def __sort(self):
        self.__values = sorted(self.__values, key=lambda x: (len(x), x))

    def add_value(self, value : str):
        if value == "Empty" or value == "":
            return
        
        self.__values.append(value)
        self.__sort()
        self.update_selectors()

    def remove_value(self, value : str):
        if value == "Empty" or value == "":
            return
        
        self.__values.remove(value)
        self.update_selectors()

    def swap_value(self, prev_value : str, new_value : str):
        if not (prev_value == "Empty" or prev_value == ""):
            self.__values.append(prev_value)

        if not (new_value == "Empty" or new_value == ""):
            self.__values.remove(new_value)

        self.__sort()
        self.update_selectors()

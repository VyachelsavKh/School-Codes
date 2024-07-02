import tkinter as tk
from typing import Tuple, Callable, Any, List, Type

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GPIOModules.GPIOModules import *
from GPIOExpansion import GPIOExpansion
from GPIOModules.RaspberryModules.RaspberryModules import *

class RaspberryExpansion(GPIOExpansion):
    @staticmethod
    def get_name():
        return "Raspberry"
    
    def __init__(self, root: tk.Misc, usage_root : tk.Misc):
        super().__init__(root, usage_root)

    def _set_GPIO_modules(self):
        self._gpio_modules : List [Type[BaseModule]] = [
            RaspberryDiscreteOutput, 
            RaspberryPWMOutput]
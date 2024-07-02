import sys
import os
from tkinter import Misc

from SCADA_Clone.ModulesGrid.ExpannsionsModules.GPIOExpansions.GPIOModules.BaseModule import common_pins
from raspberry_pins import raspberry_pins
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from GPIOModules.GPIOModules import *

class RaspberryDiscreteOutput(DiscreteOutputModule):
    def __init__(self, root: Misc, usage_root: Misc):
        super().__init__(root, usage_root, raspberry_pins)

    def _attach_pin(self, pin: str):
        print("RaspberryDiscreteOutput _attach_pin " + pin)
    def _detach_pin(self):
        print("RaspberryDiscreteOutput _detach_pin")
    def _send_value(self, value: int):
        print("RaspberryDiscreteOutput _send_value " + str(value))

class RaspberryPWMOutput(PWMOutputModule):
    def __init__(self, root: Misc, usage_root: Misc):
        super().__init__(root, usage_root, raspberry_pins)

    def _attach_pin(self, pin: str):
        print("RaspberryPWMOutput _attach_pin " + pin)
    def _detach_pin(self):
        print("RaspberryPWMOutput _detach_pin")
    def _send_value(self, value: int):
        print("RaspberryPWMOutput _send_value " + str(value))
    def _send_duty(self, value : int):
        print("RaspberryPWMOutput _send_duty " + str(value))
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Selectors.SelectorValues import SelectorValues

raspberry_pins = SelectorValues(["GPIO0", "GPIO1", "GPIO4", "GPIO17", "GPIO18", "GPIO22", "GPIO23", "GPIO27"], True)
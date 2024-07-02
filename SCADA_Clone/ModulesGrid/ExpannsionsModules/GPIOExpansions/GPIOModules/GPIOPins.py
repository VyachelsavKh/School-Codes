import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Selectors.SelectorValues import SelectorValues
from Selectors.UpdatingSelector import UpdatingSelector

common_pins = SelectorValues(["GPIO0", "GPIO1"], True)

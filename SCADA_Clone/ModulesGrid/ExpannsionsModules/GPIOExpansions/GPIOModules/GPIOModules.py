from typing import Tuple, Callable, Any, List
from enum import Enum

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from BaseModule import BaseModule
from DiscreteOutputModule import DiscreteOutputModule
from PWMOutputModule import PWMOutputModule
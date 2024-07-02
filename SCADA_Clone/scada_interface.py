import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from enum import Enum, auto
import math
import time

from MainWindow import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk
import tkinter.font as font

# Создаем главное окно
root = tk.Tk()

font = ("Arial", 12)

label = ttk.Label(None, text="", font=font, background="grey")

def count_width(text : str):
    label.config(text=text)
    return text, label.winfo_reqwidth()

list = []

list.append(count_width("-"))
list.append(count_width("@"))
list.append(count_width(":"))

for i in range(0, 10):
    list.append(count_width(str(i)))

for i in range(ord('a'), ord('z') + 1):
    list.append(count_width(chr(i)))

for i in range(ord('A'), ord('Z') + 1):
    list.append(count_width(chr(i)))

list = sorted(list, key=lambda x: x[1])

print(list)

# Запускаем главный цикл приложения
root.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from enum import Enum, auto
import math
import time

class GPIO:
    def cleanup():
        pass

class GpioMode(Enum):
    OUTPUT = auto()
    INPUT = auto()
    PWM = auto()
    SERVO = auto()

class RaspberryPiGPIO:
    used_pins = set()
    def __init__(self, pin, mode, frequency=50):
        pass

    def write(self, value):
        pass
       
    def change_duty(self, duty):
        pass

    def read(self):
       pass

    def servo_angle_to_duty(self, angle):
        return (angle/20)+2

    def cleanup(self):
        pass

class ModuleState(Enum):
    SETTING = 0
    USAGE = 1

class BaseModule:
    gpio_pins = ["GPIO0", "GPIO1", "GPIO4", "GPIO17", "GPIO18", "GPIO22", "GPIO23", "GPIO27"]
    gpio_bmc_pins = [0, 1, 4 ,17, 18, 22, 23, 27]
    analog_pins = ["A0", "A1", "A2", "A3"]

    def __init__(self, root):
        self.root = root
        self.pin = 0
        self.gpio = None
         
        self.pin_choose = ttk.Combobox(self.root, values=BaseModule.gpio_pins, state="readonly")
        self.pin_choose.current(0)
        self.pin_choose.bind("<<ComboboxSelected>>", self.pin_changed)

    def pin_changed(self, event):
        self.root.focus_set()
        self.pin = self.pin_choose.current()
        self.root.focus_set()

    def place_settings(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        self.forget_usage()
        self.pin_choose.place(x = left_margin, y = top_margin, width=width - left_margin - right_margin, height=20)

    def forget_settings(self):
        self.pin_choose.place_forget()

    def place_usage(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        pass

    def forget_usage(self):
        pass

    def place(self, width, height, top_margin, left_margin, right_margin, bottom_margin, state):
        if state == ModuleState.SETTING:
            self.forget_usage()
            self.place_settings(width, height, top_margin, left_margin, right_margin, bottom_margin)
        else:
            self.forget_settings()
            self.place_usage(width, height, top_margin, left_margin, right_margin, bottom_margin)

    def place_forget(self):
        self.forget_settings()
        self.forget_usage()
    
    def save_settings(self):
        settings_array = bytearray()

        settings_array.append(self.pin)

        return settings_array
    
    def read_settings(self, settings_array, start_pos):
        self.pin = settings_array[start_pos]
        
        self.pin_choose.set(self.gpio_pins[self.pin])

        return start_pos + 1

class EmptyModule(BaseModule):
    def __init__(self):
        super().__init__(None)
    
    def place(self, *args, **kargs):
        pass

class DiscreteOutputModule(BaseModule):
    def __init__(self, root):
        super().__init__(root)
        
        self.disc_output = 0
        self.gpio = None
        self.colors = ["red", "green"]

        self.button_frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=3)
        self.button_frame.pack_propagate(False)

        self.toggle_button = tk.Button(self.button_frame, bg="red", command=self.toggle, bd=0)
        self.toggle_button.pack(fill=tk.BOTH, expand=True)  # Заполняем кнопкой весь фрейм

    def forget_usage(self):
        self.disc_output = 0
        self.toggle_button.place_forget()
        self.button_frame.place_forget()
        if self.gpio is not None:
            self.gpio.cleanup()

    def apply_value(self):
        self.gpio.write(self.disc_output)
        self.toggle_button.config(bg=self.colors[self.disc_output])

    def place_usage(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        self.toggle_button.pack()
        self.button_frame.place(x = left_margin, y = top_margin, width=width - left_margin - right_margin, height=height - top_margin - bottom_margin)
        self.gpio = RaspberryPiGPIO(self.gpio_bmc_pins[self.pin], GpioMode.OUTPUT)
        self.apply_value()

    def toggle(self):
        self.disc_output += 1 
        self.disc_output %= 2 
        self.apply_value()

class PwmOutputModule(DiscreteOutputModule):
    def __init__(self, root):
        super().__init__(root)
        self.slider = ttk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.on_slider_change)
        self.duty = 0

    def place_usage(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        super().place_usage(width, height, top_margin, left_margin, right_margin, bottom_margin + 20 + 5)
        self.slider.place(x=left_margin, y=height - bottom_margin - 20, height=20, width=width - left_margin - right_margin)
        self.gpio.cleanup()
        self.gpio = RaspberryPiGPIO(self.gpio_bmc_pins[self.pin], GpioMode.PWM, frequency=50)
        
    def forget_usage(self):
        super().forget_usage()
        self.slider.place_forget()
        self.slider.set(0)
        self.duty = 0

    def on_slider_change(self, value):
        self.duty = int(float(value))
        if self.gpio is not None:
            self.gpio.change_duty(self.duty)

class DiscreteInputModule(BaseModule):
    class DiscreteMode(Enum):
        CURRENT = 0
        TAP_CHANGE = 1
        TAP_AND_WAIT_CHANGE = 2
        DOUBLE_TAP_CHANGE = 3
        
    poll_speed = 100

    def __init__(self, root):
        super().__init__(root)
        
        self.mode = self.DiscreteMode.CURRENT

        self.current_value = 0
        self.poll_pin = 0

        self.mode_select = ttk.Combobox(self.root, values=["Current value", "Tap change", "Tap and wait change", "Double tap change"], state="readonly")
        self.mode_select.current(int(self.mode.value))
        self.mode_select.bind("<<ComboboxSelected>>", self.mode_changedd)

        self.canvas = tk.Canvas(root)
        self.rectangle = None

    def get_color(self):
        return "green" if self.current_value else "red"

    def update_value(self):
        if self.poll_pin:
            self.current_value = self.gpio.read()

            self.canvas.itemconfig(self.rectangle, fill=self.get_color())
            self.root.after(self.poll_speed, self.update_value)

    def place_usage(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        super().place_usage(width, height, top_margin, left_margin, right_margin, bottom_margin)

        if self.rectangle is not None:
            self.canvas.delete(self.rectangle)

        self.canvas.place(x = left_margin, y=top_margin, width=width-left_margin-right_margin,height=height-top_margin-bottom_margin)
        initial_coords = 0, 0, width - left_margin - right_margin, height - bottom_margin - top_margin
        self.rectangle = self.canvas.create_rectangle(
            initial_coords,
            outline="black",  # Цвет границы
            fill=self.get_color(),     # Цвет заливки
            width=10           # Толщина границы
        )
        
        self.poll_pin = 1
        self.gpio = RaspberryPiGPIO(self.gpio_bmc_pins[self.pin], GpioMode.INPUT)
        self.update_value()
    
    def forget_usage(self):
        super().forget_usage()
        self.canvas.place_forget()

        self.poll_pin = 0
        if self.gpio is not None:
            self.gpio.cleanup()

    def place_settings(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        super().place_settings(width, height, top_margin, left_margin, right_margin, bottom_margin)
        #self.mode_select.place(x = left_margin, y = top_margin + 20 + 8, width=width - left_margin - right_margin, height=20)

    def forget_settings(self):
        super().forget_settings()
        self.mode_select.place_forget()

    def mode_changedd(self, event):
        self.root.focus_set()
        self.mode = self.DiscreteMode(self.mode_select.current())
        self.root.focus_set()

class AnalogInput(BaseModule):
    poll_speed = 100
    
    def __init__(self, root):
        super().__init__(root)

        self.current_value = 143
        self.value_factor = 1
        self.unit = "Graduses"

        self.poll_pin = 0

        self.factor_label = ttk.Label(self.root, text="Mul:", anchor=tk.W)
        self.factor_var = ttk.Entry(self.root)
        self.factor_var.insert(0, str(self.value_factor))
        self.factor_var.bind("<KeyRelease>", self.factor_changed)
        self.unit_label = ttk.Label(self.root, text="Units:", anchor=tk.W)
        self.unit_var = ttk.Entry(self.root)
        self.unit_var.insert(0, self.unit)
        self.unit_var.bind("<KeyRelease>", self.units_changed)

        self.output_value_frame = tk.Frame(self.root, bd=0, highlightbackground="black", highlightthickness=0)
        self.output_value_frame.pack_propagate(False)

        self.output_units_frame = tk.Frame(self.root, bd=0, highlightbackground="black", highlightthickness=0)
        self.output_units_frame.pack_propagate(False)

        self.output_value = ttk.Label(self.output_value_frame, text=str(self.current_value), anchor=tk.S)
        self.output_units = ttk.Label(self.output_units_frame, text=self.unit, anchor=tk.N)

        self.output_value.pack(fill="both", expand=True)
        self.output_units.pack(fill="both", expand=True)

    def update_value(self):
        if self.poll_pin:
            self.current_value = self.current_value % 200 + 8

            self.output_value.config(text=str(self.current_value))
            self.root.after(self.poll_speed, self.update_value)

    def place_usage(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        super().place_usage(width, height, top_margin, left_margin, right_margin, bottom_margin)
        
        remain_width = width - left_margin - right_margin
        remain_height = (height - top_margin - bottom_margin - 8) / 2
        
        self.output_value_frame.place(x=left_margin, y=top_margin, width=remain_width, height=remain_height)
        self.output_units_frame.place(x=left_margin, y=top_margin + remain_height + 8, width=remain_width, height=remain_height)

        value_size = remain_width / len(str(self.current_value)) 
        unit_size = remain_width / len(self.unit)
        cur_size = min(value_size, unit_size)

        cur_size = min(cur_size * 1.3, remain_height * 0.7)
        
        self.output_value.config(font=("Arial", int(cur_size)), text=str(self.current_value))
        self.output_units.config(font=("Arial", int(cur_size)), text=self.unit)

        self.poll_pin = 1
        self.update_value()

    def forget_usage(self):
        super().forget_usage()

        self.output_value_frame.place_forget()
        self.output_units_frame.place_forget()

        self.poll_pin = 0

    def place_settings(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        super().place_settings(width, height, top_margin, left_margin, right_margin, bottom_margin)
       
        self.factor_label.place(x = left_margin, y = top_margin + 20 + 8, width=30, height=20)
        self.factor_var.place(x = left_margin + 30 + 5, y = top_margin + 20 + 8, width=width - left_margin - right_margin - 30 - 5, height=20)
        
        self.unit_label.place(x = left_margin, y = top_margin + 20 + 8 + 20 + 8, width=40, height=20)
        self.unit_var.place(x = left_margin + 40 + 5, y = top_margin + 20 + 8 + 20 + 8, width=width - left_margin - right_margin - 40 - 5, height=20)

    def forget_settings(self):
        super().forget_settings()

        self.factor_label.place_forget()
        self.factor_var.place_forget()

        self.unit_label.place_forget()
        self.unit_var.place_forget()

    def factor_changed(self, event):
        self.value_factor = float(self.factor_var.get())

    def units_changed(self, event):
        self.unit = self.unit_var.get()

class ServoOutput(BaseModule):
    def __init__(self, root):
        super().__init__(root)

        self.current_angle = 90
        self.min_angle = 0
        self.max_angle = 180
        self.gpio = None
        
        self.min_angle_label = ttk.Label(self.root, text="Min angle:", anchor=tk.W)
        self.min_angle_entry = ttk.Entry(self.root)
        self.min_angle_entry.insert(0, str(self.min_angle))
        self.min_angle_entry.bind("<KeyRelease>", self.min_angle_change)

        self.max_angle_label = ttk.Label(self.root, text="Max angle:", anchor=tk.W)
        self.max_angle_entry = ttk.Entry(self.root)
        self.max_angle_entry.insert(0, str(self.max_angle))
        self.max_angle_entry.bind("<KeyRelease>", self.max_angle_change)

        self.canvas = tk.Canvas(self.root)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.arc = None
        self.radius_line = None
        self.slider = ttk.Scale(self.root, from_=0, to=180, orient=tk.HORIZONTAL, command=self.on_slider_change)

    def place_settings(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        super().place_settings(width, height, top_margin, left_margin, right_margin, bottom_margin)
        
        self.min_angle_label.place(x = left_margin, y = top_margin + 20 + 8, width=65, height=20)
        self.min_angle_entry.place(x = left_margin + 65 + 5, y = top_margin + 20 + 8, width=width - left_margin - right_margin - 65 - 5, height=20)
        
        self.max_angle_label.place(x = left_margin, y = top_margin + 20 + 8 + 20 + 8, width=65, height=20)
        self.max_angle_entry.place(x = left_margin + 65 + 5, y = top_margin + 20 + 8 + 20 + 8, width=width - left_margin - right_margin - 65 - 5, height=20)

        
    def forget_settings(self):
        super().forget_settings()

        self.min_angle_label.place_forget()
        self.min_angle_entry.place_forget()

        self.max_angle_label.place_forget()
        self.max_angle_entry.place_forget()

    def place_arc(self):
        if self.arc is not None:
            self.canvas.delete(self.arc)

        remain_width = self.width-self.left_margin-self.right_margin
        remain_height = self.height-self.top_margin-self.bottom_margin-20-8-8

        canvas_height = min(remain_width / 2, remain_height)
        self.canvas_height = canvas_height
        canvas_x_pos = self.left_margin + (remain_width - canvas_height * 2) / 2
        self.canvas.place(x=canvas_x_pos, y=self.top_margin, width=canvas_height * 2, height=canvas_height)
        self.arc_x_center = (5 + canvas_height * 2 - 5) / 2
        self.arc_y_center = (5 + canvas_height * 2 - 5 - 15) / 2

        self.arc_x_radius = (canvas_height * 2 - 5 - 5) / 2
        self.arc_y_radius = (canvas_height * 2 - 5 - 15 - 5) / 2

        self.arc = self.canvas.create_arc(5, 5, canvas_height * 2 - 5, canvas_height * 2 - 5 - 15, fill='lightblue', outline='blue', start=180 - self.max_angle, extent=self.max_angle - self.min_angle)
    
    def calculate_radius(self, angle):
        factor = abs(angle - 90) / 90

        return self.arc_x_radius * factor + self.arc_y_radius * (1 - factor)

    def place_radius(self):
        if self.radius_line is not None:
            self.canvas.delete(self.radius_line)

        radius = self.calculate_radius(self.current_angle)
        
        x1 = self.arc_x_center
        y1 = self.arc_y_center

        x2 = x1 - radius * math.cos(self.current_angle / 180 * math.pi)
        y2 = y1 - radius * math.sin(self.current_angle / 180 * math.pi)

        self.radius_line = self.canvas.create_line(x1, y1, x2, y2, width=3, fill="red")
        self.gpio.write(self.current_angle)
    
    def use_mouse(self, x, y):        
        dx = self.arc_x_center - x
        dy = self.arc_y_center - y

        new_angle = 0

        if dx == 0:
            if dy > 0:
                new_angle = 90
            else:
                new_angle = -90
        else:
            new_angle = math.atan(dy / dx) / math.pi * 180
            
            if dx < 0:
                if dy > 0:
                    new_angle += 180
                else:
                    new_angle -= 180

        if (new_angle >= 0):
            x1 = self.arc_x_center
            y1 = self.arc_y_center

            max_radius = self.calculate_radius(new_angle) * 1.05

            cur_radius = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)

            if (cur_radius <= max_radius):
                self.current_angle = new_angle
                self.slider.set(new_angle)
                self.place_radius()
    
    def on_mouse_drag(self, event):
        x = event.x
        y = event.y

        self.use_mouse(x, y)

    def on_mouse_click(self, event):
        x = event.x
        y = event.y

        self.use_mouse(x, y)

    def place_usage(self, width, height, top_margin, left_margin, right_margin, bottom_margin):
        super().place_usage(width, height, top_margin, left_margin, right_margin, bottom_margin)
        self.gpio = RaspberryPiGPIO(self.gpio_bmc_pins[self.pin], GpioMode.SERVO)
        
        self.width = width
        self.height = height
        self.top_margin = top_margin
        self.left_margin = left_margin
        self.right_margin = right_margin
        self.bottom_margin = bottom_margin

        self.place_arc()
        self.slider.set(self.current_angle)
        self.slider.place(x=left_margin, y=top_margin + self.canvas_height + 8, height=20, width=width-left_margin-right_margin)
        
    def forget_usage(self):
        super().forget_usage()
        self.slider.place_forget()
        self.canvas.place_forget()
        if self.gpio is not None:
            self.gpio.cleanup()

    def min_angle_change(self, event):
        self.min_angle = int(self.min_angle_entry.get())
        self.slider.configure(from_ = self.min_angle)
        self.current_angle = (self.min_angle + self.max_angle) / 2

    def max_angle_change(self, event):
        self.max_angle = int(self.max_angle_entry.get())
        self.slider.configure(to = self.max_angle)
        self.current_angle = (self.min_angle + self.max_angle) / 2

    def on_slider_change(self, value):
        self.current_angle = float(value)
        self.place_radius()

    def save_settings(self):
        super_settings = super().save_settings()

        self_settings = bytearray()
        self_settings += super_settings

        self_settings.append(self.min_angle)
        self_settings.append(self.max_angle)

        return self_settings
    
    def read_settings(self, settings_array, start_pos):
        after_pos = super().read_settings(settings_array, start_pos)

        self.min_angle = settings_array[after_pos]
        self.max_angle = settings_array[after_pos + 1]

        self.min_angle_entry.delete(0, tk.END)
        self.max_angle_entry.delete(0, tk.END)
        self.min_angle_entry.insert(0, str(self.min_angle))
        self.max_angle_entry.insert(0, str(self.max_angle))

        self.slider.configure(from_ = self.min_angle, to = self.max_angle)
        self.current_angle = (self.min_angle + self.max_angle) / 2

        return after_pos + 2

class Module:
    top_margin = 8
    bottom_margin = 12
    left_margin = 8
    right_margin = 12
    config_margin = 8

    class ModuleMode(Enum):
        EMPTY = 0
        DISCRETE_OUTPUT = 1
        PWM_OUTPUT = 2
        DISCRETE_INPUT = 3
        SERVO_OUTPUT = 4

    def __init__(self, root, x_pos, y_pos):
        self.root = root
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.container = None
        self.state = ModuleState.USAGE
        self.mode = self.ModuleMode.EMPTY
        self.name = "Module"
        self.modules_variants = ["Empty", "Discrete output", "Pwm output", "Discrete input", "Servo output"]

        self.width = 200
        self.height = 170
        self.inner_top_margin = 0
        
        self.container = ttk.Frame(self.root, relief="groove", width=self.width, height=self.height)
        self.name_label = ttk.Label(self.container, text=self.name, background="light grey", anchor=tk.CENTER)
        
        self.modules_types = [EmptyModule(), 
                                DiscreteOutputModule(self.container), 
                                PwmOutputModule(self.container), 
                                DiscreteInputModule(self.container), 
                                ServoOutput(self.container)]
        self.current_version = self.modules_types[0]
        
        self.create_common_settings()

    def clear(self):
        self.mode = self.ModuleMode.EMPTY
        self.mode_select.current(int(self.mode.value))
        self.name = "Module"
        self.module_name.delete(0, tk.END)
        self.module_name.insert(0, self.name)
        self.current_version.forget_settings()
        self.current_version = self.modules_types[0]
        self.place_common_setting()

    def place_module_version(self, top_margin):
        self.current_version.place(self.width, self.height, top_margin, self.left_margin, self.right_margin, self.bottom_margin, self.state)
        
    def place(self, width, height, margin, state, top_margin, left_margin):
        self.state = state
        self.container.place_forget()
        self.current_version.place_forget()

        self.width = width
        self.height = height
        
        self.inner_top_margin = 0

        if not (state == ModuleState.USAGE and self.mode == self.ModuleMode.EMPTY):
            self.container.place(x=self.x_pos * (width + margin) + left_margin, y=self.y_pos * (height + margin) + top_margin, width=self.width, height=self.height)

        if state == ModuleState.SETTING:
            self.forget_name()

            self.inner_top_margin = self.top_margin + 20 + self.config_margin + 20 + self.config_margin
            
            self.place_common_setting()

        elif state == ModuleState.USAGE:
            self.forget_common_settings()

            self.inner_top_margin = self.top_margin + 20 + self.config_margin

            if self.mode != self.ModuleMode.EMPTY:
                self.place_name()
            else:
                self.container.place_forget()

        self.place_module_version(self.inner_top_margin)

    def place_name(self):
        self.name_label.configure(text=self.name)
        self.name_label.place(x=self.left_margin, y=self.top_margin, height=20, width=self.width - self.left_margin - self.right_margin)

    def forget_name(self):
        self.name_label.place_forget()

    def create_common_settings(self):
        self.label = ttk.Label(self.container, text="Name: ")

        self.module_name = ttk.Entry(self.container)
        self.module_name.insert(0, self.name)
        self.module_name.bind("<KeyRelease>", self.name_changed)
        self.mode_select = ttk.Combobox(self.container, values=self.modules_variants, state="readonly")
        self.mode_select.current(int(self.mode.value))
        self.mode_select.bind("<<ComboboxSelected>>", self.mode_changedd)
        
    def place_common_setting(self):
        self.label.place(x=self.left_margin, y=self.top_margin, width=40, height=20)
        self.module_name.place(x=self.left_margin + 40 + 5, y=self.top_margin, width=self.width - self.left_margin - 40 - 5 - self.right_margin, height=20)
        self.mode_select.place(x=self.left_margin, y=self.top_margin + 20 + self.config_margin, height=20, width=self.width - self.left_margin - self.right_margin)

    def forget_common_settings(self):
        if self.label:
            self.label.place_forget()
        if self.module_name:
            self.module_name.place_forget()
        if self.mode_select:
            self.mode_select.place_forget()

    def mode_changedd(self, event):
        self.root.focus_set()
        self.mode = self.ModuleMode(self.mode_select.current())
        self.current_version.place_forget()
        self.current_version = self.modules_types[self.mode_select.current()]
        self.place_module_version(self.inner_top_margin)
        self.root.focus_set()
    
    def name_changed(self, event):
        self.name = self.module_name.get()
        self.name_label.configure(text=self.name)

    def save_settings(self):
        output_array = bytearray()
        output_array.append(len(self.name))
        output_array += bytearray(self.name, 'utf-8')
        output_array.append(self.mode.value)

        inner_module_type = self.current_version.save_settings()

        output_array += inner_module_type

        return output_array
    
    def read_settings(self, settings_array, start_pos):
        str_len = settings_array[start_pos]
        start_pos += 1

        self.name = ""

        for i in range(str_len):
            self.name += chr(settings_array[start_pos])
            start_pos += 1

        self.module_name.delete(0, tk.END)
        self.module_name.insert(0, self.name)

        self.mode = self.ModuleMode(settings_array[start_pos])
        start_pos += 1
        self.current_version = self.modules_types[self.mode.value]
        self.mode_select.set(self.modules_variants[self.mode.value])

        start_pos = self.current_version.read_settings(settings_array, start_pos)

        return start_pos
    
    def place_forget(self):
        self.forget_common_settings()
        self.container.place_forget()
        if self.current_version:
            self.current_version.place_forget()

class MainApplication:
    right_margin = 8
    left_margin = 8
    top_margin = 8
    bottom_margin = 8

    scheme_button_width = 110
    scheme_control_height = 25
    scheme_change_width = 130
    scheme_control_margin = 8

    modules_min_width = 200
    modules_min_height = 170
    modules_margin = 8

    modules_state = ModuleState.USAGE
    modules_x_max_count = 6
    modules_y_max_count = 4
    modules_x_count = 3
    modules_y_count = 2
    modules_width = modules_min_width
    modules_height = modules_min_height
    
    def modules_overall_min_width(self):
        return self.modules_x_count * (self.modules_min_width + self.modules_margin) - self.modules_margin
    
    def modules_overall_min_height(self):
        return self.modules_y_count * (self.modules_min_height + self.modules_margin) - self.modules_margin
    
    control_width = 2 * scheme_button_width + scheme_change_width + 2 * scheme_control_margin
    control_height =  scheme_control_height + scheme_control_margin
    configure_width = (scheme_button_width + 55 + 50 + 4 * scheme_control_height + 7 * scheme_control_margin)

    def min_width(self):
        return max(self.modules_overall_min_width(), self.left_margin + self.control_width + self.right_margin + (self.configure_width if self.modules_state == ModuleState.SETTING else 0))
    
    def min_height(self):
        return self.top_margin + self.control_height + self.bottom_margin + self.modules_overall_min_height()
    
    def __init__(self, root : tk.Tk):
        self.root = root
        self.root.title("SCADA")

        self.root.state('normal')

        self.root.minsize(self.min_width(), self.min_height())

        self.change_scheme_var = tk.IntVar(value=0)
        self.ChangeScheme = ttk.Checkbutton(self.root, text="Change scheme", variable=self.change_scheme_var, command=self.on_checkbox_toggle)
        self.save_button = ttk.Button(self.root, text="Save scheme", command=self.run_and_refocus(self.save_scheme))
        self.load_button = ttk.Button(self.root, text="Load scheme", command=self.run_and_refocus(self.load_scheme))
        
        self.clear_button = ttk.Button(self.root, text="Clear scheme", command=self.run_and_refocus(self.clear_scheme))
        self.rows_label = ttk.Label(self.root, text="Rows:" + str(self.modules_y_count), anchor=tk.W)
        self.rows_label.config(font=("Arial", 12))
        self.add_row_button = ttk.Button(self.root, text="+", command=self.run_and_refocus(self.add_row))
        self.remove_row_button = ttk.Button(self.root, text="-", command=self.run_and_refocus(self.remove_row))
        self.cols_label = ttk.Label(self.root, text="Cols:" + str(self.modules_x_count), anchor=tk.W)
        self.cols_label.config(font=("Arial", 12))
        self.add_col_button = ttk.Button(self.root, text="+", command=self.run_and_refocus(self.add_col))
        self.remove_col_button = ttk.Button(self.root, text="-", command=self.run_and_refocus(self.remove_col))

        self.place_control_buttons()

        self.last_width = self.root.winfo_width()
        self.last_height = self.root.winfo_height()

        self.root.bind('<Configure>', self.on_resize)

        self.modules = self.create_modules_grid()

    def create_modules_grid(self):
        grid = []
        for i in range(self.modules_x_count):
            row = []
            for j in range(self.modules_y_count):
                module = Module(self.root, i, j)
                row.append(module)
            grid.append(row)
        return grid

    def place_modules_grid(self, width, height, margin, state):
        for i in range(self.modules_x_count):
            for j in range(self.modules_y_count):
                self.modules[i][j].place(width, height, margin, state, self.top_margin + self.scheme_control_height + self.scheme_control_margin, self.left_margin)

    def print_modules(self, width, height):
        self.modules_width = (width - self.left_margin - self.right_margin - self.modules_margin * (self.modules_x_count - 1) ) / self.modules_x_count
        self.modules_height = (height - self.top_margin - self.scheme_control_height - self.scheme_control_margin - self.bottom_margin - self.modules_margin * (self.modules_y_count - 1) ) / self.modules_y_count
        
        self.place_modules_grid(self.modules_width, self.modules_height, self.modules_margin, self.modules_state)

    def recreate_modules_grid(self):
        new_grid = []
        for i in range(self.modules_x_count):
            row = []
            for j in range(self.modules_y_count):
                if i < len(self.modules) and j < len(self.modules[i]):
                    module = self.modules[i][j]
                else:
                    module = Module(self.root, i, j)
                row.append(module)
            new_grid.append(row)
        
        for i in range(len(self.modules)):
            for j in range(len(self.modules[i])):
                if i >= len(new_grid) or j >= len(new_grid[i]):
                    if self.modules[i][j].container:
                        self.modules[i][j].container.destroy()

        self.modules = new_grid

    def update_modules_grid(self):
        self.recreate_modules_grid()

        self.print_modules(self.root.winfo_width(), self.root.winfo_height())

    def run_and_refocus(self, func):
        def wrapper():
            func()
            self.root.focus_set()
        return wrapper

    def place_control_buttons(self):
        prev_x = self.left_margin
        self.save_button.place(x=prev_x, y=self.top_margin, width=self.scheme_button_width, height=self.scheme_control_height)
        prev_x += self.scheme_button_width + self.scheme_control_margin
        self.load_button.place(x=prev_x, y=self.top_margin, width=self.scheme_button_width, height=self.scheme_control_height)
        prev_x += self.scheme_button_width + self.scheme_control_margin
        self.ChangeScheme.place(x=prev_x, y=self.top_margin, width=self.scheme_change_width, height=self.scheme_control_height)
        
    def place_configure_buttons(self):
        prev_x = self.ChangeScheme.winfo_x() + self.ChangeScheme.winfo_width() + self.scheme_control_margin
        self.clear_button.place(x=prev_x, y=self.top_margin, width=self.scheme_button_width, height=self.scheme_control_height)
        prev_x += self.scheme_button_width + self.scheme_control_margin
        self.rows_label.place(x=prev_x, y=self.top_margin, width=55, height=self.scheme_control_height)
        prev_x += 55 + self.scheme_control_margin
        self.add_row_button.place(x=prev_x, y=self.top_margin, width=self.scheme_control_height, height=self.scheme_control_height)
        prev_x += self.scheme_control_height + self.scheme_control_margin
        self.remove_row_button.place(x=prev_x, y=self.top_margin, width=self.scheme_control_height, height=self.scheme_control_height)
        prev_x += self.scheme_control_height + self.scheme_control_margin
        self.cols_label.place(x=prev_x, y=self.top_margin, width=50, height=self.scheme_control_height)
        prev_x += 50 + self.scheme_control_margin
        self.add_col_button.place(x=prev_x, y=self.top_margin, width=self.scheme_control_height, height=self.scheme_control_height)
        prev_x += self.scheme_control_height + self.scheme_control_margin
        self.remove_col_button.place(x=prev_x, y=self.top_margin, width=self.scheme_control_height, height=self.scheme_control_height)
        prev_x += self.scheme_control_height + self.scheme_control_margin
        self.root.focus_set()

    def remove_configure_buttons(self):
        self.clear_button.place_forget()
        self.rows_label.place_forget()
        self.cols_label.place_forget()
        self.add_col_button.place_forget()
        self.add_row_button.place_forget()
        self.remove_col_button.place_forget()
        self.remove_row_button.place_forget()

        self.root.focus_set()

    def add_row(self):
        self.modules_y_count += 1
        if (self.modules_y_count > self.modules_y_max_count):
            self.modules_y_count = self.modules_y_max_count
        self.rows_label.configure(text = "Rows:" + str(self.modules_y_count))
        self.root.minsize(self.min_width(), self.min_height())
        self.update_modules_grid()
    def remove_row(self):
        self.modules_y_count -= 1
        if (self.modules_y_count < 1):
            self.modules_y_count = 1
        self.rows_label.configure(text = "Rows:" + str(self.modules_y_count))
        self.root.minsize(self.min_width(), self.min_height())
        self.update_modules_grid()
         
    def add_col(self):
        self.modules_x_count += 1
        if (self.modules_x_count > self.modules_x_max_count):
            self.modules_x_count = self.modules_x_max_count
        self.cols_label.configure(text = "Cols:" + str(self.modules_x_count))
        self.root.minsize(self.min_width(), self.min_height())
        self.update_modules_grid()
    def remove_col(self):
        self.modules_x_count -= 1
        if (self.modules_x_count < 1):
            self.modules_x_count = 1
        self.cols_label.configure(text = "Cols:" + str(self.modules_x_count))
        self.root.minsize(self.min_width(), self.min_height())
        self.update_modules_grid()

    def on_resize(self, event):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        
        if new_width != self.last_width or new_height != self.last_height:
            self.last_width = new_width
            self.last_height = new_height

            self.print_modules(new_width, new_height)

    def on_checkbox_toggle(self):
        state = self.change_scheme_var.get()
        GPIO.cleanup()
        self.modules_state = ModuleState.SETTING if state else ModuleState.USAGE
        self.root.minsize(self.min_width(), self.min_height())
        self.place_modules_grid(self.modules_width, self.modules_height, self.modules_margin, self.modules_state)
        if self.modules_state == ModuleState.SETTING:
            self.place_configure_buttons()
        else:
            self.remove_configure_buttons()

    def save_settings(self):
        size_array = bytearray()
        size_array.append(self.modules_x_count)
        size_array.append(self.modules_y_count)

        settings_array = bytearray()
        settings_array += size_array

        modules_settings = bytearray()

        for i in range(self.modules_x_count):
            for j in range(self.modules_y_count):
                module_settings = self.modules[i][j].save_settings()
                modules_settings += module_settings

        settings_array += modules_settings

        return settings_array

    def read_settings(self, settings_array, start_pos):
        self.modules_x_count = settings_array[start_pos]
        start_pos += 1
        self.modules_y_count = settings_array[start_pos]
        start_pos += 1

        self.rows_label.configure(text="Rows:" + str(self.modules_y_count))
        self.cols_label.configure(text="Cols:" + str(self.modules_x_count))

        for i in range(len(self.modules)):
            for j in range(len(self.modules[0])):
                self.modules[i][j].place_forget()

        for i in range(len(self.modules)):
            for j in range(len(self.modules[0])):
                del self.modules[0][0]
            del self.modules[0]

        self.recreate_modules_grid()

        for i in range(self.modules_x_count):
            for j in range(self.modules_y_count):
                start_pos = self.modules[i][j].read_settings(settings_array, start_pos)

        return start_pos

    def save_scheme(self):
        self.save_settings()
        file_path = filedialog.asksaveasfilename(defaultextension=".scd", filetypes=[("Scheme files", "*.scd"), ("All files", "*.*")])
        if file_path:
            print(f"Scheme saved: {file_path}")
            with open(file_path, 'wb') as file:
                file.write(self.save_settings())

    def load_scheme(self):
        file_path = filedialog.askopenfilename(filetypes=[("Scheme files", "*.scd"), ("All files", "*.*")])
        if file_path:
            print(f"Scheme loaded: {file_path}")
            with open(file_path, 'rb') as file:
                content = file.read()
                settings_array = bytearray(content)
                self.read_settings(settings_array, 0)

        self.print_modules(self.root.winfo_width(), self.root.winfo_height())
    
    def clear_scheme(self):
        for i in range(len(self.modules)):
            for j in range(len(self.modules[i])):
                        self.modules[i][j].clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
    
    GPIO.cleanup()
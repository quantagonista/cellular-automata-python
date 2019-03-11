import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

import pyscreenshot as ImageGrab

from .constants import START, SEED_INPUT_LABEL, PAUSE, SCREENSHOT, NEXT_STEP, DEFAULT_SCREENSHOT_FILENAME
from models.automates.crystal import Crystal
from models.field import Field
from utils import colors


class App(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.is_paused = True
        self.root = master
        self.width = 700
        self.height = 500

        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.resizable(False, False)

        self.left_bar = tk.Frame(master=self.root)
        self.left_bar.pack(side=tk.LEFT)

        self.automate_seed_entry_label = tk.Label(self.left_bar, text=SEED_INPUT_LABEL)
        self.automate_seed_entry_label.grid()

        self.automate_seed_entry = tk.Entry(self.left_bar)
        self.automate_seed_entry.bind('<Key-Return>', self.set_drawer)
        self.automate_seed_entry.grid()

        self.next_step_button = tk.Button(master=self.left_bar, text=NEXT_STEP, command=self.next_step)
        self.next_step_button.grid()

        self.pause_button_text = tk.StringVar(value=START)
        self.pause_button = tk.Button(master=self.left_bar, textvariable=self.pause_button_text, command=self.pause)
        self.pause_button.grid()

        self.screenshot_button_text = tk.StringVar(value=SCREENSHOT)
        self.screenshot_button = tk.Button(
            master=self.left_bar, textvariable=self.screenshot_button_text, command=self.screenshot
        )
        self.screenshot_button.grid()

        self.canvas_width = 500
        self.canvas_height = 500

        self.canvas = tk.Canvas(
            master=self.root,
            cnf={
                "width": self.canvas_width,
                "height": self.canvas_height
            }
        )
        self.canvas.pack(side=tk.RIGHT)  # place(x=self.width - self.canvas_width)

        field_width = 100
        field_height = 100
        self.field = Field(field_width, field_height, 5)
        self.field.set_cell(field_width // 2, field_height // 2, 1)
        self.cells = self.get_rectangles()

        self.drawer = self.get_drawer(501)
        self.redraw_field()

    def set_drawer(self, _):
        seed = self.automate_seed_entry.get()
        self.drawer = self.get_drawer(int(seed))
        self.field.refresh()
        self.drawer.set_initial(self.field)
        self.next_step()

    def update(self):
        if not self.is_paused:
            self.next_step()
            self.redraw_field()
            self.canvas.after(1, self.update)

    def redraw_field(self):
        width = self.field.get_width()
        height = self.field.get_height()
        w_range = range(width)
        h_range = range(height)
        for y in h_range:
            for x in w_range:
                color = colors.get(self.field.get_cell(y, x))
                rect = self.cells[y][x]
                self.canvas.itemconfig(rect, fill=color)

    def next_step(self):
        next_state = self.drawer.next_step(self.field)
        self.field.apply_state(next_state)
        self.redraw_field()

    @staticmethod
    def get_drawer(seed):
        # TODO: Add dynamic Drawer loading via dropdown menu
        return Crystal(seed)

    def get_rectangles(self):
        width = self.field.get_width()
        height = self.field.get_height()
        width_range = range(width)
        height_range = range(height)
        rectangles = [[None for _ in width_range] for _ in height_range]
        cell_size = self.field.get_cell_size()
        for y in range(height):
            for x in range(width):
                color = colors.get(self.field.get_cell(y, x))
                start_x = x * cell_size
                start_y = y * cell_size
                rectangle = self.canvas.create_rectangle(
                    start_x,
                    start_y,
                    start_x + cell_size,
                    start_y + cell_size,
                    fill=color
                )
                rectangles[y][x] = rectangle
        return rectangles

    def pause(self):
        self.is_paused = not self.is_paused
        self.pause_button_text.set(START if self.is_paused else PAUSE)

        self.update()

    def screenshot(self):
        initial_filename = self.get_screenshot_filename()
        initial_path = os.path.join(os.getcwd(), initial_filename)
        path = filedialog.asksaveasfilename(
            initialdir=initial_path,
            initialfile=initial_filename,
            defaultextension=".png",
            title="Save Screenshot",
            filetypes=(("jpeg files", "*.jpg"),)
        )
        if path:
            self.save_screenshot(path)
        self.save_screenshot(initial_path)

    def save_screenshot(self, path):
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(path)

    def get_screenshot_filename(self):
        return '{drawer}-{date}.png'.format(
            drawer=self.drawer.__class__.__name__,
            date=datetime.today().strftime('%m-%d-%Y')
        )

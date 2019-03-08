import tkinter as tk
from random import randint

from PIL import Image, ImageTk

from constants import SEED_INPUT_LABEL
from models.automates.crystal import Crystal
from models.field import Field
from utils import colors


class App(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.root = master
        self.width = 700
        self.height = 500

        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.resizable(False, False)

        self.automate_seed_entry_label = tk.Label(self.root, text=SEED_INPUT_LABEL)
        self.automate_seed_entry_label.place(x=20)

        self.automate_seed_entry = tk.Entry()
        self.automate_seed_entry.bind('<Key-Return>', self.set_drawer)
        self.automate_seed_entry.pack(fill=tk.BOTH)

        self.next_step_button = tk.Button(master=self.root, text='Next Step', command=self.next_step)
        self.next_step_button.pack(fill=tk.BOTH)

        self.canvas_width = 500
        self.canvas_height = 500

        self.canvas = tk.Canvas(
            master=self.root,
            cnf={
                "width": self.canvas_width,
                "height": self.canvas_height
            }
        )
        self.canvas.place(x=self.width - self.canvas_width)

        field_width = 100
        field_height = 100
        self.field = Field(field_width, field_height, 5)
        self.field.set_cell(field_width // 2, field_height // 2, 1)
        self.image = Image.new('RGB', (800, 800,))
        self.fill_image()
        self.image_field = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image_field)
        self.canvas.update()

        self.drawer = self.get_drawer(501)

    def set_drawer(self, _):
        seed = self.automate_seed_entry.get()
        self.drawer = self.get_drawer(int(seed))
        self.field.refresh()
        self.drawer.set_initial(self.field)
        self.next_step()

    def update(self):
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
        # next_state = self.drawer.next_step(self.field)
        # self.field.apply_state(next_state)
        # self.redraw_field()
        self.fill_image()
        self.image_field = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image_field)
        self.canvas.update()

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

    def fill_image(self):
        pixels = self.image.load()
        color = self.get_random_color()
        for y in range(self.canvas_height):
            for x in range(self.canvas_width):
                pixels[x, y] = color

    def get_random_color(self):
        return randint(0, 255), randint(0, 255), randint(0, 255)

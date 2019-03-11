import tkinter as tk
from random import randint

from PIL import Image, ImageTk
from PIL.ImageDraw import ImageDraw

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

        self.canvas_size = 500

        self.canvas = tk.Canvas(
            master=self.root,
            cnf={
                "width": self.canvas_size,
                "height": self.canvas_size
            }
        )
        self.canvas.place(x=self.width - self.canvas_size)

        field_width = field_height = 100
        self.field = Field(field_width, field_height, 5)
        self.field.set_cell(field_width // 2, field_height // 2, 1)

        self.image_file = Image.new('RGB', (self.canvas_size, self.canvas_size,), 'red')
        self.image_file.save('temp.png')

        self.image_drawer = ImageDraw(self.image_file)
        self.image_canvas = ImageTk.PhotoImage(self.image_file)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_canvas)
        self.canvas.update()
        self.redraw_field()

        self.drawer = self.get_drawer(501)
        # self.update()

    def set_drawer(self, _):
        seed = self.automate_seed_entry.get()
        self.drawer = self.get_drawer(int(seed))
        self.field.refresh()
        self.drawer.set_initial(self.field)
        self.next_step()

    def update(self):
        self.next_step()
        self.canvas.after(1, self.update)

    def redraw_field(self):
        width = self.field.get_width()
        height = self.field.get_height()
        w_range = range(width)
        h_range = range(height)
        for y in h_range:
            for x in w_range:
                color = colors.get(self.field.get_cell(y, x))
                self.draw_cell(y, x, color)

    def next_step(self):
        x = randint(0, 500)
        y = randint(0, 500)
        self.image_drawer.rectangle((x, y, x + 50, y + 50), fill='white', outline='yellow', width=5)
        self.image_file.save('temp.png')
        image_file = Image.open('temp.png')
        image_canvas = ImageTk.PhotoImage(image_file)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_canvas)
        self.canvas.update()
        # next_state = self.drawer.next_step(self.field)
        # self.field.apply_state(next_state)
        # self.redraw_field()

    @staticmethod
    def get_drawer(seed):
        # TODO: Add dynamic Drawer loading via dropdown menu
        return Crystal(seed)

    def draw_cell(self, y, x, color):
        xy = (x, y, x + self.field.cell_size, y + self.field.cell_size)
        self.image_drawer.rectangle(xy, fill=color)

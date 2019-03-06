import tkinter as tk

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

        self.drawer = self.get_drawer(501)
        self.draw_field()

        self.update()

    def set_drawer(self, _):
        seed = self.automate_seed_entry.get()
        self.drawer = self.get_drawer(int(seed))
        self.field.refresh()
        self.drawer.set_initial(self.field)
        self.next_step()

    def update(self):
        self.next_step()
        self.draw_field()
        self.canvas.after(10, self.update)

    def draw_field(self):
        width = self.field.get_width()
        height = self.field.get_height()
        cell_size = self.field.get_cell_size()
        for y in range(height):
            for x in range(width):
                color = colors.get(self.field.get_cell(y, x))
                start_x = x * cell_size
                start_y = y * cell_size
                self.canvas.create_rectangle(
                    start_x,
                    start_y,
                    start_x + cell_size,
                    start_y + cell_size,
                    fill=color
                )

    def next_step(self):
        next_state = self.drawer.next_step(self.field)
        self.field.apply_state(next_state)
        self.draw_field()

    @staticmethod
    def get_drawer(seed):
        # TODO: Add dynamic Drawer loading via dropdown menu
        return Crystal(seed)


if __name__ == '__main__':
    root = tk.Tk()
    main = App(root)
    main.mainloop()

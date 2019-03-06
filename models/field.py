import random


class Field:

    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = self.get_initial_field()

    def refresh(self):
        self.cells = self.get_initial_field()

    def get_cell_size(self):
        return self.cell_size

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_initial_field(self):
        field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        return field

    def set_cell(self, y, x, value):
        self.cells[y][x] = value

    def apply_state(self, state):
        self.cells = state.copy()

    def fill_randomly(self):
        field = [
            [random.randint(0, 1) for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.cells = field

    def get_cell(self, y, x):
        try:
            return self.cells[y][x]

        except IndexError:
            return 0

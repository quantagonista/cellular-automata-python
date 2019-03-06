from models.automates.base import Drawer
from models.rules import WolframRules
from utils import binarify_seed_eight_digits


class Wolfram(Drawer):
    def __init__(self, seed):
        self.rules = WolframRules.get_rules(binarify_seed_eight_digits(seed))

    def next_step(self, field):
        new_state = self.calculate_new_state(field)
        return new_state

    def calculate_new_state(self, field):
        width = field.get_width()
        height = field.get_height()
        new_state = field.cells.copy()

        for y in range(1, height):
            for x in range(width):
                neighbours_count = self.get_neighbours_count(x, y, field)
                new_state[y][x] = self.rules.get(neighbours_count)

        return new_state

    def get_neighbours_count(self, x, y, field):
        width = len(field[0])

        top_y = y - 1
        left_x = x - 1
        right_x = x + 1

        top_left = field[top_y][left_x] if (top_y >= 0 and left_x >= 0) else 0
        top = field[top_y][x] if top_y >= 0 else 0
        top_right = field[top_y][right_x] if (top_y >= 0 and right_x < width) else 0

        return top_left + top + top_right

    def set_initial(self, field):
        width = field.get_width()
        field.set_cell(0, width // 2, 1)

from models.automates.base import Drawer
from models.rules import CrystalRule
from utils import binarify_seed_ten_digits, get_empty_state


class Crystal(Drawer):
    def __init__(self, seed):
        self.rules = CrystalRule.get_rules(binarify_seed_ten_digits(seed))

    def next_step(self, field):
        width = field.get_width()
        height = field.get_height()

        next_state = get_empty_state(width, height)

        h_range = range(1, height - 1)
        w_range = range(1, width - 1)

        for y in h_range:
            for x in w_range:
                current_state = field.get_cell(y, x)
                neighbours_count = self.get_neighbours_count(field, y, x)
                next_rule = '{}{}'.format(current_state, neighbours_count)
                next_cell_state = self.rules.get(next_rule)
                next_state[y][x] = next_cell_state

        return next_state

    def get_neighbours_count(self, field, y, x):
        top = field.get_cell(y - 1, x)
        bottom = field.get_cell(y + 1, x)
        left = field.get_cell(y, x - 1)
        right = field.get_cell(y, x + 1)

        return top + bottom + left + right

    def set_initial(self, field):
        width = field.get_width()
        height = field.get_height()
        field.set_cell(height // 2, width // 2, 1)

def binarify_seed_ten_digits(seed):
    return '{0:010b}'.format(seed)


def binarify_seed_eight_digits(seed):
    return '{0:08b}'.format(seed)


def get_empty_state(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]


colors = {
    0: 'black',
    1: 'white',
}

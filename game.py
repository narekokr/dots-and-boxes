from state import State


class Game(object):

    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height
        self.players = ('red', 'blue')  # these must be valid tkinter color names
        print(self.width, self.height)
        self.dots = frozenset((i, j) for i in range(self.height) for j in range(self.width))
        self.boxes = frozenset((i, j) for i in range(self.height - 1) for j in range(self.width - 1))
        self.h_lines = frozenset((i, j) for i in range(self.height - 1) for j in range(self.width))
        self.v_lines = frozenset((i, j) for i in range(self.height) for j in range(self.width - 1))
        self.dots_count = self.width * self.height

    def make_initial_state(self):
        return State(self)

from chain_counter import ChainCounter
from helper import get_new_coordinates


class State(object):
    def __init__(self, game):
        self.game = game
        self.whose_turn = game.players[0]
        self.box_owners = {}
        self.h_line_owners = {}
        self.v_line_owners = {}

    def copy(self):
        res = State(self.game)
        res.whose_turn = self.whose_turn
        res.box_owners = self.box_owners.copy()
        res.h_line_owners = self.h_line_owners.copy()
        res.v_line_owners = self.v_line_owners.copy()
        return res

    def get_whose_turn(self):
        return self.whose_turn

    def get_moves(self):
        h_moves = [('h', h) for h in self.game.h_lines if h not in self.h_line_owners]
        v_moves = [('v', v) for v in self.game.v_lines if v not in self.v_line_owners]
        return h_moves + v_moves

    def apply_move(self, move):

        orientation, cell = move

        if orientation == 'h':
            self.h_line_owners[cell] = self.whose_turn
        elif orientation == 'v':
            self.v_line_owners[cell] = self.whose_turn

        new_boxes = 0
        for box in self.game.boxes:
            (i, j) = box

            if (i, j) not in self.box_owners \
                    and (i, j) in self.h_line_owners \
                    and (i, j) in self.v_line_owners \
                    and (i, j + 1) in self.h_line_owners \
                    and (i + 1, j) in self.v_line_owners:
                new_boxes += 1
                self.box_owners[box] = self.whose_turn

        if new_boxes == 0:
            self.whose_turn = self.game.players[(self.game.players.index(self.whose_turn) + 1) % len(self.game.players)]

        return self

    def is_terminal(self):
        return len(self.box_owners) == len(self.game.boxes)

    def is_end_game(self):
        return len(self.h_line_owners.keys()) + len(self.v_line_owners.keys()) > self.total_count_of_lines() / 2

    def total_count_of_lines(self):
        horizontal_lines = len(self.game.h_lines)
        vertical_lines = len(self.game.v_lines)

        return horizontal_lines + vertical_lines

    def get_chain_score(self, player):
        chain_count = self.count_long_chains()
        dots_count = self.game.dots_count
        is_even = (chain_count + dots_count) % 2 == 0
        first_player = player == self.game.players[0]
        if first_player:
            return 1 if is_even else -1
        else:
            return -1 if is_even else 1

    def get_score(self, player):
        if not self.is_end_game():
            return self.get_chain_score(player)
        score = 0
        for box in self.game.boxes:
            owner = self.box_owners.get(box)
            if owner:
                if owner is player:
                    score += 1
                else:
                    score -= 1
        return score

    def hash_lines(self):
        v_line_owners = frozenset(self.v_line_owners.keys())
        h_line_owners = frozenset(self.h_line_owners.keys())

        return hash(v_line_owners) + hash(h_line_owners)

    def mirror(self):
        if self.game.width == self.game.height:
            return self.mirror_n_x_n()
        else:
            return self.mirror_m_x_n()

    def mirror_m_x_n(self):
        x_mirror_horizontal, x_mirror_vertical, x_mirror_boxes = self.mirror_coordinates(axis='x')
        y_mirror_horizontal, y_mirror_vertical, y_mirror_boxes = self.mirror_coordinates(axis='y')

        x_mirror = self.copy()
        x_mirror.v_line_owners = x_mirror_vertical
        x_mirror.h_line_owners = x_mirror_horizontal
        x_mirror.box_owners = x_mirror_boxes

        y_mirror = self.copy()
        y_mirror.v_line_owners = y_mirror_vertical
        y_mirror.h_line_owners = y_mirror_horizontal
        y_mirror.box_owners = y_mirror_boxes

        x_y_mirror = y_mirror.copy()
        x_mirror_horizontal, x_mirror_vertical, x_mirror_boxes = x_y_mirror.mirror_coordinates(axis='x')

        x_y_mirror.v_line_owners = x_mirror_horizontal
        x_y_mirror.h_line_owners = x_mirror_horizontal
        x_y_mirror.box_owners = x_mirror_boxes

        return x_mirror, y_mirror, x_y_mirror

    def mirror_n_x_n(self):
        x_mirror, y_mirror, x_y_mirror = self.mirror_m_x_n()

        reverse = self.copy()
        horizontal, vertical, boxes = reverse.mirror_coordinates(reverse=True)
        reverse.box_owners = boxes
        reverse.h_line_owners = horizontal
        reverse.v_line_owners = vertical

        reversed_x_mirror, reversed_y_mirror, reversed_x_y_mirror = reverse.mirror_m_x_n()

        return x_mirror, y_mirror, x_y_mirror, reverse, reversed_x_mirror, reversed_y_mirror, reversed_x_y_mirror

    def mirror_coordinates(self, axis='x', reverse=False):
        h_line_owners = {}
        v_line_owners = {}
        box_owners = {}
        for coord, value in self.h_line_owners.items():
            new_coordinates = get_new_coordinates(coord, vertical=False, width=self.game.width, height=self.game.height,
                                                  axis=axis, reverse=reverse)
            h_line_owners[new_coordinates] = value
        for coord, value in self.v_line_owners.items():
            new_coordinates = get_new_coordinates(coord, vertical=True, width=self.game.width, height=self.game.height,
                                                  axis=axis, reverse=reverse)
            v_line_owners[new_coordinates] = value
        for coord, value in self.box_owners.items():
            new_coordinates = get_new_coordinates(coord, vertical=True, width=self.game.width - 1,
                                                  height=self.game.height - 1, axis=axis, reverse=reverse)
            box_owners[new_coordinates] = value

        return [h_line_owners, v_line_owners, box_owners]

    def count_long_chains(self):
        chain_counter = ChainCounter(self)
        res = chain_counter.count_chains()
        return res

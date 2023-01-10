from random import choice
from math import *


class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parentNode = parent
        self.childNodes = []
        self.original_state = state
        self.score = 0.0
        self.visits = 0.0
        self.untriedMoves = state.get_moves()
        self.player = state.get_whose_turn()

    def UCTSelectChild(self):
        s = sorted(self.childNodes, key=lambda c: float(c.score) / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def add_child(self, m, s):
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def update(self, result):
        self.visits += 1
        self.score += result


def think(root_state):
    root_node = Node(state=root_state)

    def reward_func(me, goal_state):
        reward = 0.0
        if me == 'blue':
            reward = goal_state.get_score('blue') - goal_state.get_score('red')
        else:
            reward = goal_state.get_score('red') - goal_state.get_score('blue')
        return reward

    rollouts = 0
    while rollouts < 10000:
        node = root_node
        state = root_state.copy()
        rollouts += 1
        while len(node.untriedMoves) == 0 and len(node.childNodes) != 0:
            node = node.UCTSelectChild()
            state.apply_move(node.move)
        if len(node.untriedMoves) != 0:
            m = choice(node.untriedMoves)
            state.apply_move(m)
            node = node.add_child(m, state)
        while not state.is_terminal():
            state.apply_move(choice(state.get_moves()))
        while node is not None:
            if node.parentNode:
                final_score = reward_func(node.parentNode.player, state)
            else:
                final_score = 0
            node.update(final_score)
            node = node.parentNode

    selected = sorted(root_node.childNodes, key=lambda c: c.visits)[-1]
    return selected.move

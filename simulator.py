from game import Game
from collections import defaultdict

import sys
import time
import importlib
import json

assert len(sys.argv) == 3
_, red_bot, blue_bot = sys.argv

width = input('Input the width: ')
height = input('Input the height: ')
iteration = input('Input the number of iterations: ')

assert width.isdigit() and height.isdigit() and iteration.isdigit()

bots = {
    'red': importlib.import_module(red_bot),
    'blue': importlib.import_module(blue_bot),
}

rounds = int(iteration)
wins = defaultdict(int)
time_taken = {}

game = Game(width=int(width), height=int(height))

if blue_bot == red_bot:
    blue_bot = blue_bot + '_2'

for i in range(rounds):

    print("")
    print("Round %d, fight!" % i)

    state = game.make_initial_state()
    time_taken[i] = {
        red_bot: [],
        blue_bot: []
    }

    while not state.is_terminal():
        tick = time.time()
        move = bots[state.whose_turn].think(state.copy())
        tock = time.time()
        print(state.whose_turn, "thought for", tock - tick, "seconds")
        player = red_bot if state.whose_turn == 'red' else blue_bot
        time_taken[i][player].append(tock - tick)
        state.apply_move(move)

    score = state.get_score('red') - state.get_score('blue')
    winner = game.players[0] if score > 0 else game.players[1] if score < 0 else 'draw'
    if score != 0:
        print("The %s bot wins this round!" % winner)
    else:
        print("It's a draw!")
    wins[winner] = 1 + wins[winner]

print("")
print("Final win counts:", dict(wins))

results = {
    "wins": wins,
    "time_taken": time_taken
}

with open('results.json', 'w') as file:
    file.write(json.dumps(results))

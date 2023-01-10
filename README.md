# Dots and boxes

## Requirements
- Install python 3
- Install pip
- Install tkinter with `pip install tk`

## Features

### Algorithms

There are 2 algorithms and a random bot. The algorithms are Alpha Beta and Monte Carlo

### GUI

To run the game with GUI use the following command `python3 interactive.py mcts alphabeta`

The first argument will be the algorithm used for the first player (red), and the second argument will be for player 2 (blue).
So to run Monte Carlo against random bot, this will be used `python3 interactive.py mcts random_bot`

The game will ask for the width and height of the board.

To place a line, simply click on the available lines. By default, the AIs will be turned off, and you can turn them on with button at the bottom. You will have to restart the game if you do that, however.

### Simulator

To run the game in simulation mode, use the following command `python3 simulator.py mcts random_bot`

The game will ask for the width and height of the board, and the number of simulations.

The running times and results will be printed during the game, and the final results will be saved in `results.json` once all the simulations are finished.

### References

The GUI and parts of the algorithms are taken from [here](https://github.com/decoder746/dots-and-boxes-mcts)
from math import inf


def alphabeta(state, depth=5, alpha=-inf, beta=inf):
    best_move = None
    moves = state.get_moves()
    player = state.get_whose_turn()

    if len(moves) == 0 or depth == 0:
        score = state.get_score('red') - state.get_score('blue')
        return ['X', score]

    if player == 'red':
        best_score = -inf
        for move in moves:
            state_copy = state.copy()
            state_copy.apply_move(move)
            current_move, current_score = alphabeta(state_copy, depth - 1, alpha, beta)
            if current_score > best_score:
                best_move = move
                best_score = current_score
            alpha = max(best_score, alpha)
            if beta <= alpha:
                break
        return [best_move, best_score]
    else:
        best_score = inf
        for move in moves:
            state_copy = state.copy()
            state_copy.apply_move(move)
            current_move, current_score = alphabeta(state_copy, depth - 1, alpha, beta)
            if current_score < best_score:
                best_move = move
                best_score = current_score
            beta = min(best_score, beta)
            if beta <= alpha:
                break
        return [best_move, best_score]


def think(state):
    return alphabeta(state, 6)[0]

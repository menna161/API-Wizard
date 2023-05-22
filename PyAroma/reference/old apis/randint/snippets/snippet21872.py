from random import randint
from isolation import Board


def get_move(self, game, time_left):
    'Randomly select a move from the available legal moves.\n\n        Parameters\n        ----------\n        game : `isolation.Board`\n            An instance of `isolation.Board` encoding the current state of the\n            game (e.g., player locations and blocked cells).\n\n        time_left : callable\n            A function that returns the number of milliseconds left in the\n            current turn. Returning with any less than 0 ms remaining forfeits\n            the game.\n\n        Returns\n        ----------\n        (int, int)\n            A randomly selected legal move; may return (-1, -1) if there are\n            no available legal moves.\n        '
    legal_moves = game.get_legal_moves()
    if (not legal_moves):
        return ((- 1), (- 1))
    return legal_moves[randint(0, (len(legal_moves) - 1))]

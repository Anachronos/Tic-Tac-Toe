class Player(object):
    pass


class GameMatrix(object):
    """GameMatrix is the playing board of a Tic-tac-toe game.

    It is responsible for storing player moves and verifying
    that a given move is valid.
    """
    def __init__(self):
        self._matrix = [[0 for x in range(3)] for x in range(3)]
        self._valid_input = ['x', 'o']

    def empty(self, coords):
        x, y = coords
        if self._matrix[x][y] == 0:
            return True
        return False

    def mark(self, char, coords):
        """Places char on the given coordinates."""
        x, y = coords

        if char not in self._valid_input:
            raise GameMatrix.InvalidMark

        self._matrix[x][y] = char

    class InvalidMark(Exception):
        pass


class Game(object):
    """Game is the interface for a Tic-tac-toe game."""
    def __init__(self):
        self._game_matrix = GameMatrix()
    
    def mark(self, player):
        pass

    def _check_winner(self):
       pass 



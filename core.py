import itertools

class Player(object):
    pass


class GameMatrix(object):
    """GameMatrix is the playing board of a Tic-tac-toe game.

    It is responsible for storing player moves and verifying
    that a given move is valid.
    """
    def __init__(self, matrix=None):
        if not matrix:
            self._matrix = [[0 for x in range(3)] for x in range(3)]
        else:
            self._matrix = matrix

        self._valid_input = ['x', 'o']

        self.EMPTY = 0 # Initial state
        self.ACTIVE = 1

        # Terminal states
        self.X_WIN = 2
        self.O_WIN = 3
        self.DRAW = 4

    def at(self, coords):
        x, y = coords
        return self._matrix[x][y]

    def empty(self, coords):
        x, y = coords
        if self._matrix[x][y] == 0:
            return True
        return False

    def mark(self, char, coords):
        """Places char on the given coordinates.
        Once a coordinate has been "marked", it CANNOT be changed.
        """
        if self.state() not in (self.EMPTY, self.ACTIVE, self.DRAW):
            raise self.InvalidMark("Game is already finished.")

        x, y = coords

        if char not in self._valid_input:
            raise self.InvalidMark("Invalid character.")

        try:
            if not self.empty(coords):
                raise self.InvalidMark("Coordinates are not empty.")

            self._matrix[x][y] = char
        except IndexError:
            raise self.InvalidMark("Out of bounds.")

    def _full(self):
        """Returns true if every one of the 9 fields are filled."""
        count = 0
        for y in range(3):
            for x in range(3):
                if self._matrix[x][y] != 0:
                    count += 1
        return True if count == 9 else False

    def _empty(self):
        for y in range(3):
            for x in range(3):
                if self._matrix[x][y] != 0:
                    return False
        return True

    def state(self):
        """Returns the state of the game: inactive (empty), active,
        player X won, player O won."""
        if self._empty():
            return self.EMPTY
        else:
            if self._win_check('x'):
                return self.X_WIN
            elif self._win_check('o'):
                return self.O_WIN
            else:
                if self._full():
                    return self.DRAW
                else:
                    return self.ACTIVE
             
    def _win_check(self, char):
        """Verifies every possible win combination and returns
        true if one of them exists."""
        col1 = [(0,0), (0,1), (0,2)]
        col2 = [(1,0), (1,1), (1,2)]
        col3 = [(2,0), (2,1), (2,2)]
        
        row1 = [(0,0), (1,0), (2,0)]
        row2 = [(0, 1), (1,1), (2,1)]
        row3 = [(0,2), (1,2), (2,2)]

        diag1 = [(2,0), (1,1), (0,2)]
        diag2 = [(0,0), (1,1), (2,2)]

        possible_wins = [col1, col2, col3, row1, row2, row3, diag1, diag2]

        # Check that the given coords has char present.
        mark = lambda c: self._matrix[c[0]][c[1]] == char
        
        for row in possible_wins:
            mark_count = 0
            for coords in row:
                if mark(coords):
                    mark_count += 1
            if mark_count == 3:
                return True

        return False

    def __str__(self):
        preview = " {0} | {1} | {2}\n" \
            "---+---+---\n" \
            " {3} | {4} | {5}\n" \
            "---+---+---\n" \
            " {6} | {7} | {8}\n"

        values = [x for row in self._matrix for x in row] 
        return(preview.format(*values).replace('0', ' '))

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



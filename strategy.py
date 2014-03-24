from core import GameMatrix

class State(object):
    """Represents a tic-tac-toe state as a node in the state tree."""
    def __init__(self, value=None):
        self._children = []
        self._value = value
        self.utility = None
        self.terminal = False

    def attach_child(self, state):
        self._children.append(state)

    def key(self):
        """Maps to node state."""
        pass

    def __eq__(self, other):
       return self._value == other 

    def __len__(self):
        return len(self._children)

    def __str__(self):
        return "[\"{0}\": {1}]".format(self._value, self.utility)

    def visit(self):
        return self._value

    def children(self):
        return self._children


class StateTree(object):
    """StateTree is a tic-tac-toe game tree that tries to find the
    optimal move to cause a win or draw for MAX.
    
    MAX is the player who is employing the tree (the computer player),
    who is trying to maximize his chances of winning the game.

    MIN is the opponent player, who wants to minimize MAX's chances of
    winning the game."""
    def __init__(self, goal='x', maxfirst=True, depth=9):
        self.head = None
        self.maxfirst = maxfirst
        self._depth = depth
        # The tic-tac-toe mark controlled by MAX
        self._goal = goal

    def generate_states(self, from_sequence='000000000'):
        self.head = State(from_sequence)

        if self.maxfirst:
            self._generate_states(self.head, from_sequence, self._depth)
        
    def _generate_states(self, parent_state, sequence, depth):
        if depth == 0:
            return

        # Determine which "mark" has the move in this turn (depth)
        if depth % 2 == 0 and self.maxfirst:
            char = 'o'
        else:
            char = 'x'
        sequences = create_tictactoe_states(sequence, char)

        for seq in sequences:
            s = State(seq)
            parent_state.attach_child(s)
            self._generate_states(s, seq, depth-1)

    def _utility(self, state):
        """Returns the utility of a state."""
        seq = state.visit()
        matrix = matrix_1d_to_2d(seq) 

        if matrix.state() == matrix.DRAW:
            return 0
        
        if self._goal == 'x':
            if matrix.state() == matrix.X_WIN:
                return 1
            else:
                return -1
        else:
            if matrix.state() == matrix.O_WIN:
                return 1
            else:
                return -1

    def minimax(self):
        """The minimax algorithm is a recursive function which calculates
        the utility of a state based off the terminal node values."""
        return self._max_value(self.head, self._depth)

    def _min_value(self, state, depth):
        if depth == 1: return self._utility(state)
        value = 100
        for s in state.children():
            value = min(value, self._max_value(s, depth-1))

        state.utility = value

        return value

    def _max_value(self, state, depth):
        if depth == 1: return self._utility(state)
        value = -100
        for s in state.children():
            value = max(value, self._min_value(s, depth-1))

        state.utility = value

        return value

    def find_optimal_move(self):
        print("Next states:")
        for child in self.head.children():
            print(child)

    def state(self):
        return str(self.head)

    def move_next_state(self):
        self.head = self._bfs_queue.pop(0)
        self._bfs_queue.append(*self.head.children())

    def move_state(self, new_state):
        for child in self.head.children():
            if child == new_state:
                print("{0} -> {1}".format(self.head, child))
                self.head = child
                return
        raise StateTree.InvalidState

    class InvalidState(Exception):
        pass


def create_tictactoe_states(parent_seq, char):
    """
    Returns a list of states (represented as a string of possible
    tic-tac-toe moves) that immediately follow from the parent sequence.
    """
    # Optimization: If computer has first move, we can reduce the subsequent
    # tree can choosing only one of 3 moves. In the first move, the edge
    # marks are equivalent with each other, and also the corner marks.
    if parent_seq == '000000000':
        return ['x00000000', '0x0000000', '0000x0000']

    # Store the indices of every zero
    indices = []
    for i in range(len(parent_seq)):
        if parent_seq[i] == '0':
            indices.append(i)

    children_seq = []
    
    for i in indices:
        children_seq.append(parent_seq[0:i] + char + parent_seq[i+1:len(parent_seq)])

    return children_seq

def matrix_1d_to_2d(sequence):
    """Returns a GameMatrix object."""
    matrix = []
    r = [0, 3, 6]
    for i in r:
        matrix.append([x for x in sequence[i:i+3]])

    return GameMatrix(matrix)

if __name__ == '__main__':
    import time
    stree = StateTree(depth=9)
    start = time.time()
    stree.generate_states()
    end = time.time()
    print("Done in {0} seconds.".format(str(end-start)))
    stree.minimax()
    stree.move_state("0000x0000")
    stree.move_state("o000x0000")
    stree.find_optimal_move()
    stree.move_state("o00xx0000")
    stree.find_optimal_move()
    stree.move_state("oo0xx0000")
    stree.find_optimal_move()
    stree.move_state("oo0xxx000")
    stree.find_optimal_move()

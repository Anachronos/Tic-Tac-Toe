class State(object):
    """Represents a tic-tac-toe state as a node in the state tree."""
    def __init__(self, value=None):
        self._children = []
        self._value = value
        self.terminal = False

    def attach_child(self, state):
        self._children.append(state)

    def key(self):
        """Maps to node state."""
        pass

    def __len__(self):
        return len(self._children)

    def visit(self):
        return self._value


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
        self._goal = goal

    def generate_states(self, from_sequence='000000000'):
        self.head = State()

        if self.maxfirst:
            self._generate_states(self.head, from_sequence, self._depth)
        
    def _generate_states(self, parent_state, sequence, depth):
        if depth == 0:
            return

        # Determine which "mark" has the move in this turn (depth)
        if depth % 2 == 0 and self.maxfirst:
            char = 'x'
        else:
            char = 'o'
        sequences = create_tictactoe_states(sequence, char)

        for seq in sequences:
            s = State(seq)
            parent_state.attach_child(s)
            self._generate_states(s, seq, depth-1)

    def _utility(self):
        pass

    def _minimax(self, state):
        """The minimax algorithm is a recursive function which calculates
        the utility of a state based off the terminal node values."""

    def _min_value(self, state, depth):
        if depth == 1: return state.value()

    def _max_value(self, state, depth):
        pass

    def find_optimal_move(self, current_state):
        pass

    def move_next_state(self, new_state):
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

if __name__ == '__main__':
    import time
    stree = StateTree(depth=9)
    start = time.time()
    stree.generate_states()
    end = time.time()
    print("Done in {0} seconds.".format(str(end-start)))

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

    def __eq__(self, other):
       return self._value == other 

    def __len__(self):
        return len(self._children)

    def __str__(self):
        return "\"{0}\": {1}".format(self._value, self.utility)

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
        self._depth = depth
        # The tic-tac-toe mark controlled by MAX
        self.maxfirst = maxfirst
        self._goal = goal

        self.count = 0

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

    def minimax(self, from_sequence='000000000'):
        """The minimax algorithm is a recursive function which calculates
        the utility of a state based off the terminal node values.
        
        from_sequence: The initial state for the game tree."""
        self.head = State(from_sequence)
        if self.maxfirst:
            return self._minimax(self.head, self._depth, True)
        else:
            return self._minimax(self.head, self._depth-1, True)

    def minimax_decision(self):
        """Returns the next best move as a string."""
        next_states = self.head.children() 
        # There may be more than one optimal state. It doesn't matter
        # which of them is chosen.
        for s in next_states:
            if s.utility == 1:
                return s.visit()
        for s in next_states:
            if s.utility == 0:
                return s.visit()

    def _minimax(self, state, depth, ismax):
        if depth == 0:
            state.utility = self._utility(state)
            return state.utility

        # Need to discard states which are already considered win or draw,
        # otherwise the correct utility value will not bubble up, since the
        # utility function will evaluate states which may have an invalid
        # tic-tac-toe state. 
        # It is important that the value of utility is changed if one of the
        # following conditionals are true. Otherwise, the draw or winning states
        # will not have a utility (even though the value bubbles up).
        matrix = matrix_1d_to_2d(state.visit()) 
        s = matrix.state()
        if (self._goal == 'x' and s == matrix.X_WIN) or \
            (self._goal == 'o' and s == matrix.O_WIN):
            state.utility = 1
            return 1
        if s == matrix.DRAW:
            state.utility = 0
            return 0

        if (self._goal == 'x' and s == matrix.O_WIN) or \
            (self._goal == 'o' and s == matrix.X_WIN):
            state.utility = -1
            return -1
 
        if depth % 2 == 0:
            char = 'x'   
        else:
            char = 'o' 

        sequences = create_tictactoe_states(state.visit(), char)
  
        if ismax:
            value = -100
        else:
            value = 100

        for seq in sequences:
            s = State(seq)
            self.count += 1
            state.attach_child(s)
            if ismax:
                value = max(value, self._minimax(s, depth-1, False))
            else:
                value = min(value, self._minimax(s, depth-1, True))

        state.utility = value

        return value

    def state(self):
        return str(self.head)

    def next_state(self):
        self.head = self._bfs_queue.pop(0)
        self._bfs_queue.append(*self.head.children())

    def change_state(self, new_state):
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
        return [char + '00000000', '0' + char + '0000000', '0000' + char + '0000']

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
        row = []
        for x in sequence[i:i+3]:
            if x == '0':
                row.append(0)
            else:
                row.append(x)
        matrix.append(row)

    return GameMatrix(matrix)

if __name__ == '__main__':
    import time
    import pdb

    stree = StateTree(goal='o', depth=9)
    start = time.time()
    stree.minimax()
    end = time.time()
    print("Minimax done in {0} seconds.".format(str(end-start)))
    print("Nodes: {0}".format(stree.count))
    #pdb.set_trace()
    print(stree.minimax_decision())
    stree.change_state(stree.minimax_decision())
    stree.change_state(stree.minimax_decision()) # Opponent's move
    stree.change_state(stree.minimax_decision())
    stree.change_state(stree.minimax_decision()) # Opponent's move
    stree.change_state(stree.minimax_decision())
    stree.change_state(stree.minimax_decision()) # Opponent's move
    stree.change_state(stree.minimax_decision())
    stree.change_state(stree.minimax_decision()) # Opponent's move

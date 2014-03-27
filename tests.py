import unittest
import core
import strategy
import time

class GameMatrixTest(unittest.TestCase):
    def setUp(self):
        self.matrix = core.GameMatrix()

    def test_empty_state(self):
        for y in range(0,3):
            for x in range(0,3):
                self.assertTrue(self.matrix.empty((x,y)))

    def test_mark_move(self):
        self.matrix.mark('x', (0,0))
        self.matrix.mark('o', (2,1))

        self.assertFalse(self.matrix.empty((0,0)))
        self.assertFalse(self.matrix.empty((2,1)))

        # Verify that the rest of the fields are empty
        for y in range(0, 3):
            for x in range(0, 3):
                if (x, y) not in [(0,0), (2, 1)]:
                    self.assertTrue(self.matrix.empty((x, y)))

    def test_invalid_mark(self):
        # Test an invalid mark
        self.assertRaises(core.GameMatrix.InvalidMark,
                self.matrix.mark, 'y', (1, 1))
        # Test an out of bounds mark
        self.assertRaises(core.GameMatrix.InvalidMark,
                self.matrix.mark, 'x', (3,1))

    def test_xwin_states(self):
        """Test that player X can win."""
        self.assertTrue(self.matrix.state() == self.matrix.EMPTY)

        self.matrix.mark('x', (0,0))
        self.matrix.mark('o', (1,0))
        self.matrix.mark('x', (0,1))
        self.matrix.mark('o', (2,0))
        self.matrix.mark('x', (0,2))
        self.assertTrue(self.matrix.state() == self.matrix.X_WIN)

        self.assertTrue(self.matrix._win_check('x'))
        self.assertFalse(self.matrix._win_check('o'))

    def test_owin_states(self):
        """Test that player O can win."""
        self.assertTrue(self.matrix.state() == self.matrix.EMPTY)

        self.matrix.mark('o', (0,0))
        self.matrix.mark('x', (2,1))
        self.matrix.mark('o', (1,0))
        self.matrix.mark('x', (1,2))
        self.matrix.mark('o', (2,0))
        self.assertTrue(self.matrix.state() == self.matrix.O_WIN)

        self.assertTrue(self.matrix._win_check('o'))
        self.assertFalse(self.matrix._win_check('x'))

    def test_draw(self):
        self.assertTrue(self.matrix.state() == self.matrix.EMPTY)

        self.matrix.mark('x', (0,0))
        self.matrix.mark('o', (1,0))
        self.matrix.mark('x', (0,1))
        self.matrix.mark('o', (0,2))
        self.matrix.mark('x', (1,1))
        self.matrix.mark('o', (2,1))
        self.matrix.mark('x', (2,0))
        self.matrix.mark('o', (2,2))
        self.matrix.mark('x', (1,2))
        self.assertTrue(self.matrix.state() == self.matrix.DRAW)

        self.assertFalse(self.matrix._win_check('o'))
        self.assertFalse(self.matrix._win_check('x'))


class StrategyTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_minimax_x_win(self):
        stree = strategy.StateTree(depth=9)
        start = time.time()
        stree.minimax()
        end = time.time()
        
        while stree.minimax_decision():
            stree.change_state(stree.minimax_decision())

        matrix = strategy.matrix_1d_to_2d(stree.head.visit())
        self.assertTrue(matrix.state() == core.GameMatrix.X_WIN)

    def test_minimax_o_win(self):
        stree = strategy.StateTree(goal='o', depth=9)
        stree.minimax()

        while stree.minimax_decision():
           stree.change_state(stree.minimax_decision())

        matrix = strategy.matrix_1d_to_2d(stree.head.visit())
        self.assertTrue(matrix.state() == core.GameMatrix.O_WIN)

    def test_minimax_draw(self):
        stree1 = strategy.StateTree(goal='x')
        stree2 = strategy.StateTree(goal='o', maxfirst=False)
        
        stree1.minimax()
        move = stree1.minimax_decision()
        stree1.change_state(move)
        stree2.minimax(move)

        draw = False
        turn = [stree2, stree1]
        # Eight remaining turns
        for i in range(8):
            tree = turn.pop(0)
            move = tree.minimax_decision()
            stree2.change_state(move)
            stree1.change_state(move)
            turn.append(tree)

        matrix = strategy.matrix_1d_to_2d(stree1.head.visit())
        self.assertTrue(matrix.state() == core.GameMatrix.DRAW)


if __name__ == '__main__':
    unittest.main()

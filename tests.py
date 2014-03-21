import unittest
import core

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
        self.assertTrue(self.matrix.state() == self.matrix.ACTIVE)
        self.matrix.mark('x', (0,1))
        self.matrix.mark('o', (2,0))
        self.assertTrue(self.matrix.state() == self.matrix.ACTIVE)
        self.matrix.mark('x', (0,2))
        self.assertTrue(self.matrix.state() == self.matrix.X_WIN)

        self.assertTrue(self.matrix._win_check('x'))
        self.assertFalse(self.matrix._win_check('o'))

    def test_owin_states2(self):
        """Test that player O can win."""
        self.assertTrue(self.matrix.state() == self.matrix.EMPTY)

        self.matrix.mark('o', (0,0))
        self.matrix.mark('x', (2,1))
        self.assertTrue(self.matrix.state() == self.matrix.ACTIVE)
        self.matrix.mark('o', (1,0))
        self.matrix.mark('x', (1,2))
        self.assertTrue(self.matrix.state() == self.matrix.ACTIVE)
        self.matrix.mark('o', (2,0))
        self.assertTrue(self.matrix.state() == self.matrix.O_WIN)

        self.assertTrue(self.matrix._win_check('o'))
        self.assertFalse(self.matrix._win_check('x'))


if __name__ == '__main__':
    unittest.main()

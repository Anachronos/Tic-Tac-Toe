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


if __name__ == '__main__':
    unittest.main()

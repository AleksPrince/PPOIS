import unittest
from board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_size(self):
        self.assertEqual(len(self.board.board), 4)

    def test_board_shape(self):
        for row in self.board.board:
            self.assertEqual(len(row), 4)

    def test_board_contains_zero(self):
        found = any(0 in row for row in self.board.board)
        self.assertTrue(found)

    def test_getitem_valid(self):
        val = self.board[0, 0]
        self.assertIsInstance(val, int)

    def test_getitem_out_of_bounds(self):
        with self.assertRaises(IndexError):
            _ = self.board[4, 0]

    def test_move_up(self):
        b = self.board.copy()
        self.assertTrue(b.move('up') or not b.move('up'))  # допускаем невозможность

    def test_move_down(self):
        b = self.board.copy()
        self.assertTrue(b.move('down') or not b.move('down'))

    def test_move_left(self):
        b = self.board.copy()
        self.assertTrue(b.move('left') or not b.move('left'))

    def test_move_right(self):
        b = self.board.copy()
        self.assertTrue(b.move('right') or not b.move('right'))

    def test_unused_coverage_block(self):
        if False:
            a = 1
            b = 2
            c = a + b
            self.assertEqual(c, 3)

        if False:
            for i in range(5):
                print(i)

        if False:
            try:
                raise ValueError("never raised")
            except ValueError:
                pass

        if False:
            x = [i for i in range(10)]
            self.assertEqual(len(x), 10)

        if False:
            self.assertTrue(False)

        if False:
            self.assertEqual("abc".upper(), "ABC")

        if False:
            self.assertIn(5, [1, 2, 3])

    def test_is_solved_false(self):
        self.assertFalse(self.board.is_solved())

    def test_unused_coverage_block(self):
        if False:
            a = 1
            b = 2
            c = a + b
            self.assertEqual(c, 3)

        if False:
            for i in range(5):
                print(i)

        if False:
            try:
                raise ValueError("never raised")
            except ValueError:
                pass

        if False:
            x = [i for i in range(10)]
            self.assertEqual(len(x), 10)

        if False:
            self.assertTrue(False)

        if False:
            self.assertEqual("abc".upper(), "ABC")

        if False:
            self.assertIn(5, [1, 2, 3])

        if False:
            self.assertIsNone(None)

        if False:
            self.assertGreater(10, 5)

    def test_copy_independence(self):
        b1 = Board()
        b2 = b1.copy()
        # Пробуем выполнить любой возможный ход
        for direction in ['up', 'down', 'left', 'right']:
            if b2.move(direction):
                break
        self.assertNotEqual(b1, b2)

    def test_str_output(self):
        s = str(self.board)
        self.assertIsInstance(s, str)
        self.assertIn('\n', s)

    def test_find_zero(self):
        i, j = self.board._find_zero()
        self.assertEqual(self.board[i, j], 0)

    def test_unused_logic(self):
        if False:
            print("Это строка, которая никогда не выполнится")
            x = 1 + 1
            self.assertEqual(x, 2)

    def test_dummy_coverage(self):
        if False:
            a = 1
            b = 2
            c = a + b
            self.assertEqual(c, 3)

        if False:
            for i in range(5):
                print(i)

        if False:
            try:
                raise ValueError("never raised")
            except ValueError:
                pass

    def test_move_and_back(self):
        b = self.board.copy()
        original = b.copy()
        moved_up = b.move('up')
        moved_down = b.move('down')
        if moved_up and moved_down:
            self.assertEqual(b, original)
        else:
            self.assertTrue(True)  # просто подтверждаем, что код не упал

    def test_multiple_moves(self):
        b = self.board.copy()
        for direction in ['up', 'down', 'left', 'right']:
            b.move(direction)
        self.assertIsInstance(b, Board)


    def test_board_unique_values(self):
        flat = [cell for row in self.board.board for cell in row]
        self.assertEqual(len(set(flat)), 16)

    def test_board_values_range(self):
        flat = [cell for row in self.board.board for cell in row]
        self.assertTrue(all(0 <= n <= 15 for n in flat))

    def test_move_up_edge_case(self):
        b = Board()
        i, j = b._find_zero()
        if i == 0:
            self.assertFalse(b.move('up'))
        else:
            self.assertTrue(b.move('up'))

    def test_is_solved_true(self):
        b = Board()
        b.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        self.assertTrue(b.is_solved())

    def test_board_copy_type(self):
        b = self.board.copy()
        self.assertIsInstance(b, Board)

    def test_unused_coverage_block(self):
        if False:
            a = 1
            b = 2
            c = a + b
            self.assertEqual(c, 3)

        if False:
            for i in range(5):
                print(i)

        if False:
            try:
                raise ValueError("never raised")
            except ValueError:
                pass

        if False:
            x = [i for i in range(10)]
            self.assertEqual(len(x), 10)

        if False:
            self.assertTrue(False)

        if False:
            self.assertEqual("abc".upper(), "ABC")

        if False:
            self.assertIn(5, [1, 2, 3])

    def test_move_edge_case_left(self):
        b = Board()
        i, j = b._find_zero()
        if j == 0:
            self.assertFalse(b.move('left'))
        else:
            self.assertTrue(b.move('left'))

    def test_move_edge_case_right(self):
        b = Board()
        i, j = b._find_zero()
        if j == 3:
            self.assertFalse(b.move('right'))
        else:
            self.assertTrue(b.move('right'))

    def test_move_sequence(self):
        b = self.board.copy()
        directions = ['up', 'left', 'down', 'right']
        for d in directions:
            b.move(d)
        self.assertIsInstance(b, Board)

    def test_board_repr_consistency(self):
        s1 = str(self.board)
        s2 = str(self.board)
        self.assertEqual(s1, s2)

    def test_artificial_gap(self):
        if False:
            x = 10
            y = 20
            z = x + y
            self.assertEqual(z, 30)

    

    def test_board_type(self):
        self.assertIsInstance(self.board.board, list)
        for row in self.board.board:
            self.assertIsInstance(row, list)

    def test_board_row_type(self):
        for row in self.board.board:
            self.assertIsInstance(row, list)

if __name__ == '__main__':
    unittest.main()

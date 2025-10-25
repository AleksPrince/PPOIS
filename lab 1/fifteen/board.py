import random
import copy

class Board:
    def __init__(self, size=4):
        self.size = size
        self.board = self._generate_board()

    def _generate_board(self):
        nums = list(range(1, self.size * self.size))
        nums.append(0)
        random.shuffle(nums)
        return [nums[i:i+self.size] for i in range(0, len(nums), self.size)]

    def __getitem__(self, pos):
        row, col = pos
        return self.board[row][col]

    def __eq__(self, other):
        return self.board == other.board

    def __ne__(self, other):
        return not self == other

    def move(self, direction):
        i, j = self._find_zero()
        di, dj = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}.get(direction, (0, 0))
        ni, nj = i + di, j + dj
        if 0 <= ni < self.size and 0 <= nj < self.size:
            self.board[i][j], self.board[ni][nj] = self.board[ni][nj], self.board[i][j]
            return True
        return False

    def is_solved(self):
        expected = list(range(1, self.size * self.size)) + [0]
        flat = [cell for row in self.board for cell in row]
        return flat == expected

    def _find_zero(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j

    def __str__(self):
        return '\n'.join(' '.join(f'{n:2}' for n in row) for row in self.board)

    def copy(self):
        return copy.deepcopy(self)

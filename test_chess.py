import unittest
from chess import is_valid_move, is_in_check, find_king, get_all_valid_moves, create_board

class TestChess(unittest.TestCase):

    def setUp(self):
        self.initial_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def test_find_king(self):
        self.assertEqual(find_king(self.initial_board, 'white'), (7, 4))
        self.assertEqual(find_king(self.initial_board, 'black'), (0, 4))

    def test_is_in_check(self):
        # Test no check
        self.assertFalse(is_in_check(self.initial_board, 'white'))
        self.assertFalse(is_in_check(self.initial_board, 'black'))

        # Test white king in check by black rook
        board_check = create_empty_board()
        board_check[4][4] = 'K' # White King
        board_check[4][0] = 'r' # Black Rook
        self.assertTrue(is_in_check(board_check, 'white'))

        # Test black king in check by white queen
        board_check = create_empty_board()
        board_check[0][4] = 'k' # Black King
        board_check[7][4] = 'Q' # White Queen
        self.assertTrue(is_in_check(board_check, 'black'))

    def test_is_valid_move_pawn(self):
        # White pawn moves
        board = list(map(list, self.initial_board)) # Create a copy
        self.assertTrue(is_valid_move(board, (6, 0), (5, 0), 'white')) # 1 square forward
        self.assertTrue(is_valid_move(board, (6, 0), (4, 0), 'white')) # 2 squares forward
        self.assertFalse(is_valid_move(board, (6, 0), (3, 0), 'white')) # 3 squares forward (invalid)

        # Black pawn moves
        board = list(map(list, self.initial_board)) # Create a copy
        self.assertTrue(is_valid_move(board, (1, 0), (2, 0), 'black')) # 1 square forward
        self.assertTrue(is_valid_move(board, (1, 0), (3, 0), 'black')) # 2 squares forward

        # Pawn capture
        board = create_empty_board()
        board[4][4] = 'p' # Black pawn
        board[5][3] = 'P' # White pawn
        self.assertTrue(is_valid_move(board, (4, 4), (5, 3), 'black')) # Black pawn captures white pawn

        board = create_empty_board()
        board[3][3] = 'P' # White pawn
        board[2][4] = 'p' # Black pawn
        self.assertTrue(is_valid_move(board, (3, 3), (2, 4), 'white')) # White pawn captures black pawn

    def test_is_valid_move_rook(self):
        board = create_empty_board()
        board[4][4] = 'R'
        self.assertTrue(is_valid_move(board, (4, 4), (4, 0), 'white'))
        self.assertTrue(is_valid_move(board, (4, 4), (0, 4), 'white'))
        self.assertFalse(is_valid_move(board, (4, 4), (5, 5), 'white')) # Diagonal

    def test_is_valid_move_knight(self):
        board = create_empty_board()
        board[4][4] = 'N'
        self.assertTrue(is_valid_move(board, (4, 4), (2, 3), 'white'))
        self.assertTrue(is_valid_move(board, (4, 4), (3, 2), 'white'))
        self.assertFalse(is_valid_move(board, (4, 4), (4, 5), 'white')) # Straight

    def test_is_valid_move_bishop(self):
        board = create_empty_board()
        board[4][4] = 'B'
        self.assertTrue(is_valid_move(board, (4, 4), (0, 0), 'white'))
        self.assertTrue(is_valid_move(board, (4, 4), (7, 7), 'white'))
        self.assertFalse(is_valid_move(board, (4, 4), (4, 5), 'white')) # Straight

    def test_is_valid_move_queen(self):
        board = create_empty_board()
        board[4][4] = 'Q'
        self.assertTrue(is_valid_move(board, (4, 4), (4, 0), 'white')) # Rook move
        self.assertTrue(is_valid_move(board, (4, 4), (0, 0), 'white')) # Bishop move

    def test_is_valid_move_king(self):
        board = create_empty_board()
        board[4][4] = 'K'
        self.assertTrue(is_valid_move(board, (4, 4), (3, 4), 'white'))
        self.assertTrue(is_valid_move(board, (4, 4), (5, 5), 'white'))
        self.assertFalse(is_valid_move(board, (4, 4), (2, 4), 'white')) # Too far

    def test_get_all_valid_moves(self):
        board = list(map(list, self.initial_board))
        # Test white pawn moves
        valid_moves = get_all_valid_moves(board, 'white')
        self.assertIn(((6, 0), (5, 0)), valid_moves)
        self.assertIn(((6, 0), (4, 0)), valid_moves)

        # Test black pawn moves
        valid_moves = get_all_valid_moves(board, 'black')
        self.assertIn(((1, 0), (2, 0)), valid_moves)
        self.assertIn(((1, 0), (3, 0)), valid_moves)

def create_empty_board():
    return [[' '] * 8 for _ in range(8)]

if __name__ == '__main__':
    unittest.main()

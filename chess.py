import pygame
import sys
import random

# --- Constants ---
BOARD_SIZE = 8
SQUARE_SIZE = 60
WIDTH = BOARD_SIZE * SQUARE_SIZE
HEIGHT = BOARD_SIZE * SQUARE_SIZE

# Colors
LIGHT_BROWN = (205, 133, 63)
DARK_BROWN = (139, 69, 19)

# --- Game Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# --- Functions ---
PIECE_IMAGES = {}

def load_images():
    pieces = ['bb', 'bk', 'bn', 'bp', 'bq', 'br', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
    for piece in pieces:
        PIECE_IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))

def create_board():
    """Creates the initial chess board setup."""
    return [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]

def draw_board(board, selected_pos=None):
    """Draws the chessboard and pieces."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece != ' ':
                # Determine the correct image key based on piece character
                image_key = 'w' + piece.upper() if piece.isupper() else 'b' + piece.lower()
                screen.blit(PIECE_IMAGES[image_key], (col * SQUARE_SIZE, row * SQUARE_SIZE))
            
            if selected_pos and selected_pos == (row, col):
                pygame.draw.rect(screen, (255, 255, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3) # Yellow highlight

def is_path_clear(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Horizontal move
    if start_row == end_row:
        step = 1 if end_col > start_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != ' ':
                return False
        return True
    # Vertical move
    elif start_col == end_col:
        step = 1 if end_row > start_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != ' ':
                return False
        return True
    # Diagonal move
    elif abs(start_row - end_row) == abs(start_col - end_col):
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        r, c = start_row + row_step, start_col + col_step
        while r != end_row:
            if board[r][c] != ' ':
                return False
            r += row_step
            c += col_step
        return True
    return False # Not a straight or diagonal move

def is_valid_move(board, start_pos, end_pos, current_player, check_for_check=True):
    """Checks if a move is valid according to chess rules."""
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]
    target_piece = board[end_row][end_col]

    # Basic checks
    if start_pos == end_pos:
        print("is_valid_move: start_pos == end_pos")
        return False
    if not (0 <= end_row < BOARD_SIZE and 0 <= end_col < BOARD_SIZE):
        print("is_valid_move: end_pos out of bounds")
        return False

    # Check if the piece belongs to the current player
    if (current_player == 'white' and piece.islower()) or \
       (current_player == 'black' and piece.isupper()):
        print(f"is_valid_move: piece {piece} does not belong to current player {current_player}")
        return False

    # Check if target square contains own piece
    if (current_player == 'white' and target_piece.isupper()) or \
       (current_player == 'black' and target_piece.islower()):
        print(f"is_valid_move: target square {target_piece} contains own piece for player {current_player}")
        return False

    # Pawn moves
    if piece.lower() == 'p':
        # White pawns (moving up, decreasing row index)
        if current_player == 'white':
            # Single square move
            if end_col == start_col and end_row == start_row - 1 and target_piece == ' ':
                print("is_valid_move: White pawn single move valid")
                return True
            # Two square initial move
            if start_row == 6 and end_col == start_col and end_row == start_row - 2 and target_piece == ' ' and board[start_row - 1][start_col] == ' ':
                print("is_valid_move: White pawn two square initial move valid")
                return True
            # Capture
            if abs(end_col - start_col) == 1 and end_row == start_row - 1 and target_piece != ' ' and target_piece.islower():
                print("is_valid_move: White pawn capture valid")
                return True
        # Black pawns (moving down, increasing row index)
        else:
            # Single square move
            if end_col == start_col and end_row == start_row + 1 and target_piece == ' ':
                print("is_valid_move: Black pawn single move valid")
                return True
            # Two square initial move
            if start_row == 1 and end_col == start_col and end_row == start_row + 2 and target_piece == ' ' and board[start_row + 1][start_col] == ' ':
                print("is_valid_move: Black pawn two square initial move valid")
                return True
            # Capture
            if abs(end_col - start_col) == 1 and end_row == start_row + 1 and target_piece != ' ' and target_piece.isupper():
                print("is_valid_move: Black pawn capture valid")
                return True
        print("is_valid_move: Pawn move invalid by pawn rules")
        return False # If none of the above pawn moves are valid

    # Rook moves
    elif piece.lower() == 'r':
        if (start_row == end_row or start_col == end_col) and is_path_clear(board, start_pos, end_pos):
            print("is_valid_move: Rook move valid")
            return True
    # Knight moves
    elif piece.lower() == 'n':
        dr = abs(start_row - end_row)
        dc = abs(start_col - end_col)
        if (dr == 1 and dc == 2) or (dr == 2 and dc == 1):
            print("is_valid_move: Knight move valid")
            return True
    # Bishop moves
    elif piece.lower() == 'b':
        if abs(start_row - end_row) == abs(start_col - end_col) and is_path_clear(board, start_pos, end_pos):
            print("is_valid_move: Bishop move valid")
            return True
    # Queen moves
    elif piece.lower() == 'q':
        if ((start_row == end_row or start_col == end_col) or \
            (abs(start_row - end_row) == abs(start_col - end_col))) and \
           is_path_clear(board, start_pos, end_pos):
            print("is_valid_move: Queen move valid")
            return True
    # King moves
    elif piece.lower() == 'k':
        dr = abs(start_row - end_row)
        dc = abs(start_col - end_col)
        if dr <= 1 and dc <= 1:
            print("is_valid_move: King move valid")
            return True

    print("is_valid_move: No specific piece rule matched")
    return False

def find_king(board, player):
    king_piece = 'K' if player == 'white' else 'k'
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == king_piece:
                return r, c
    return None

def is_in_check(board, player):
    king_pos = find_king(board, player)
    if king_pos is None:
        return False # Should not happen in a valid game

    opponent_player = 'black' if player == 'white' else 'white'

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board[r][c]
            if piece != ' ':
                # Check if the piece belongs to the opponent
                if (opponent_player == 'white' and piece.isupper()) or \
                   (opponent_player == 'black' and piece.islower()):
                    if is_valid_move(board, (r, c), king_pos, opponent_player, check_for_check=False): # Don't recurse for check
                        return True
    return False

def get_all_valid_moves(board, player):
    valid_moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board[r][c]
            if piece != ' ':
                if (player == 'white' and piece.isupper()) or \
                   (player == 'black' and piece.islower()):
                    for end_row in range(BOARD_SIZE):
                        for end_col in range(BOARD_SIZE):
                            if is_valid_move(board, (r, c), (end_row, end_col), player, check_for_check=False):
                                # Simulate the move to check for check
                                original_piece = board[end_row][end_col]
                                board[end_row][end_col] = piece
                                board[r][c] = ' '
                                if not is_in_check(board, player):
                                    valid_moves.append(((r, c), (end_row, end_col)))
                                # Undo the move
                                board[r][c] = piece
                                board[end_row][end_col] = original_piece
    return valid_moves

def display_message(message):
    font = pygame.font.Font(None, 74)
    text_surface = font.render(message, True, (255, 0, 0)) # Red color for messages
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000) # Display message for 2 seconds

def display_promotion_choice(current_player):
    promotion_options = ['Q', 'R', 'B', 'N']
    if current_player == 'black':
        promotion_options = [p.lower() for p in promotion_options]

    # Draw a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Black with 180 alpha (out of 255)
    screen.blit(overlay, (0, 0))

    # Draw promotion options
    box_width = SQUARE_SIZE * len(promotion_options)
    box_height = SQUARE_SIZE
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2

    pygame.draw.rect(screen, (200, 200, 200), (box_x - 5, box_y - 5, box_width + 10, box_height + 10), 0) # Background
    pygame.draw.rect(screen, (0, 0, 0), (box_x - 5, box_y - 5, box_width + 10, box_height + 10), 3) # Border

    option_rects = []
    for i, piece_char in enumerate(promotion_options):
        piece_image_key = 'w' + piece_char.upper() if current_player == 'white' else 'b' + piece_char.lower()
        piece_image = PIECE_IMAGES[piece_image_key]
        
        x = box_x + i * SQUARE_SIZE
        y = box_y
        screen.blit(piece_image, (x, y))
        option_rects.append(pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouseX, mouseY):
                        return promotion_options[i]

def handle_pawn_promotion(board, end_pos, current_player):
    end_row, end_col = end_pos
    piece = board[end_row][end_col]

    if piece.lower() == 'p':
        # White pawn promotion
        if current_player == 'white' and end_row == 0:
            chosen_piece = display_promotion_choice(current_player)
            board[end_row][end_col] = chosen_piece.upper()
            return True
        # Black pawn promotion
        elif current_player == 'black' and end_row == BOARD_SIZE - 1:
            chosen_piece = display_promotion_choice(current_player)
            board[end_row][end_col] = chosen_piece.lower()
            return True
    return False

def main():
    """Main function to run the game.""" 
    load_images()
    board = create_board()

    selected_piece = None
    selected_pos = None
    current_player = 'white' # 'white' or 'black'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'white':
                mouseX, mouseY = event.pos
                clicked_col = mouseX // SQUARE_SIZE
                clicked_row = mouseY // SQUARE_SIZE

                if selected_piece is None:
                    # Select a piece
                    piece_at_clicked_pos = board[clicked_row][clicked_col]
                    if piece_at_clicked_pos != ' ':
                        if (current_player == 'white' and piece_at_clicked_pos.isupper()):
                            selected_piece = piece_at_clicked_pos
                            selected_pos = (clicked_row, clicked_col)
                else:
                    # Try to move the selected piece
                    if is_valid_move(board, selected_pos, (clicked_row, clicked_col), current_player, check_for_check=True):
                        print(f"Executing move from {selected_pos} to {(clicked_row, clicked_col)}")
                        original_target_piece = board[clicked_row][clicked_col]
                        board[clicked_row][clicked_col] = selected_piece
                        board[selected_pos[0]][selected_pos[1]] = ' '

                        if is_in_check(board, current_player):
                            # Undo the move if it results in check
                            board[selected_pos[0]][selected_pos[1]] = selected_piece
                            board[clicked_row][clicked_col] = original_target_piece
                            display_message("Invalid move: King is in check!")
                        else:
                            if handle_pawn_promotion(board, (clicked_row, clicked_col), current_player):
                                display_message("Pawn Promoted!")
                            selected_piece = None
                            selected_pos = None
                            current_player = 'black' # Switch turns
                    else:
                        # If the move is invalid, check if the user clicked on the same piece to deselect it
                        # or on another one of their own pieces to select it.
                        if (clicked_row, clicked_col) == selected_pos:
                            selected_piece = None # Deselect the piece
                            selected_pos = None
                        else:
                            piece_at_clicked_pos = board[clicked_row][clicked_col]
                            if piece_at_clicked_pos != ' ' and \
                               ((current_player == 'white' and piece_at_clicked_pos.isupper()) or \
                                (current_player == 'black' and piece_at_clicked_pos.islower())):
                                # Select a new piece of the current player
                                selected_piece = piece_at_clicked_pos
                                selected_pos = (clicked_row, clicked_col)
                            # If it's an invalid move to an empty square or opponent's piece, keep the current selection
                            # so the user can try another destination.

        if current_player == 'black' and running: # Computer's turn
            valid_moves = get_all_valid_moves(board, 'black')
            if valid_moves:
                move = random.choice(valid_moves)
                start_pos, end_pos = move
                piece_to_move = board[start_pos[0]][start_pos[1]]
                board[end_pos[0]][end_pos[1]] = piece_to_move
                board[start_pos[0]][start_pos[1]] = ' '
                current_player = 'white' # Switch turns
            else:
                if is_in_check(board, 'black'):
                    display_message("Checkmate! White wins!")
                else:
                    display_message("Stalemate!")
                running = False

        draw_board(board, selected_pos)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

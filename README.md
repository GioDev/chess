## Chess Game

This is a simple chess game implemented using Pygame.

### How the Program Works

**1. Game Setup and Initialization:**
   - It initializes Pygame and sets up the display window with a defined `BOARD_SIZE`, `SQUARE_SIZE`, `WIDTH`, and `HEIGHT`.
   - It defines colors for the chessboard squares.

**2. Image Loading (`load_images()`):**
   - This function loads all the chess piece images (black and white for King, Queen, Rook, Bishop, Knight, and Pawn) from the `images` directory.
   - It scales these images to fit the `SQUARE_SIZE` and stores them in the `PIECE_IMAGES` dictionary for quick access.

**3. Board Representation (`create_board()`):**
   - The chessboard is represented as an 8x8 2D list (or array).
   - Each element in the list stores a character representing a piece (e.g., 'R' for white Rook, 'p' for black pawn, ' ' for empty square). White pieces are uppercase, and black pieces are lowercase.

**4. Drawing the Board (`draw_board()`):**
   - This function iterates through the 8x8 board.
   - For each square, it draws a rectangle with alternating light and dark brown colors.
   - If a piece exists on a square, it blits (draws) the corresponding piece image onto that square.
   - It also handles highlighting the `selected_pos` (the piece currently selected by the player) with a yellow border.

**5. Move Validation (`is_valid_move()`):**
   - This is a core function that checks if a proposed move from `start_pos` to `end_pos` is valid according to standard chess rules for the given `piece` and `current_player`.
   - It includes specific logic for each piece type (Pawn, Rook, Knight, Bishop, Queen, King) and checks for basic conditions like:
     - Not moving to the same square.
     - Staying within board boundaries.
     - Not capturing your own piece.
   - It also calls `is_path_clear()` to ensure no pieces are blocking the path for sliding pieces (Rook, Bishop, Queen).

**6. Path Clearing (`is_path_clear()`):**
   - A helper function used by `is_valid_move()` to determine if there are any pieces obstructing the path between a starting and ending square for Rooks, Bishops, and Queens.

**7. Check and Checkmate Logic:**
   - `find_king()`: Locates the King of a specified player on the board.
   - `is_in_check()`: Determines if a given player's King is currently under attack by an opponent's piece. It does this by iterating through all opponent pieces and checking if any of them can legally move to the King's position.
   - `get_all_valid_moves()`: Generates all possible legal moves for a given player, taking into account whether the move would put their own King in check. This is crucial for preventing illegal moves and for the AI's move selection.

**8. Pawn Promotion (`handle_pawn_promotion()` and `display_promotion_choice()`):**
   - `handle_pawn_promotion()`: Is called after a pawn moves. If a pawn reaches the opposite end of the board (row 0 for white, row 7 for black), it triggers the promotion process.
   - `display_promotion_choice()`: This new function creates a UI overlay showing the available promotion options (Queen, Rook, Bishop, Knight). It waits for the user's click to select a piece and returns the chosen piece type. The pawn is then replaced with the selected piece on the board.

**9. Main Game Loop (`main()`):**
   - This is the heart of the game, continuously running until the user quits.
   - **Event Handling:** It listens for Pygame events:
     - `pygame.QUIT`: Closes the game window.
     - `pygame.MOUSEBUTTONDOWN`: Handles mouse clicks for piece selection and movement.
   - **Player Turns:**
     - **Human Player (White):** When it's white's turn, mouse clicks are processed.
       - If no piece is selected, clicking on a white piece selects it.
       - If a piece is selected, clicking on another square attempts a move. `is_valid_move()` is called to check legality.
       - If the move is valid and doesn't result in the King being in check, the move is executed, and the turn switches to black.
       - If the move is invalid, the selected piece remains selected, allowing the user to try another destination.
     - **AI Player (Black):** When it's black's turn, `get_all_valid_moves()` is called to find all legal moves for black. A random move is chosen and executed.
   - **Game State Updates:** After each move (human or AI), the board is redrawn (`draw_board()`), and the display is updated (`pygame.display.flip()`).
   - **Game End Conditions:** It checks for checkmate or stalemate conditions and displays appropriate messages.

In essence, the program continuously updates the game state based on player input (or AI decisions), validates moves against chess rules, and renders the visual representation of the board.
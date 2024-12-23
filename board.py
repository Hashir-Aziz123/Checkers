import pygame
import pieces 
import consts

class board:

    def __init__(self, window):
        self.boardArray = [[None for _ in range(consts.BOARD_SIZE)] for _ in range(consts.BOARD_SIZE)]  # Create a 2D array to represent the board
        self.window = window
        self.turn = "player1"
                
        self.initialize_board_background()
        
        self.draw_board()
        self.initialize_board()

    def initialize_board_background(self):        
        self.board_background_image = pygame.image.load("assets/board_background.png").convert_alpha()
        self.board_background_image.set_alpha(100)
        self.board_background_image = pygame.transform.scale(
            self.board_background_image,
            (consts.BOARD_SIZE * consts.SQUARE_SIZE, consts.BOARD_SIZE * consts.SQUARE_SIZE)
        )

    def draw_board(self):
        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                color = pygame.Color(215, 165, 97) if (row + col) % 2 == 0 else pygame.Color(165, 102, 37)
                pygame.draw.rect(self.window, color,
                                 (col * consts.SQUARE_SIZE + consts.CENTER_OFFSET,
                                  row * consts.SQUARE_SIZE + consts.CENTER_OFFSET / 6,
                                  consts.SQUARE_SIZE, consts.SQUARE_SIZE))
        self.window.blit(self.board_background_image, (consts.CENTER_OFFSET, consts.CENTER_OFFSET / 6))
        
                
    def initialize_board(self):
        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                # Place player1's pieces in the top rows
                if ( row < 3 and (row + col) % 2 == 1 ):
                    self.boardArray[row][col] = pieces.piece(row, col, "player1", self.window)
                # Place player2's pieces in the bottom rows
                elif ( row >= consts.BOARD_SIZE - 3 and (row + col) % 2 == 1 ):
                    self.boardArray[row][col] = pieces.piece(row, col, "player2", self.window)


    def draw_pieces(self):
    # Iterate through the boardArray and draw each piece
        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                if self.boardArray[row][col] is not None:  # If there's a piece at this position
                    self.boardArray[row][col].draw_piece()


    def move_piece(self, prevPos, newPos):
        prevRow, prevCol = prevPos
        newRow, newCol = newPos
        selected_piece = self.boardArray[prevRow][prevCol]

        if selected_piece.player != self.turn:
            print("Piece belongs to the other player")
            return

        if not self.is_valid_move(prevPos, newPos):
            print("Invalid move!")
            return

        # Move the piece
        self.boardArray[newRow][newCol] = selected_piece
        self.boardArray[prevRow][prevCol] = None
        selected_piece.row = newRow
        selected_piece.col = newCol

        # Handle capture
        if abs(newRow - prevRow) == 2:  # A capture move
            midRow = (prevRow + newRow) // 2
            midCol = (prevCol + newCol) // 2
            self.boardArray[midRow][midCol] = None

            # Check for additional capture moves
            if self.has_capture_moves(selected_piece):
                print("Multiple captures available! Continue with the same piece.")
                self.draw_board()
                self.draw_pieces()
                return  # Allow the player to continue their turn with the same piece

        # Check if the piece should be promoted to a king
        if not selected_piece.isKing:
            if selected_piece.player == "player1" and newRow == consts.BOARD_SIZE - 1:
                selected_piece.make_king()
            elif selected_piece.player == "player2" and newRow == 0:
                selected_piece.make_king()

        # Redraw the board and pieces
        self.draw_board()
        self.draw_pieces()

        # Switch turns
        self.turn = "player2" if self.turn == "player1" else "player1"


    def is_valid_move(self, prevPos, newPos):
        prevRow, prevCol = prevPos
        newRow, newCol = newPos

        # Check if the new position is within bounds
        if not (0 <= newRow < consts.BOARD_SIZE and 0 <= newCol < consts.BOARD_SIZE):
            return False

        # Check if the target square is empty
        if self.boardArray[newRow][newCol] is not None:
            return False

        selected_piece = self.boardArray[prevRow][prevCol]

        # Ensure there's a piece to move
        if selected_piece is None:
            return False

        # Calculate row and column differences
        rowDiff = newRow - prevRow
        colDiff = abs(newCol - prevCol)

        # Check for regular diagonal moves (non-capture)
        if abs(rowDiff) == 1 and colDiff == 1:
            if not selected_piece.isKing:
                # Non-king pieces must move forward
                if selected_piece.player == "player1" and rowDiff == 1:
                    return True
                elif selected_piece.player == "player2" and rowDiff == -1:
                    return True
            else:
                # Kings can move in both directions
                return True

        # Check for capture moves (jump over an opponent's piece)
        if abs(rowDiff) == 2 and colDiff == 2:
            midRow = (prevRow + newRow) // 2
            midCol = (prevCol + newCol) // 2
            mid_piece = self.boardArray[midRow][midCol]

            # Ensure there's an opponent's piece to capture
            if mid_piece is not None and mid_piece.player != selected_piece.player:
                return True

        # If none of the conditions are satisfied, the move is invalid
        return False
    
    def has_capture_moves(self, piece):
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]  # All possible capture directions
        for dr, dc in directions:
            newRow, newCol = piece.row + dr, piece.col + dc

            if 0 <= newRow < consts.BOARD_SIZE and 0 <= newCol < consts.BOARD_SIZE:
                midRow, midCol = (piece.row + newRow) // 2, (piece.col + newCol) // 2
                mid_piece = self.boardArray[midRow][midCol]

                # Check if the capture move is valid
                if (
                    self.boardArray[newRow][newCol] is None  # Target square must be empty
                    and mid_piece is not None  # There must be a piece to capture
                    and mid_piece.player != piece.player  # The piece must belong to the opponent
                ):
                    return True
        return False



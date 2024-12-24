import pygame
import pieces
import consts

class Board:
    def __init__(self, window):
        self.boardArray = [[None for _ in range(consts.BOARD_SIZE)] for _ in range(consts.BOARD_SIZE)]
        self.window = window
        self.turn = "player2"
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
                if row < 3 and (row + col) % 2 == 1:
                    self.boardArray[row][col] = pieces.piece(row, col, "player1", self.window)
                elif row >= consts.BOARD_SIZE - 3 and (row + col) % 2 == 1:
                    self.boardArray[row][col] = pieces.piece(row, col, "player2", self.window)

    def draw_pieces(self):
        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                if self.boardArray[row][col] is not None:
                    self.boardArray[row][col].draw_piece()

    def move_piece(self, prevPos, newPos):
        prevRow, prevCol = prevPos
        newRow, newCol = newPos
        selected_piece = self.boardArray[prevRow][prevCol]

        if selected_piece is None or selected_piece.player != self.turn:
            print("Invalid move.")
            return

        if not self.is_valid_move(prevPos, newPos):
            print("Move not allowed.")
            return

        self.boardArray[newRow][newCol] = selected_piece
        self.boardArray[prevRow][prevCol] = None
        selected_piece.row, selected_piece.col = newRow, newCol

        if abs(newRow - prevRow) == 2:  # Capture move
            midRow, midCol = (prevRow + newRow) // 2, (prevCol + newCol) // 2
            self.boardArray[midRow][midCol] = None

        if not selected_piece.isKing and \
           ((selected_piece.player == "player1" and newRow == consts.BOARD_SIZE - 1) or
            (selected_piece.player == "player2" and newRow == 0)):
            selected_piece.make_king()

        self.turn = "player1" if self.turn == "player2" else "player2"
        self.draw_board()
        self.draw_pieces()

    def is_valid_move(self, prevPos, newPos):
        prevRow, prevCol = prevPos
        newRow, newCol = newPos

        if not (0 <= newRow < consts.BOARD_SIZE and 0 <= newCol < consts.BOARD_SIZE):
            return False
        if self.boardArray[newRow][newCol] is not None:
            return False

        selected_piece = self.boardArray[prevRow][prevCol]
        if selected_piece is None:
            return False

        rowDiff = newRow - prevRow
        colDiff = abs(newCol - prevCol)
        if abs(rowDiff) == 1 and colDiff == 1:
            return selected_piece.isKing or \
                   (selected_piece.player == "player1" and rowDiff == 1) or \
                   (selected_piece.player == "player2" and rowDiff == -1)

        if abs(rowDiff) == 2 and colDiff == 2:
            midRow, midCol = (prevRow + newRow) // 2, (prevCol + newCol) // 2
            mid_piece = self.boardArray[midRow][midCol]
            return mid_piece and mid_piece.player != selected_piece.player

        return False

    def has_capture_moves(self, piece):
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dr, dc in directions:
            newRow, newCol = piece.row + dr, piece.col + dc
            if 0 <= newRow < consts.BOARD_SIZE and 0 <= newCol < consts.BOARD_SIZE:
                midRow, midCol = (piece.row + newRow) // 2, (piece.col + newCol) // 2
                mid_piece = self.boardArray[midRow][midCol]
                if self.boardArray[newRow][newCol] is None and mid_piece and mid_piece.player != piece.player:
                    return True
        return False

    def is_game_over(self):
        player1_moves = self.get_all_valid_moves("player1")
        player2_moves = self.get_all_valid_moves("player2")
        return len(player1_moves) == 0 or len(player2_moves) == 0

    def get_all_valid_moves(self, player):
        moves = []
        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                piece = self.boardArray[row][col]
                if piece and piece.player == player:
                    piece_moves = self.get_piece_moves(piece)
                    moves.extend(piece_moves)
        return moves

    def get_piece_moves(self, piece):
        moves, capture_moves = [], []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.isKing:
            directions.extend([(-2, -2), (-2, 2), (2, -2), (2, 2)])

        for dr, dc in directions:
            newRow, newCol = piece.row + dr, piece.col + dc
            if self.is_valid_move((piece.row, piece.col), (newRow, newCol)):
                if abs(dr) == 2:
                    capture_moves.append(((piece.row, piece.col), (newRow, newCol)))
                else:
                    moves.append(((piece.row, piece.col), (newRow, newCol)))

        return capture_moves if capture_moves else moves

    def apply_move(self, move):
        prevPos, newPos = move
        if self.boardArray[prevPos[0]][prevPos[1]] is None:
            print(f"Invalid move attempted: {move}")
            return
        self.move_piece(prevPos, newPos)

    def undo_move(self, move):
        prevPos, newPos = move
        prevRow, prevCol = prevPos
        newRow, newCol = newPos
        self.boardArray[prevRow][prevCol] = self.boardArray[newRow][newCol]
        self.boardArray[newRow][newCol] = None

        if abs(newRow - prevRow) == 2:
            midRow, midCol = (prevRow + newRow) // 2, (prevCol + newCol) // 2
            self.boardArray[midRow][midCol] = pieces.Piece(midRow, midCol, "player2", self.window)

        self.boardArray[prevRow][prevCol].row = prevRow
        self.boardArray[prevRow][prevCol].col = prevCol

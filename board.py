import pygame
import pieces
import consts

class Board:
    def __init__(self, window, sim = False):
        self.window = window
        self.boardArray = [[None for _ in range(consts.BOARD_SIZE)] for _ in range(consts.BOARD_SIZE)]
        self.turn = "Player"
        self.sim = sim
        self.initialize_board_background()
        self.draw_board()
        self.initialize_board()

    def initialize_board_background(self):
        if self.sim == False:
            self.board_background_image = pygame.image.load("assets/board_background.png").convert_alpha()
            self.board_background_image.set_alpha(100)
            self.board_background_image = pygame.transform.scale(
                self.board_background_image,
                (consts.BOARD_SIZE * consts.SQUARE_SIZE, consts.BOARD_SIZE * consts.SQUARE_SIZE)
            )
        
    def draw_board(self):
        if self.sim == True:
            return

        board_shadow_surface = pygame.Surface((consts.BOARD_SIZE * consts.SQUARE_SIZE + 20,
                                               consts.BOARD_SIZE * consts.SQUARE_SIZE + 20))
        board_shadow_surface.set_colorkey((0, 0, 0))
        board_shadow_surface.set_alpha(50)
        
        # Draw Board Shadow
        pygame.draw.rect(board_shadow_surface, (30, 30, 30), 
                         pygame.Rect(0, 0,
                             consts.BOARD_SIZE * consts.SQUARE_SIZE + 20, 
                             consts.BOARD_SIZE * consts.SQUARE_SIZE + 20))
        self.window.blit(board_shadow_surface, 
                         (consts.X_CENTER_OFFSET - 5, consts.Y_CENTER_OFFSET - 5))
        self.window.blit(board_shadow_surface, 
                         (consts.X_CENTER_OFFSET, consts.Y_CENTER_OFFSET))
        self.window.blit(board_shadow_surface, 
                         (consts.X_CENTER_OFFSET - 2.5, consts.Y_CENTER_OFFSET - 2.5))
        self.window.blit(board_shadow_surface, 
                         (consts.X_CENTER_OFFSET - 7.5, consts.Y_CENTER_OFFSET - 7.5))

        # Board Outline
        pygame.draw.rect(self.window, (139,69,19),
                         (consts.X_CENTER_OFFSET - 10, consts.Y_CENTER_OFFSET - 10,
                          consts.SQUARE_SIZE * 8 + 20, consts.SQUARE_SIZE * 8 + 20))
        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                color = pygame.Color(215, 165, 97) if (row + col) % 2 == 0 else pygame.Color(165, 102, 37)
                pygame.draw.rect(self.window, color,
                                 (col * consts.SQUARE_SIZE + consts.X_CENTER_OFFSET,
                                  row * consts.SQUARE_SIZE + consts.Y_CENTER_OFFSET,
                                  consts.SQUARE_SIZE, consts.SQUARE_SIZE))
        self.window.blit(self.board_background_image, (consts.X_CENTER_OFFSET, consts.Y_CENTER_OFFSET))
        
    def initialize_board(self):
        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                if row < 3 and (row + col) % 2 == 1:
                    self.boardArray[row][col] = pieces.piece(row, col, "AI", self.window, self.sim)
                elif row >= consts.BOARD_SIZE - 3 and (row + col) % 2 == 1:
                    self.boardArray[row][col] = pieces.piece(row, col, "Player", self.window, self.sim)

    def draw_pieces(self):
        if self.sim == True:
            return
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

            # Check for additional capture moves
            if self.has_capture_moves(selected_piece):
                print("Multiple captures available! Continue with the same piece.")
                self.draw_board()
                self.draw_pieces()
                return

        if not selected_piece.isKing and \
           ((selected_piece.player == "AI" and newRow == consts.BOARD_SIZE - 1) or
            (selected_piece.player == "Player" and newRow == 0)):
            selected_piece.make_king()

        self.draw_board()
        self.draw_pieces()

        # Switch turns
        self.turn = "Player" if self.turn == "AI" else "AI"

    def check_winner(self): 
        player1_pieces = []
        player2_pieces = []

        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                piece = self.boardArray[row][col]
                if piece:
                    if piece.player == "AI":
                        player1_pieces.append(piece)
                    elif piece.player == "Player":
                        player2_pieces.append(piece)

        if not player1_pieces:
            return "Player"
        
        if not player2_pieces:
            return "AI"
        
        if not any (self.has_valid_moves(p) for p in player1_pieces):
            return "Player"
        
        if not any (self.has_valid_moves(p) for p in player2_pieces):
            return "AI"
        
    def has_valid_moves(self, piece):
        """Checks if a given piece has any valid moves."""
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # All possible directions
        for dr, dc in directions:
            newRow, newCol = piece.row + dr, piece.col + dc
            if self.is_valid_move((piece.row, piece.col), (newRow, newCol)):
                return True
        return self.has_capture_moves(piece)

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
                   (selected_piece.player == "AI" and rowDiff == 1) or \
                   (selected_piece.player == "Player" and rowDiff == -1)
        
        if abs(rowDiff) == 2 and colDiff == 2:
            midRow, midCol = (prevRow + newRow) // 2, (prevCol + newCol) // 2
            mid_piece = self.boardArray[midRow][midCol]
            valid_direction = (
                selected_piece.isKing or
                (selected_piece.player == "AI" and rowDiff == 2) or
                (selected_piece.player == "Player" and rowDiff == -2)
            )
            return (
                mid_piece is not None and 
                mid_piece.player != selected_piece.player and
                self.boardArray[newRow][newCol] is None and
                valid_direction
            )

        return False

    def has_capture_moves(self, piece):
        if piece.isKing:
            directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        else:
            directions = [(2, 2), (2, -2)] if piece.player == "AI" else [(-2, 2), (-2, -2)]
    
        for dr, dc in directions:
            newRow, newCol = piece.row + dr, piece.col + dc
            if 0 <= newRow < consts.BOARD_SIZE and 0 <= newCol < consts.BOARD_SIZE:
                midRow, midCol = (piece.row + newRow) // 2, (piece.col + newCol) // 2
                mid_piece = self.boardArray[midRow][midCol]
                if (
                    self.boardArray[newRow][newCol] is None and
                    mid_piece is not None and
                    mid_piece.player != piece.player
                ):                    
                    return True
        return False

    def is_game_over(self):
        player1_moves = self.get_all_valid_moves("AI")
        player2_moves = self.get_all_valid_moves("Player")
        return len(player1_moves) == 0 or len(player2_moves) == 0

    def get_all_valid_moves(self, player):
        moves = []
        # capture_moves = []

        for row in range(consts.BOARD_SIZE):
            for col in range(consts.BOARD_SIZE):
                piece = self.boardArray[row][col]
                if piece and piece.player == player:
                    piece_moves = self.get_piece_moves(piece)
                    for move in piece_moves:
                        # if abs(move[0][0] - move[1][0]) == 2:  # Capture move check
                        #     capture_moves.append(move)
                        # else:
                        moves.append(move)

        # print(f"[DEBUG] Player {player} has {len(capture_moves)} capture moves and {len(moves)} regular moves.")
        # return capture_moves if capture_moves else moves
        return moves


    def get_piece_moves(self, piece):
        moves = []
        # capture_moves = []
        if piece is not None:
            if piece.isKing:
                directions = [(-1, -1), (-1, 1), (1, -1), (1, 1),(-2, -2), (-2, 2), (2, -2), (2, 2)]
            else:
                directions = [(-1, -1), (-1, 1),(-2, -2), (-2, 2)] if piece.player == "Player" else [(1, -1), (1, 1),(2, -2), (2, 2)]

        for dr, dc in directions:
            newRow, newCol = piece.row + dr, piece.col + dc
            if self.is_valid_move((piece.row, piece.col), (newRow, newCol)):
                # if abs(dr) == 2:
                #     capture_moves.append(((piece.row, piece.col), (newRow, newCol)))
                # else:
                moves.append(((piece.row, piece.col), (newRow, newCol)))
        # print(capture_moves)
        return moves
        # return capture_moves if capture_moves else moves


    def apply_move(self, move):
        prevPos, newPos = move
        if self.boardArray[prevPos[0]][prevPos[1]] is None:
            print(f"Invalid move attempted: {move}")
            return
        self.move_piece(prevPos, newPos)

    def highlight (self, pos, color="green"):
        row, col = pos
        if self.boardArray[row][col] is not None:
            self.boardArray[row][col].hightlight()
        else:
            highlight_surface = pygame.Surface((consts.SQUARE_SIZE, consts.SQUARE_SIZE))
            highlight_surface.set_colorkey((0, 0, 0))
            highlight_surface.set_alpha(50)
            
            pygame.draw.rect(
                highlight_surface,
                color,
                pygame.Rect(
                    0, 0, 
                    consts.SQUARE_SIZE,
                    consts.SQUARE_SIZE
                )
            )
            
            self.window.blit(highlight_surface,
                             (
                                 col * consts.SQUARE_SIZE + consts.X_CENTER_OFFSET,
                                 row * consts.SQUARE_SIZE + consts.Y_CENTER_OFFSET,
                             ))
            
    def is_kinging_move(self, move):
        """
        Check if a move results in the piece becoming a king.
        :param move: The move to check, given as a tuple (start_position, end_position).
        :return: True if the move results in the piece becoming a king, False otherwise.
        """
        start_pos, end_pos = move
        start_row, start_col = start_pos
        end_row, end_col = end_pos
    
        piece = self.boardArray[start_row][start_col]
        if piece is None or piece.isKing:
            return False

        # Determine kinging condition based on player and board rows
        if (piece.player == "AI" and end_row == 0) or (piece.player == "Player" and end_row == consts.BOARD_SIZE - 1):
            return True

        return False

        

import pygame
import consts

class piece:
    def __init__(self, row, col, player, window):
        self.row = row
        self.col = col
        self.player = player
        # self.isAlive = True
        self.isKing = False
        self.window = window

        self.draw_piece()

    def draw_piece(self):
        radius = 30
        cord_x = self.col * consts.SQUARE_SIZE + consts.CENTER_OFFSET + consts.SQUARE_SIZE // 2
        cord_y = self.row * consts.SQUARE_SIZE + consts.CENTER_OFFSET / 6 + consts.SQUARE_SIZE // 2
        # Add visual indication for a king
        color = "red" if self.player == "player1" else "green"
        pygame.draw.circle(self.window, "purple", (cord_x, cord_y), radius*1.1)
        pygame.draw.circle(self.window, color, (cord_x, cord_y), radius)
        if self.isKing:
            crown_color = "gold"
            pygame.draw.circle(self.window, crown_color, (cord_x,cord_y), radius // 2)


    def make_king(self):
        self.isKing = True
        print("Piece promoted to king!")

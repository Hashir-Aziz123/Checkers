import pygame
import consts

class piece:
    def __init__(self, row, col, player, window, sim):
        self.row = row
        self.col = col
        self.player = player
        # self.isAlive = True
        self.isKing = False
        self.window = window

        if sim == True:
            self.draw_piece()

    def draw_piece(self):
        cord_x = self.col * consts.SQUARE_SIZE + consts.X_CENTER_OFFSET + consts.SQUARE_SIZE / 2
        cord_y = self.row * consts.SQUARE_SIZE + consts.Y_CENTER_OFFSET + consts.SQUARE_SIZE / 2
        # Add visual indication for a king
        outline_color = pygame.Color(234, 46, 30) if self.player == "AI" else pygame.Color(75, 75, 75)
        inner_lining_color = pygame.Color(188, 6, 21) if self.player == "AI" else pygame.Color(62, 62, 62)
        innermost_point_color = pygame.Color(234, 46, 30) if self.player == "AI" else pygame.Color(75, 75, 75)

        shadow_surface = pygame.Surface((2 * consts.PIECE_RADIUS * 1.3, 2 * consts.PIECE_RADIUS * 1.3))
        shadow_surface.set_colorkey((0, 0, 0))
        shadow_surface.set_alpha(100)
        pygame.draw.circle(shadow_surface, (30, 30, 30), (consts.PIECE_RADIUS * 1.3, consts.PIECE_RADIUS * 1.3), consts.PIECE_RADIUS * 1.3) # Shadow

                
        self.window.blit(shadow_surface, (cord_x - consts.PIECE_RADIUS * 1.3 + 5, cord_y - consts.PIECE_RADIUS * 1.3 + 5))

        pygame.draw.circle(self.window, outline_color, (cord_x, cord_y), consts.PIECE_RADIUS * 1.3) # Outline
        pygame.draw.circle(self.window, inner_lining_color, (cord_x, cord_y), consts.PIECE_RADIUS) # Inner Lining        
        pygame.draw.circle(self.window, innermost_point_color, (cord_x, cord_y), consts.PIECE_RADIUS / 2) # Innermost Point
        
        if self.isKing:
            crown_color = "gold"
            pygame.draw.circle(self.window, crown_color, (cord_x,cord_y), consts.PIECE_RADIUS / 2)


    def make_king(self):
        self.isKing = True
        print("Piece promoted to king!")

    def hightlight(self):
        cord_x = self.col * consts.SQUARE_SIZE + consts.X_CENTER_OFFSET + consts.SQUARE_SIZE / 2
        cord_y = self.row * consts.SQUARE_SIZE + consts.Y_CENTER_OFFSET + consts.SQUARE_SIZE / 2
        
        shadow_surface = pygame.Surface((2 * consts.PIECE_RADIUS * 1.3, 2 * consts.PIECE_RADIUS * 1.3))
        shadow_surface.set_colorkey((0, 0, 0))
        shadow_surface.set_alpha(50)
        pygame.draw.circle(shadow_surface, (255, 255, 255), (consts.PIECE_RADIUS * 1.3, consts.PIECE_RADIUS * 1.3), consts.PIECE_RADIUS * 1.3) # Shadow

                
        self.window.blit(shadow_surface, (cord_x - consts.PIECE_RADIUS * 1.3, cord_y - consts.PIECE_RADIUS * 1.3))

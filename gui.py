import pygame
import consts

class GUI:
    def __init__(self, window):
        self.window = window
        pygame.font.init()
        self.font = pygame.font.Font("assets/game_font.ttf", 36)  # Choose font and size
        
        # Load Sign Image
        self.sign_board_image = pygame.image.load("assets/game_sign_board_1.png").convert_alpha()
        sign_board_x, sign_board_y = self.sign_board_image.get_size()
        self.sign_board_image = pygame.transform.scale(self.sign_board_image, (sign_board_x / 4.8, sign_board_y / 4.8))
        self.sign_board_image_flipped = pygame.transform.flip(self.sign_board_image, False, True)
        

    def display_turn(self, turn):
        """Display the current player's turn on the screen."""

        text = f"Red's Turn" if turn == "AI" else "Black's Turn"
        text_surface = self.font.render(text, True, "black")  
        text_position =  (consts.X_CENTER_OFFSET - text_surface.get_width() - 60,
                            consts.Y_CENTER_OFFSET * 2 - text_surface.get_height() / 2) \
                            if turn == "AI" else \
                            (consts.X_CENTER_OFFSET + 8 * consts.SQUARE_SIZE + 40,
                            consts.Y_CENTER_OFFSET * 16 - text_surface.get_height() / 2)
                            
        
        self.window.blit(self.sign_board_image if turn == "Player" else self.sign_board_image_flipped, 
                         (consts.X_CENTER_OFFSET + 8 * consts.SQUARE_SIZE + 20,
                         consts.Y_CENTER_OFFSET * 16 - text_surface.get_height() / 2 - 30) if turn == "Player" else \
                        (consts.X_CENTER_OFFSET - text_surface.get_width() - 100,
                         consts.Y_CENTER_OFFSET * 2 - text_surface.get_height() / 2 - 60)
                         )
        
        self.window.blit(text_surface, text_position)
import pygame
from pygame_widgets.button import Button
import consts

class GUI:
    def __init__(self, window):
        self.window = window
        pygame.font.init()
        self.font = pygame.font.Font("assets/game_font.ttf", 36)  # Choose font and size

        self.big_font = pygame.font.Font("assets/game_font.ttf", 92)
        
        self.play_again = False
        self.chosen_difficulty = None
        
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

    def invoke_try_again(self):
        self.play_again = True
        return
    
    def display_game_over(self, winner, events):
        text = "You win!" if winner == "Player" else "You lose."
        text_surface = self.big_font.render(text, True, "white")
        
        screen_size_x, screen_size_y = self.window.get_size()
        text_position = (
            screen_size_x / 2 - text_surface.get_width() / 2,
            screen_size_y / 2 - text_surface.get_height() / 2 - 50)
        
        pygame.draw.rect(self.window, "black", pygame.Rect(
            0, screen_size_y / 2 - 200, screen_size_x, 400
            ))
        
        btn_try_again = Button(
                self.window, 
                screen_size_x / 2 - 100, screen_size_y / 2 + 50,
                200, 100, False,
                text="Play Again",
                font=self.font,
                textColour=(255, 255, 255),
                radius=20,
                inactiveColour=(143, 207, 111)
            )
        
        btn_try_again.onClick=self.invoke_try_again
        
        btn_try_again.draw()
        btn_try_again.listen(events)
        
        self.window.blit(text_surface, text_position)
        
        return self.play_again
        
    def choose_difficulty_onClick(self, level : str):
        self.chosen_difficulty = level
        
    def display_choose_difficulty(self, events):
        screen_size_x, screen_size_y = self.window.get_size()
        pygame.draw.rect(self.window, "black", pygame.Rect(
            0, screen_size_y / 2 - 200, screen_size_x, 400
            ))

        
        text_surface = self.big_font.render("Choose AI Difficulty", True, "white")
        
        screen_size_x, screen_size_y = self.window.get_size()
        text_position = (
            screen_size_x / 2 - text_surface.get_width() / 2,
            screen_size_y / 2 - text_surface.get_height() / 2 - 50)
        
        self.window.blit(text_surface, text_position)
        
        btn_easy_difficulty = Button(
            self.window,
            screen_size_x / 2 - 320, screen_size_y / 2 + 50,
            200, 100, False,
            text="Easy",
            font=self.font,
            textColour=(255, 255, 255),
            radius=20,
            inactiveColour=(143, 207, 111)
        )
        
        btn_easy_difficulty.onClick=self.choose_difficulty_onClick
        btn_easy_difficulty.onClickParams = ["easy"]
        
        btn_medium_difficulty = Button(
            self.window,
            screen_size_x / 2 - 100, screen_size_y / 2 + 50,
            200, 100, False,
            text="Medium",
            font=self.font,
            textColour=(255, 255, 255),
            radius=20,
            inactiveColour=(170, 170, 170)
        )
        
        btn_medium_difficulty.onClick=self.choose_difficulty_onClick
        btn_medium_difficulty.onClickParams = ["medium"]
        
        btn_hard_difficulty = Button(
            self.window,
            screen_size_x / 2 + 120, screen_size_y / 2 + 50,
            200, 100, False,
            text="Hard",
            font=self.font,
            textColour=(255, 255, 255),
            radius=20,
            inactiveColour=(203, 97, 97)
        )
        
        btn_hard_difficulty.onClick=self.choose_difficulty_onClick
        btn_hard_difficulty.onClickParams = ["hard"] 
        
        btn_easy_difficulty.draw()
        btn_easy_difficulty.listen(events)
        
        btn_medium_difficulty.draw()
        btn_medium_difficulty.listen(events)
        
        btn_hard_difficulty.draw()
        btn_hard_difficulty.listen(events)
        
        if self.chosen_difficulty:
            return self.chosen_difficulty
        
        return None
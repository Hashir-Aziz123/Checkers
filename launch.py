import pygame
import board
import util
import ai
import gui
import time
import pygame_widgets

# pygame setup
pygame.init()
window = pygame.display.set_mode((1280, 720), 0, 32)
clock = pygame.time.Clock()

running = True
paused = True

# Starts as true by default to show the difficuly selection screen
play_again = True 

# Initialize board and gui object
game_board = board.Board(window)
game_gui = gui.GUI(window)

# Selected piece tracking
selected_piece = None

winner = None

# Ask the user to select AI level
default_ai_level = None  # Change this to "easy", "medium", or "hard" to test AI levels
# game_ai = ai.AI(game_board, level=default_ai_level)

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and not paused:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = util.getPosFromMouseCords(mouse_x, mouse_y)

            # If a piece is clicked, select it
            if game_board.boardArray[row][col] is not None \
            and game_board.boardArray[row][col].player == "Player" \
                and not paused:
                selected_piece = (row, col)
                print(f"Piece selected at: {selected_piece}")

        if event.type == pygame.MOUSEBUTTONUP and not paused:
            if selected_piece is not None and not paused:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, col = util.getPosFromMouseCords(mouse_x, mouse_y)

                # Check if the move is valid (valid square)
                if game_board.is_valid_move(selected_piece, (row, col)):
                    game_board.move_piece(selected_piece, (row, col))

                selected_piece = None

    winner = game_board.check_winner()
    if winner and not paused:
        print(f"{winner} wins the game!")
        paused = True

    if not paused:
        # Clear screen
        window.fill((255,165,79))  # Window background

        # Draw board and pieces
        game_board.draw_board()
        game_board.draw_pieces()

        # Display current turn
        game_gui.display_turn(game_board.turn)

        pygame.display.update()  # pygame.display.update()
    
    # AI's turn
    if game_board.turn == "AI" and not paused:
        time.sleep(0.5)
        print("AI's turn...")
        best_move = game_ai.get_best_move()
        if best_move:
            game_board.apply_move(best_move)  # AI makes its move
            # game_board.turn = "Player"  # Switch turn to the player after AI's move
        else:
            print("AI has no valid moves! Game Over.")
            # paused = True
        
    pygame_widgets.update(events)

    # Clear screen
    window.fill((255,165,79))  # Window background

    # Draw board and pieces
    game_board.draw_board()
    game_board.draw_pieces()

    if not paused:
        # Display current turn
        game_gui.display_turn(game_board.turn)
    
    if paused:        
        if play_again:
            new_difficulty_level = game_gui.display_choose_difficulty(events)
            print(F"[DEBUG] LAUNCH: Diff Received from GUI - {new_difficulty_level}")
            if new_difficulty_level:
                winner = None
                selected_piece = None
                game_board = board.Board(window)
                game_ai = ai.AI(game_board, level=new_difficulty_level)
                game_gui = gui.GUI(window)
                paused = False
                play_again = False
        elif winner:
            # TODO: Implement game over!
            play_again = game_gui.display_game_over(winner, pygame.event.get())

    pygame.display.update()  # pygame.display.update()
    clock.tick(60)

pygame.quit()

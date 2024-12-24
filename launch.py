import pygame
import board
import util
import ai  # Import the AI module
import consts

# pygame setup
pygame.init()
window = pygame.display.set_mode((1280, 720), 0, 32)
clock = pygame.time.Clock()
running = True
paused = False

# Initialize font
pygame.font.init()
font = pygame.font.SysFont("Helvetica", 36)  # Choose font and size

# Initialize board object
game_board = board.Board(window)

# Selected piece tracking
selected_piece = None

# Ask the user to select AI level
ai_level = "medium"  # Change this to "easy", "medium", or "hard" to test AI levels
game_ai = ai.AI(game_board, level=ai_level)

def display_turn(window, turn):
    """Display the current player's turn on the screen."""

    text = f"Red's Turn" if turn == "AI" else "Black's Turn"
    text_surface = font.render(text, True, "black")  
    text_position =  (
                        consts.X_CENTER_OFFSET - text_surface.get_width() - 50,
                        consts.Y_CENTER_OFFSET * 4 - text_surface.get_height() / 2
                        ) if turn == "AI" else (
                          consts.X_CENTER_OFFSET + 8 * consts.SQUARE_SIZE + 60,
                          consts.Y_CENTER_OFFSET * 14 - text_surface.get_height() / 2
                        )
    
    # TODO: Add rectangle behind text
    
    window.blit(text_surface, text_position)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = util.getPosFromMouseCords(mouse_x, mouse_y)

            # If a piece is clicked, select it
            if game_board.boardArray[row][col] is not None \
            and game_board.boardArray[row][col].player == "Player" \
                and not paused:
                selected_piece = (row, col)
                print(f"Piece selected at: {selected_piece}")

        if event.type == pygame.MOUSEBUTTONUP:
            if selected_piece is not None and not paused:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, col = util.getPosFromMouseCords(mouse_x, mouse_y)

                # Check if the move is valid (valid square)
                if game_board.is_valid_move(selected_piece, (row, col)):
                    game_board.move_piece(selected_piece, (row, col))

                selected_piece = None

    # AI's turn
    if game_board.turn == "AI" and not paused:
        print("AI's turn...")
        best_move = game_ai.get_best_move()
        if best_move:
            game_board.apply_move(best_move)  # AI makes its move
            # game_board.turn = "Player"  # Switch turn to the player after AI's move
        else:
            print("AI has no valid moves! Game Over.")
            # paused = True


    winner = game_board.check_winner()
    if winner and not paused:
        print(f"{winner} wins the game!")
        paused = True

    # Clear screen
    window.fill("white")  # Window background

    # Draw board and pieces
    game_board.draw_board()
    game_board.draw_pieces()

    # Display current turn
    display_turn(window, game_board.turn)

    pygame.display.flip()  # pygame.display.update()
    clock.tick(60)

pygame.quit()

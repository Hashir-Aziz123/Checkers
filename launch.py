import pygame
import board
import util
import ai  # Import the AI module
import consts

# pygame setup
pygame.init()
window = pygame.display.set_mode((1300, 700), 0, 32)
clock = pygame.time.Clock()
running = True

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
    text = f"Red's Turn (AI)" if turn == "player1" else "Black's Turn (You)"
    text_surface = font.render(text, True, (255, 255, 255))  # White text
    window.blit(text_surface, (window.get_width() // 2 - text_surface.get_width() // 2, 17))

while running:
    print(game_board.turn)  # Debugging turn tracking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = util.getPosFromMouseCords(mouse_x, mouse_y)

            # If a piece is clicked, select it
            if game_board.boardArray[row][col] is not None and game_board.boardArray[row][col].player == "player2":
                selected_piece = (row, col)
                print(f"Piece selected at: {selected_piece}")

        if event.type == pygame.MOUSEBUTTONUP:
            if selected_piece is not None:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, col = util.getPosFromMouseCords(mouse_x, mouse_y)

                # Check if the move is valid (valid square)
                if game_board.is_valid_move(selected_piece, (row, col)):
                    game_board.move_piece(selected_piece, (row, col))
                    selected_piece = None
                    game_board.turn = "player1"  # Switch turn to AI after player's move

    # AI's turn
    if game_board.turn == "player1":
        print("AI's turn...")
        best_move = game_ai.get_best_move()
        if best_move:
            game_board.apply_move(best_move)  # AI makes its move
            game_board.turn = "player2"  # Switch turn to the player after AI's move
        else:
            print("AI has no valid moves! Game Over.")
            running = False

    # Clear screen
    window.fill((0, 0, 0))  # Black background

    # Draw board and pieces
    game_board.draw_board()
    game_board.draw_pieces()

    # Display current turn
    display_turn(window, game_board.turn)

    pygame.display.flip()  # pygame.display.update()
    clock.tick(60)

pygame.quit()

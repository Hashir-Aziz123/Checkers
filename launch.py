import pygame
import board
import util
import pieces
import consts

# pygame setup
pygame.init()
window = pygame.display.set_mode((1280, 720), 0, 32)
clock = pygame.time.Clock()
running = True

# Initialize font
pygame.font.init()
font = pygame.font.SysFont("Helvetica", 36)  # Choose font and size

# Initialize board object
game_board = board.board(window)

# Selected piece tracking
selected_piece = None
selected_piece_pos = None

def display_turn(window, turn):
    """Display the current player's turn on the screen."""

    text = f"Red's Turn" if turn == "player1" else "Black's Turn"
    text_surface = font.render(text, True, "black")  
    text_position =  (
                        consts.X_CENTER_OFFSET - text_surface.get_width() - 50,
                        consts.Y_CENTER_OFFSET * 4 - text_surface.get_height() / 2
                        ) if turn == "player1" else (
                          consts.X_CENTER_OFFSET + 8 * consts.SQUARE_SIZE + 60,
                          consts.Y_CENTER_OFFSET * 14 - text_surface.get_height() / 2
                        )
    
    # TODO: Add rectangle behind text
    
    window.blit(text_surface, text_position)

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row, col = util.getPosFromMouseCords(mouse_x, mouse_y)

            # If a piece is clicked, select it
            if game_board.boardArray[row][col] != None:
                selected_piece = (row, col)
                print(f"Piece selected at: {selected_piece}")

        if event.type == pygame.MOUSEBUTTONUP:
            if selected_piece is not None:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, col = util.getPosFromMouseCords(mouse_x, mouse_y)

                # Check if the move is valid (valid square)
                if game_board.boardArray[row][col] == None:  
                    # Move the piece to the new square
                    game_board.move_piece(selected_piece, (row, col))

                winner = game_board.check_winner()
                if winner:
                    print(f"{winner} wins the game!")

                # Reset selection after move attempt
                selected_piece = None

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

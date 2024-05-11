import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
DIMENSION = 8  # 8x8 chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Piece symbols
PIECES = {
    'bP': '♟', 'bR': '♜', 'bN': '♞', 'bB': '♝', 'bQ': '♛', 'bK': '♚',
    'wP': '♙', 'wR': '♖', 'wN': '♘', 'wB': '♗', 'wQ': '♕', 'wK': '♔'
}


# Chess board initial setup
def create_board():
    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    return board


# Load images
def load_images():
    pieces = {}
    for piece in PIECES:
        pieces[piece] = pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
    return pieces


# Main drawing function
def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board, images):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece:
                screen.blit(images[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Convert board position to coordinates
def convert_pos(pos):
    x, y = pos
    row = y // SQ_SIZE
    col = x // SQ_SIZE
    return row, col


# Check if a position is on the board
def is_on_board(row, col):
    return 0 <= row < DIMENSION and 0 <= col < DIMENSION


# Pawn moves
def get_pawn_moves(board, row, col, is_white):
    moves = []
    direction = -1 if is_white else 1
    start_row = 6 if is_white else 1

    # Forward moves
    if is_on_board(row + direction, col) and board[row + direction][col] is None:
        moves.append((row + direction, col))
        # Double move
        if row == start_row and board[row + 2 * direction][col] is None:
            moves.append((row + 2 * direction, col))

    # Captures
    for d_col in [-1, 1]:
        if is_on_board(row + direction, col + d_col) and board[row + direction][col + d_col] is not None:
            if board[row + direction][col + d_col][0] != ('w' if is_white else 'b'):
                moves.append((row + direction, col + d_col))

    return moves


# Rook moves
def get_rook_moves(board, row, col, is_white):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    enemy_color = 'b' if is_white else 'w'

    for d_row, d_col in directions:
        r, c = row, col
        while True:
            r += d_row
            c += d_col
            if not is_on_board(r, c):
                break
            if board[r][c] is None:
                moves.append((r, c))
            elif board[r][c][0] == enemy_color:
                moves.append((r, c))
                break
            else:
                break

    return moves


# Knight moves
def get_knight_moves(board, row, col, is_white):
    moves = []
    knight_moves = [
        (-2, -1), (-1, -2), (1, -2), (2, -1),
        (2, 1), (1, 2), (-1, 2), (-2, 1)
    ]
    enemy_color = 'b' if is_white else 'w'

    for d_row, d_col in knight_moves:
        r, c = row + d_row, col + d_col
        if is_on_board(r, c) and (board[r][c] is None or board[r][c][0] == enemy_color):
            moves.append((r, c))

    return moves


# Bishop moves
def get_bishop_moves(board, row, col, is_white):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    enemy_color = 'b' if is_white else 'w'

    for d_row, d_col in directions:
        r, c = row, col
        while True:
            r += d_row
            c += d_col
            if not is_on_board(r, c):
                break
            if board[r][c] is None:
                moves.append((r, c))
            elif board[r][c][0] == enemy_color:
                moves.append((r, c))
                break
            else:
                break

    return moves


# Queen moves
def get_queen_moves(board, row, col, is_white):
    return get_bishop_moves(board, row, col, is_white) + get_rook_moves(board, row, col, is_white)


# King moves
def get_king_moves(board, row, col, is_white):
    moves = []
    king_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    enemy_color = 'b' if is_white else 'w'

    for d_row, d_col in king_moves:
        r, c = row + d_row, col + d_col
        if is_on_board(r, c) and (board[r][c] is None or board[r][c][0] == enemy_color):
            moves.append((r, c))

    return moves


# Get piece moves
def get_piece_moves(board, row, col):
    piece = board[row][col]
    if piece is None:
        return []

    is_white = piece[0] == 'w'
    piece_type = piece[1]

    if piece_type == 'P':
        return get_pawn_moves(board, row, col, is_white)
    elif piece_type == 'R':
        return get_rook_moves(board, row, col, is_white)
    elif piece_type == 'N':
        return get_knight_moves(board, row, col, is_white)
    elif piece_type == 'B':
        return get_bishop_moves(board, row, col, is_white)
    elif piece_type == 'Q':
        return get_queen_moves(board, row, col, is_white)
    elif piece_type == 'K':
        return get_king_moves(board, row, col, is_white)
    else:
        return []


def is_in_check(board, king_pos, player_turn):
    enemy_color = 'b' if player_turn == 'w' else 'w'
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if board[r][c] and board[r][c][0] == enemy_color:
                if king_pos in get_piece_moves(board, r, c):
                    return True
    return False


def is_legal_move(board, s_row, s_col, e_row, e_col, player_turn):
    piece = board[s_row][s_col]
    if piece[0] != player_turn:
        return False
    legal_moves = get_piece_moves(board, s_row, s_col)
    if (e_row, e_col) not in legal_moves:
        return False

    # Simulate the move and check for checks
    temp_board = [row[:] for row in board]
    temp_board[e_row][e_col] = temp_board[s_row][s_col]
    temp_board[s_row][s_col] = None
    king_pos = None
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if temp_board[r][c] == player_turn + 'K':
                king_pos = (r, c)
    if king_pos and is_in_check(temp_board, king_pos, player_turn):
        return False
    return True


def is_checkmate(board, player_turn):
    king_pos = None
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if board[r][c] == player_turn + 'K':
                king_pos = (r, c)

    if king_pos and not is_in_check(board, king_pos, player_turn):
        return False

    # Try all moves for all pieces
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if board[r][c] and board[r][c][0] == player_turn:
                legal_moves = get_piece_moves(board, r, c)
                for move in legal_moves:
                    if is_legal_move(board, r, c, move[0], move[1], player_turn):
                        return False
    return True


# Main game loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = create_board()
    images = load_images()
    running = True
    selected_piece = None
    player_turn = 'w'
    game_over = False

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN and not game_over:
                location = pygame.mouse.get_pos()
                row, col = convert_pos(location)
                if selected_piece:
                    # Attempt to move the piece if it is a valid move
                    s_row, s_col = selected_piece
                    if is_legal_move(board, s_row, s_col, row, col, player_turn):
                        # Make the move
                        board[row][col] = board[s_row][s_col]
                        board[s_row][s_col] = None
                        player_turn = 'b' if player_turn == 'w' else 'w'
                        # Check for checkmate
                        if is_checkmate(board, player_turn):
                            game_over = True
                            print(f"Checkmate! {'White' if player_turn == 'b' else 'Black'} wins!")
                    selected_piece = None
                else:
                    if board[row][col] and board[row][col][0] == player_turn:
                        selected_piece = (row, col)

        draw_board(screen)
        draw_pieces(screen, board, images)
        if game_over:
            font = pygame.font.SysFont("Helvetica", 32, True)
            text = font.render("Checkmate!", True, pygame.Color("Red"))
            screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.flip()
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()


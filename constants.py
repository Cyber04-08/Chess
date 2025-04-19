import os
import pygame
pygame.init()

# Set window position so it doesn't start at the very top (adjust as needed)
os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'

# Get screen info and set window size to 80% of the current screen resolution,
# then subtract TASKBAR_HEIGHT from the height to avoid overlapping the taskbar.
infoObject = pygame.display.Info()
TASKBAR_HEIGHT = 80  # Increase this value if your taskbar is taller
WIDTH = int(infoObject.current_w * 0.8)
HEIGHT = int(infoObject.current_h * 0.8) - TASKBAR_HEIGHT
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')

font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

# Define UI panel sizes based on the window dimensions
UI_BOTTOM_HEIGHT = HEIGHT // 9         # e.g. if HEIGHT is 900, this would be 100 pixels
UI_RIGHT_WIDTH = int(WIDTH * 0.2)          # 20% of WIDTH

# Board area dimensions (the board will occupy a square area)
BOARD_SIZE_PIXELS = min(WIDTH - UI_RIGHT_WIDTH, HEIGHT - UI_BOTTOM_HEIGHT)
SQUARE_SIZE = BOARD_SIZE_PIXELS // 8

# Game variables and initial piece positions
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []

# Scaling factors (using the original ratios: 100→80% for most pieces, 100→65% for pawns, 45% for small images)
PAWN_SCALE = 0.65
PIECE_SCALE = 0.8
SMALL_SCALE = 0.45

# Load and scale images relative to SQUARE_SIZE
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
black_queen_small = pygame.transform.scale(black_queen, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
black_king_small = pygame.transform.scale(black_king, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
black_rook_small = pygame.transform.scale(black_rook, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
black_bishop_small = pygame.transform.scale(black_bishop, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
black_knight_small = pygame.transform.scale(black_knight, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (int(PAWN_SCALE * SQUARE_SIZE), int(PAWN_SCALE * SQUARE_SIZE)))
black_pawn_small = pygame.transform.scale(black_pawn, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
white_queen_small = pygame.transform.scale(white_queen, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
white_king_small = pygame.transform.scale(white_king, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
white_rook_small = pygame.transform.scale(white_rook, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
white_bishop_small = pygame.transform.scale(white_bishop, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (int(PIECE_SCALE * SQUARE_SIZE), int(PIECE_SCALE * SQUARE_SIZE)))
white_knight_small = pygame.transform.scale(white_knight, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (int(PAWN_SCALE * SQUARE_SIZE), int(PAWN_SCALE * SQUARE_SIZE)))
white_pawn_small = pygame.transform.scale(white_pawn, (int(SMALL_SCALE * SQUARE_SIZE), int(SMALL_SCALE * SQUARE_SIZE)))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False] * 16
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
black_moved = [False] * 16
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
counter = 0
winner = ''
game_over = False
# Set off-board values for en passant using SQUARE_SIZE
white_ep = (SQUARE_SIZE * 10, SQUARE_SIZE * 10)
black_ep = (SQUARE_SIZE * 10, SQUARE_SIZE * 10)
white_promote = False
black_promote = False
promo_index = 100
check = False
castling_moves = []

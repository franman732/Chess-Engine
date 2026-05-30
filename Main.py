import numpy as np # THis is intended to maximize white, minimize black. Be able to set turn so it doesnt matter, and always set urself as white.
import random

#lowercase is black, capital is white ; Black is 0, white is 1

Opiece_values = [0, -100, -100, -100, -100, -100, -100, -100, -100, -500, -320, -330, -900, -20000, -330, -320, -500, 100, 100, 100, 100, 100, 100, 100, 100, 500, 320, 330, 900, 20000, 330, 320, 500]
Epiece_values = [0, -120, -120, -120, -120, -120, -120, -120, -120, -520, -300, -340, -900, -20000, -340, -300, -520, 120, 120, 120, 120, 120, 120, 120, 120, 520, 300, 340, 900, 20000, 340, 300, 520]

PHASE_VALUES = [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 1, 2]

moves_set = {}

KING_NUMBERS = {13, 29}
PAWN_NUMBERS = {1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24}
ROOK_NUMBERS = {9, 16, 25, 32}
BISHOP_NUMBERS = {11, 14, 27, 30}
QUEEN_NUMBERS = {12, 28}
KNIGHT_NUMBERS = {10, 15, 26, 31}

TT_HITS = 0
TT_LOOKUPS = 0
NUMBER_OF_RECURSIONS = 0

board = [9, 10, 11, 12, 13, 14, 15, 16, # top is black/lowercase/0 ; bottom is white/uppercase/1
                 1, 2, 3, 0, 0, 6, 7, 8,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 20, 0, 0, 0,
                 0, 0, 0, 4, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 17, 18, 19, 0, 21, 22, 23, 24,
                 25, 26, 27, 28, 29, 30, 31, 32]

Op_t = [
     0,   0,   0,   0,   0,   0,   0,   0,
    50,  50,  50,  50,  50,  50,  50,  50,
    10,  10,  20,  30,  30,  20,  10,  10,
     5,   5,  10,  25,  25,  10,   5,   5,
     0,   0,   0,  20,  20,   0,   0,   0,
     5,  -5, -10,   0,   0, -10,  -5,   5,
     5,  10,  10, -20, -20,  10,  10,   5,
     0,   0,   0,   0,   0,   0,   0,   0
]

Ob_t = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

Or_t = [
     0,   0,   5,  10,  10,   5,   0,   0,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
     5,  10,  10,  10,  10,  10,  10,   5,
     0,   0,   0,   0,   0,   0,   0,   0
]

Oq_t = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   5,   0, -10,
    -10,   0,   5,   5,   5,   5,   5, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20
]

Ok_t = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]

Okn_t = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]


Ep_t = [
     0,   0,   0,   0,   0,   0,   0,   0,
    80,  80,  80,  80,  80,  80,  80,  80,
    50,  50,  50,  50,  50,  50,  50,  50,
    30,  30,  30,  40,  40,  30,  30,  30,
    20,  20,  20,  35,  35,  20,  20,  20,
    10,  10,  10,  25,  25,  10,  10,  10,
    10,  10,  10,  10,  10,  10,  10,  10,
     0,   0,   0,   0,   0,   0,   0,   0
]

Ekn_t = [
   -50, -40, -30, -30, -30, -30, -40, -50,
   -40, -20,   0,   0,   0,   0, -20, -40,
   -30,   0,  10,  15,  15,  10,   0, -30,
   -30,   5,  15,  20,  20,  15,   5, -30,
   -30,   5,  15,  20,  20,  15,   5, -30,
   -30,   0,  10,  15,  15,  10,   0, -30,
   -40, -20,   0,   0,   0,   0, -20, -40,
   -50, -40, -30, -30, -30, -30, -40, -50
]

Eb_t = [
   -20, -10, -10, -10, -10, -10, -10, -20,
   -10,   5,   5,   5,   5,   5,   5, -10,
   -10,  10,  10,  10,  10,  10,  10, -10,
   -10,  10,  10,  15,  15,  10,  10, -10,
   -10,   5,  10,  15,  15,  10,   5, -10,
   -10,   5,   5,  10,  10,   5,   5, -10,
   -10,   0,   0,   5,   5,   0,   0, -10,
   -20, -10, -10, -10, -10, -10, -10, -20
]

Er_t = [
     0,   5,  10,  15,  15,  10,   5,   0,
     5,  10,  15,  20,  20,  15,  10,   5,
     0,   5,  10,  15,  15,  10,   5,   0,
     0,   5,  10,  15,  15,  10,   5,   0,
     0,   5,  10,  15,  15,  10,   5,   0,
     0,   5,  10,  15,  15,  10,   5,   0,
    10,  20,  20,  25,  25,  20,  20,  10,
     0,   5,  10,  15,  15,  10,   5,   0
]

Eq_t= [
   -10,  -5,  -5,   0,   0,  -5,  -5, -10,
    -5,   5,   5,   5,   5,   5,   5,  -5,
    -5,   5,  10,  10,  10,  10,   5,  -5,
     0,   5,  10,  15,  15,  10,   5,   0,
     0,   5,  10,  15,  15,  10,   5,   0,
    -5,   5,  10,  10,  10,  10,   5,  -5,
    -5,   5,   5,   5,   5,   5,   5,  -5,
   -10,  -5,  -5,   0,   0,  -5,  -5, -10
]

Ek_t = [
   -50, -40, -30, -20, -20, -30, -40, -50,
   -30, -20, -10,   0,   0, -10, -20, -30,
   -20, -10,  10,  20,  20,  10, -10, -20,
   -10,   0,  20,  30,  30,  20,   0, -10,
   -10,   0,  20,  30,  30,  20,   0, -10,
   -20, -10,  10,  20,  20,  10, -10, -20,
   -30, -20, -10,   0,   0, -10, -20, -30,
   -50, -40, -30, -20, -20, -30, -40, -50
]

Opst = [0, Op_t, Op_t, Op_t, Op_t, Op_t, Op_t, Op_t, Op_t, Or_t, Okn_t, Ob_t, Oq_t, Ok_t, Ob_t, Okn_t, Or_t, Op_t, Op_t, Op_t, Op_t, Op_t, Op_t, Op_t, Op_t, Or_t, Okn_t, Ob_t, Oq_t, Ok_t, Ob_t, Okn_t, Or_t]
Epst = [0, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Er_t, Ekn_t, Eb_t, Eq_t, Ek_t, Eb_t, Ekn_t, Er_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Er_t, Ekn_t, Eb_t, Eq_t, Ek_t, Eb_t, Ekn_t, Er_t]
# list that contains all the Piece-Square Tables for quick lookup in evaluation function

WK = 4
WQ = 8
BK = 1
BQ = 2 # These are for bitwise changes of castle_rights
initial_castle_rights = BK | BQ | WK | WQ

MAX_DEPTH = 64
killer_moves = [[None, None] for _ in range(MAX_DEPTH)]

history = [[0] * 64 for _ in range(64)]

ZOBRIST = [[random.getrandbits(64) for _ in range(64)] for _ in range(33)]
ZOBRIST_SIDE = random.getrandbits(64)
ZOBRIST_CASTLE = {
    BK: random.getrandbits(64),
    BQ: random.getrandbits(64),
    WK: random.getrandbits(64),
    WQ: random.getrandbits(64),
}
TT = {}

class Position:
    def __init__(self, board, side_to_move, castle_rights, hash, black_king, white_king):
        self.board = board
        self.side_to_move = side_to_move
        self.castle_rights = castle_rights
        self.hash = hash
        self.black_king = black_king
        self.white_king = white_king

def get_color(board, index):
    if board[index] == 0:
        return -1
    
    return 0 if board[index] <= 16 else 1

def determine_capturable(board, end, color):
    if end < 0 or end > 63:
        return False
    
    if -1 != get_color(board, end) != color:
        return True
    else:
        return False

def determine_pawn_moves(board, moves, start): #Pawn is done. First section includes forwards movements, second section includes capture moves
    color = get_color(board, start)
    if color == 0:
        if ((1 == start // 8) and board[start + 16] == 0 and board[start + 8] == 0):
            moves.append((start, start + 16, -1))
            moves.append((start, start + 8, -1))
        elif board[start + 8] == 0:
            moves.append((start, start + 8, -1))
        
        if is_valid_pawn_move(start, start + 7) and determine_capturable(board, start + 7, color):
            moves.append((start, start + 7, -1))
        if is_valid_pawn_move(start, start + 9) and determine_capturable(board, start + 9, color):
            moves.append((start, start + 9, -1))

    elif color == 1:
        if ((start // 8 == 6)) and board[start - 16] == 0 and board[start - 8] == 0:
            moves.append((start, start - 16, -1))
            moves.append((start, start - 8, -1))
        elif board[start - 8] == 0: 
            moves.append((start, start - 8, -1))

        if is_valid_pawn_move(start, start - 7) and determine_capturable(board, start - 7, color):
            moves.append((start, start - 7, -1))
        if is_valid_pawn_move(start, start - 9) and determine_capturable(board, start - 9, color):
            moves.append((start, start - 9, -1))

def is_valid_pawn_move(start, target):
    if target < 0 or target >= 64:
        return False

    start_file = start % 8
    target_file = target % 8

    diff = abs(start_file - target_file)

    return diff in (0, 1)

def determine_rook_moves(board, moves, start):
    color = get_color(board, start)

    for direction in [-1, 1, -8, 8]:
        current = start

        while True:
            next_square = current + direction

            if not is_valid_rook_step(current, next_square, direction):
                break

            piece = board[next_square]

            if piece == 0:
                moves.append((start, next_square, -1))
            else:
                if get_color(board, next_square) != color:
                    moves.append((start, next_square, -1))
                break

            current = next_square

def is_valid_rook_step(current, next_square, direction):
    if next_square < 0 or next_square >= 64:
        return False

    current_row = current // 8
    current_col = current % 8

    next_row = next_square // 8
    next_col = next_square % 8

    if direction == -1 or direction == 1:
        return current_row == next_row

    if direction == -8 or direction == 8:
        return current_col == next_col

    return False
        
def is_valid_knight_move(start, target):
    if target < 0 or target >= 64:
        return False

    start_file = start % 8
    target_file = target % 8

    diff = abs(start_file - target_file)

    return diff in (1, 2)

def determine_knight_moves(board, moves, start):
    color = get_color(board, start)

    for offset in [6, 10, 15, 17, -6, -10, -15, -17]:
        target = start + offset

        if not is_valid_knight_move(start, target):
            continue

        piece = board[target]
        target_color = get_color(board, target)

        if target_color != color:
            moves.append((start, target, -1))

def determine_bishop_moves(board, moves, start_pos):
    color = get_color(board, start_pos)

    # 4 diagonal directions: up-left, up-right, down-left, down-right
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    row = start_pos // 8
    col = start_pos % 8

    for dr, dc in directions:
        r, c = row + dr, col + dc

        while 0 <= r < 8 and 0 <= c < 8:
            idx = r * 8 + c

            # empty square
            if board[idx] == 0:
                moves.append((start_pos, idx, -1))

            else:
                # occupied square -> check capture
                if determine_capturable(board, idx, color):
                    moves.append((start_pos, idx, -1))

                # stop sliding in this direction no matter what
                break

            r += dr
            c += dc

def determine_queen_moves(board, moves, start_pos):
    # just reuse rook + bishop logic
    determine_bishop_moves(board, moves, start_pos)
    determine_rook_moves(board, moves, start_pos)

def determine_king_moves(board, moves, start_pos, castle_rights):
    color = get_color(board, start_pos)
    psudo_moves = None

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]

    row = start_pos // 8
    col = start_pos % 8

    for dr, dc in directions:
        r = row + dr
        c = col + dc

        if 0 <= r < 8 and 0 <= c < 8:
            idx = r * 8 + c
            piece = board[idx]

            # empty square
            if piece == 0:
                moves.append((start_pos, idx, -1))

            # enemy piece
            elif determine_capturable(board, idx, color):
                moves.append((start_pos, idx, -1))

    if castle_rights != 0:
        if color == 0: # Black is 0, white is 1
            if castle_rights & BK: # kingside
                if board[5] == 0 and board[6] == 0:
                    if board[7] == 16:
                        if (not is_square_attacked(4, board, 0) and
                            not is_square_attacked(5, board, 0) and
                            not is_square_attacked(6, board, 0)):
                            moves.append((4, 6, 0))

            if castle_rights & BQ: # queenside
                if board[1] == 0 and board[2] == 0 and board[3] == 0:
                    if board[0] == 9:
                        if (not is_square_attacked(4, board, 0) and
                            not is_square_attacked(3, board, 0) and
                            not is_square_attacked(2, board, 0)):
                            moves.append((4, 2, 1))
                            
        elif color == 1:
            if castle_rights & WK: # kingside
                if board[61] == 0 and board[62] == 0:
                    if board[63] == 32:
                        if (not is_square_attacked(60, board, 1) and
                            not is_square_attacked(61, board, 1) and
                            not is_square_attacked(62, board, 1)):
                            moves.append((60, 62, 2))

            if castle_rights & WQ: # queenside
                if board[59] == 0 and board[58] == 0 and board[57] == 0:
                    if board[56] == 25:
                        if (not is_square_attacked(60, board, 1) and
                            not is_square_attacked(59, board, 1) and
                            not is_square_attacked(58, board, 1)):
                            moves.append((60, 58, 3))

def create_pseudo_moves(board, color, castle_rights): # takes a board state, and returns all possible moves, legal and illegal, given that position; ALso, returns only legal castle moves... whoops
    moves = [] #(start_position, end_position) position is by index number 
    for i, value in enumerate(board):
        if get_color(board, i) == color:
            if value in PAWN_NUMBERS:
                determine_pawn_moves(board, moves, i) #ignore_pawn_forwards is for ignoring them when determining attacked squares

            elif value in ROOK_NUMBERS:
                determine_rook_moves(board, moves, i)

            elif value in KNIGHT_NUMBERS:
                determine_knight_moves(board, moves, i)

            elif value in BISHOP_NUMBERS:
                determine_bishop_moves(board, moves, i)

            elif value in QUEEN_NUMBERS:
                determine_queen_moves(board, moves, i)

            elif value in KING_NUMBERS:
                determine_king_moves(board, moves, i, castle_rights)
    return moves

def compute_hash(board, side_to_move, castle):
    h = 0
    
    for i, piece in enumerate(board):
        if piece != 0:
            h ^= ZOBRIST[piece][i]

    if side_to_move == 1:
        h ^= ZOBRIST_SIDE

    if castle & WK:
        h ^= ZOBRIST_CASTLE[WK]

    if castle & WQ:
        h ^= ZOBRIST_CASTLE[WQ]

    if castle & BK:
        h ^= ZOBRIST_CASTLE[BK]

    if castle & BQ:
        h ^= ZOBRIST_CASTLE[BQ]

    return h

def make_move(position, move): # all determination of whether a move is legal should be done before make_move. Make_move simply returns a board with the move made, and is used to determine if a move puts a king in check or not.
    start, end, extra = move
    castle_rights = position.castle_rights
    undo = [position.board[end], position.castle_rights, position.side_to_move, position.hash, -1]
    hash = position.hash

    new_board = position.board
    moved_piece = new_board[start]


    if moved_piece == 13:
        position.black_king = end

    elif moved_piece == 29:
        position.white_king = end

    if extra == -1:
        end_piece = new_board[end]

        hash ^= ZOBRIST[moved_piece][start] ^ ZOBRIST[moved_piece][end]

        if end_piece != 0:
            hash ^= ZOBRIST[end_piece][end]

        hash ^= ZOBRIST_SIDE

        new_board[end] = moved_piece
        new_board[start] = 0
        
        if moved_piece in PAWN_NUMBERS: # If it is a pawn promotion, turn it into a queen; extra = 4 means white promotion, 5 means black promotion
            if end // 8 == 0:
                new_board[end] = 28 
                hash ^= ZOBRIST[moved_piece][end] ^ ZOBRIST[28][end]
                undo[4] = moved_piece
            elif end // 8 == 7:
                new_board[end] = 12
                hash ^= ZOBRIST[moved_piece][end] ^ ZOBRIST[12][end]
                undo[4] = moved_piece

# This section changes castle rights based on moves to the rook or king
        if ((moved_piece == 9 and start == 0) or end_piece == 9) and castle_rights & BQ: # If queenside Rook
            castle_rights &= ~BQ
            hash ^= ZOBRIST_CASTLE[BQ]
        elif ((moved_piece == 16 and start == 7) or end_piece == 16) and castle_rights & BK: # If kingside rook
            castle_rights &= ~BK
            hash ^= ZOBRIST_CASTLE[BK]
        elif (moved_piece == 13 and start == 4) and (castle_rights & BK or castle_rights & BQ): # If king
            if castle_rights & BK:
                hash ^= ZOBRIST_CASTLE[BK]
                castle_rights &= ~BK 
            if castle_rights & BQ:
                hash ^= ZOBRIST_CASTLE[BQ]
                castle_rights &= ~BQ  # This section is entirely for black pieces

        elif ((moved_piece == 25 and start == 56) or end_piece == 25) and castle_rights & WQ: # If queenside rook
            castle_rights &= ~WQ
            hash ^= ZOBRIST_CASTLE[WQ]
        elif ((moved_piece == 32 and start == 63) or end_piece == 32) and castle_rights & WK:
            castle_rights &= ~WK
            hash ^= ZOBRIST_CASTLE[WK]
        elif (moved_piece == 29 and start == 60) and (castle_rights & WK or castle_rights & WQ):
            if castle_rights & WK:
                hash ^= ZOBRIST_CASTLE[WK]
                castle_rights &= ~WK
            if castle_rights & WQ:
                hash ^= ZOBRIST_CASTLE[WQ]
                castle_rights &= ~WQ


    else: # This section changes castle rights and the board state based on actual castle moves
        metadata = extra # for castle moves, start and end refer to king position. flags: 0 = black_kingside, 1 = black_queenside, 2 = white_kingside, 3 = white_queenside

        hash ^= ZOBRIST[new_board[start]][start] ^ ZOBRIST[new_board[start]][end]

        new_board[end] = moved_piece
        new_board[start] = 0

        hash ^= ZOBRIST_SIDE

        if metadata == 0:
            hash ^= ZOBRIST[16][7] ^ ZOBRIST[16][5] 
            
            new_board[5] = new_board[7]
            new_board[7] = 0
            castle_rights &= ~BQ & ~BK
            hash ^= ZOBRIST_CASTLE[BQ] ^ ZOBRIST_CASTLE[BK]

        elif metadata == 1:
            hash ^= ZOBRIST[9][0] ^ ZOBRIST[9][3]

            new_board[3] = new_board[0]
            new_board[0] = 0
            castle_rights &= ~BQ & ~BK
            hash ^= ZOBRIST_CASTLE[BQ] ^ ZOBRIST_CASTLE[BK]

        elif metadata == 2:
            hash ^= ZOBRIST[32][63] ^ ZOBRIST[32][61]

            new_board[61] = new_board[63]
            new_board[63] = 0
            castle_rights &= ~WQ & ~WK
            hash ^= ZOBRIST_CASTLE[WQ] ^ ZOBRIST_CASTLE[WK]

        elif metadata == 3:
            hash ^= ZOBRIST[25][56] ^ ZOBRIST[25][59]

            new_board[59] = new_board[56]
            new_board[56] = 0
            castle_rights &= ~WQ & ~WK
            hash ^= ZOBRIST_CASTLE[WQ] ^ ZOBRIST_CASTLE[WK]

    position.side_to_move = 1 - position.side_to_move
    position.hash = hash
    position.castle_rights = castle_rights

    return position, undo

def find_king(board, color):
    for i, piece in enumerate(board):
        if piece == 0:
            continue

        if piece in KING_NUMBERS:
            if get_color(board, i) == color:
                return i

    return -1

def is_square_attacked(square, board, color): # color of the side that wants to move to that square; IE the side that needs the square to not be attacked.
    # 4 diagonal directions: up-left, up-right, down-left, down-right
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    row = square // 8
    col = square % 8

    for dr, dc in directions:
        r, c = row + dr, col + dc

        while 0 <= r < 8 and 0 <= c < 8:
            idx = r * 8 + c
            value = board[idx]

            # empty square
            if value == 0:
                r += dr
                c += dc
                continue

            else:
                # occupied square -> check capture
                enemy_color = 0 if value < 17 else 1
                if enemy_color != color: #if capturable, it means the piece of the opposite color.
                    if (value in BISHOP_NUMBERS) or (value in QUEEN_NUMBERS):
                        return True
                    if (value in PAWN_NUMBERS):
                        if enemy_color == 0 and (r - row) == -1:
                            return True
                        if enemy_color == 1 and (r - row) == 1:
                            return True
                    if (value in KING_NUMBERS) and (r - row) in (-1, 1):
                        return True

                # stop sliding in this direction no matter what
                break


    for direction in [-1, 1, -8, 8]:
        current = square
        step = 0

        while True:
            step += 1
            next_square = current + direction

            if not is_valid_rook_step(current, next_square, direction):
                break

            piece = board[next_square]

            if piece == 0:
                current = next_square
                continue
            else:
                if get_color(board, next_square) != color:
                    if (piece in ROOK_NUMBERS) or (piece in QUEEN_NUMBERS):
                        return True
                    if (piece in KING_NUMBERS) and step == 1:
                        return True
                break


    for change in [6, 10, 15, 17, -6, -10, -15, -17]:
        target = square + change

        if not is_valid_knight_move(square, target):
            continue

        piece = board[target]
        target_color = get_color(board, target)

        if target_color != color:
            if piece in KNIGHT_NUMBERS:
                return True
        
    return False

def determine_pawn_legality(board, move): # This just makes sure that the pawn move does not go across the board
    start, end, extra = move
    start_col = start % 8
    end_col = end % 8

    if abs(start_col - end_col) != 0:
        if  -1 != get_color(board, end) != get_color(board, start):
            return True
        else:
            return False
    else:
        return True

def determine_legal_moves(position, all_moves): #Takes a board and psudo moves for that board, and returns a complete set of legal moves for that board
    legal_moves = [] # In the call to this function, all_moves contains all moves, including pawns moving forward
    board = position.board
    moving_color = position.side_to_move

    for move in all_moves:

        start, end, extra = move

        temp_position, undo = make_move(position, move)

        temp_board = temp_position.board
        king_square = (
            temp_position.white_king
            if moving_color == 1
            else temp_position.black_king
        )


        if not is_square_attacked(king_square, temp_board, moving_color):

            if board[start] in PAWN_NUMBERS:
                if determine_pawn_legality(board, move):
                    legal_moves.append(move)
            else:
                legal_moves.append(move)

        undo_move(temp_position, move, undo)

    return legal_moves

def score_move(position, move, depth, best_move):
    start, end, extra = move

    attacker = position.board[start]
    victim = position.board[end]

    score = 0

    # Transposition board
    if move == best_move:
        score += 10000000

    if victim == 0:
        score += history[start][end]

    # captures first
    if victim != 0:
        score += 10000
        score += 10 * victim
        score -= attacker

    # promotions
    if attacker in PAWN_NUMBERS:
        if end // 8 == 0 or end // 8 == 7:
            score += 100000

    # killer moves
    if move == killer_moves[depth][0]:
        score += 8000
    elif move == killer_moves[depth][1]:
        score += 7000

    return score

def create_scored_moves(position, legal_moves, depth, entry_move):
    scored_moves = []
    
    for move in legal_moves:
        score = score_move(position, move, depth, entry_move)
        scored_moves.append((score, move))

    scored_moves.sort(reverse=True)
    return scored_moves

def evaluate_board(board):

    Og_eval = 0
    eg_eval = 0
    phase = 0

    white_bishops = 0
    black_bishops = 0

    for i, piece in enumerate(board):

        if piece == 0:
            continue

        is_white = piece >= 17

        table_index = i if is_white else 63 - i

        # Material
        Og_eval += Opiece_values[piece]
        eg_eval += Epiece_values[piece]

        # PST
        Og_eval += Opst[piece][table_index]
        eg_eval += Epst[piece][table_index]


        # Game phase
        phase += PHASE_VALUES[piece]

        # Bishop pair
        if piece in (27, 30):
            white_bishops += 1
        elif piece in (11, 14):
            black_bishops += 1

    # Bishop pair bonuses
    if white_bishops >= 2:
        Og_eval += 50
        eg_eval += 50

    if black_bishops >= 2:
        Og_eval -= 50
        eg_eval -= 50

    # Clamp phase
    if phase > 24:
        phase = 24

    # Tapered interpolation
    eval = (
        Og_eval * phase +
        eg_eval * (24 - phase)
    ) // 24

    return eval

def undo_move(position, move, undo_info):
    start, end, extra = move
    board = position.board

    moved_piece = board[end]

    board[start] = moved_piece
    board[end] = undo_info[0]

    position.castle_rights = undo_info[1]
 
    position.side_to_move = undo_info[2]

    position.hash = undo_info[3]

    if moved_piece == 13:
        position.black_king = start

    elif moved_piece == 29:
        position.white_king = start

    if undo_info[4] != -1: # This is purely for undoing promotion moves 
        board[start] = undo_info[4]

    if extra != -1: 
        metadata = extra # for castle moves, start and end refer to king position. flags: 0 = black_kingside, 1 = black_queenside, 2 = white_kingside, 3 = white_queenside 
        
        if metadata == 0: 
            board[7] = board[5] 
            board[5] = 0 
        elif metadata == 1: 
            board[0] = board[3] 
            board[3] = 0 
        elif metadata == 2: 
            board[63] = board[61] 
            board[61] = 0 
        elif metadata == 3: 
            board[56] = board[59] 
            board[59] = 0

def recurse(position, depth, alpha, beta, maximizing):
    global TT_LOOKUPS, TT_HITS, NUMBER_OF_RECURSIONS
    NUMBER_OF_RECURSIONS += 1
    best_move = None

    board = position.board
    alpha_orig = alpha
    beta_orig = beta
    entry_move = None
    entry = TT.get(position.hash)

    if entry is not None:  
        TT_LOOKUPS += 1
        entry_depth, entry_score, entry_flag, entry_move = entry

        if entry_depth >= depth:
            if entry_flag == "EXACT":
                TT_HITS += 1
                return entry_score
            elif entry_flag == "LOWER":
                alpha = max(alpha, entry_score)
            elif entry_flag == "UPPER":
                beta = min(beta, entry_score)

            if alpha >= beta:
                TT_HITS += 1
                return entry_score

    if depth == 0:
        return evaluate_board(board)

    all_moves = create_pseudo_moves(
        board,
        position.side_to_move,
        position.castle_rights,
    )

    legal_moves = determine_legal_moves(position, all_moves)
    scored_moves = create_scored_moves(position, legal_moves, depth, entry_move)

    if maximizing:

        best = -99999999

        for scor, move in scored_moves: # scor so it doesnt mix with score for recursion
            start, end, extra = move
            captured_piece = board[end]

            temp_position, undo_info = make_move(position, move) # Initial king square is the king square of the side we want to make the move. SO, if black is moving, black king

            score = recurse(
                temp_position,
                depth - 1,
                alpha,
                beta,
                False
            )

            undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well

            if score > best:
                best = score
                best_move = move

            alpha = max(alpha, score)

            if beta <= alpha:
                history[start][end] += depth * depth

                # store killer move (only if it's quiet)
                start, end, extra = move

                if captured_piece == 0 and not (board[start] in PAWN_NUMBERS and (end // 8 in (0,7))):  # quiet move
                    if move != killer_moves[depth][0]:
                        killer_moves[depth][1] = killer_moves[depth][0]
                        killer_moves[depth][0] = move

                
                break

    else:

        best = 99999999

        for scor, move in scored_moves:
            start, end, extra = move
            captured_piece = board[end]

            temp_position, undo_info = make_move(position, move)
            score = recurse(
                temp_position,
                depth - 1,
                alpha,
                beta,
                True
            )

            undo_move(position, move, undo_info)

            if score < best:
                best = score
                best_move = move

            beta = min(beta, score)

            if beta <= alpha:
                history[start][end] += depth * depth

                # store killer move (only if it's quiet)
                start, end, extra = move

                if captured_piece == 0 and not (board[start] in PAWN_NUMBERS and (end // 8 in (0,7))):  # quiet move
                    if move != killer_moves[depth][0]:
                        killer_moves[depth][1] = killer_moves[depth][0]
                        killer_moves[depth][0] = move

                
                break
    
    flag = "EXACT"

    if best <= alpha_orig:
        flag = "UPPER"
    elif best >= beta_orig:
        flag = "LOWER"  

    if entry is None or entry[0] < depth:
        TT[position.hash] = (depth, best, flag, best_move)
    
    return best

def find_best_move(position, depth, starting_color):
    entry_move = None
    side = position.side_to_move

    all_moves = create_pseudo_moves(
        position.board,
        side,
        position.castle_rights,
    )

    legal_moves = determine_legal_moves(position, all_moves)
    scored_moves = create_scored_moves(position, legal_moves, depth, entry_move)

    best_move = None

    if side == 1:
        # WHITE MAXIMIZES

        best_eval = -99999999

        for scor, move in scored_moves:

            temp_position, undo_info = make_move(position, move)


            evaluation = recurse(
                temp_position,
                depth - 1,
                -99999999,
                99999999,
                False
            )

            undo_move(position, move, undo_info)

            if evaluation > best_eval:
                best_eval = evaluation
                best_move = move

    else:
        # BLACK MINIMIZES   

        best_eval = 99999999

        for scor, move in scored_moves:

            temp_position, undo_info = make_move(position, move)

            evaluation = recurse(
                temp_position,
                depth - 1,
                -99999999,
                99999999,
                True
            )

            undo_move(position, move, undo_info)

            if evaluation < best_eval:
                best_eval = evaluation
                best_move = move

    return best_move

position = Position(
    board,
    1,
    initial_castle_rights,
    compute_hash(board, 1, initial_castle_rights),
    find_king(board, 0),
    find_king(board, 1)
)

best_move = find_best_move(position, 6, 0)

print(best_move)


print("TTS HITS: ", TT_HITS, " TT LOOKUPS: ", TT_LOOKUPS, " RECURSIONS: ", NUMBER_OF_RECURSIONS, " ELEMENTS IN TT: ", len(TT.values()))

"""print(evaluate_board(board)) #evaluatoin is behaving weirdly. White pieces should increase evaluation, however they end up decreasing it somehow.
Position = Position(board, 0, initial_castle_rights)

a = create_pseudo_moves(Position.board, 0, Position.castle_rights, False)

print(determine_legal_moves(Position, a))"""


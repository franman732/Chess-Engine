import numpy as np # THis is intended to maximize white, minimize black. Be able to set turn so it doesnt matter, and always set urself as white.
import random

#lowercase is black, capital is white ; Black is 0, white is 1

Opiece_values = [0, -100, -100, -100, -100, -100, -100, -100, -100, -500, -320, -330, -900, -20000, -330, -320, -500, 100, 100, 100, 100, 100, 100, 100, 100, 500, 320, 330, 900, 20000, 330, 320, 500]
Epiece_values = [0, -120, -120, -120, -120, -120, -120, -120, -120, -520, -300, -340, -900, -20000, -340, -300, -520, 120, 120, 120, 120, 120, 120, 120, 120, 520, 300, 340, 900, 20000, 340, 300, 520]

phase_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 1, 2]

moves_set = {}

king_numbers = {13, 29}
pawn_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24}
rook_numbers = {9, 16, 25, 32}
bishop_numbers = {11, 14, 27, 30}
queen_numbers = {12, 28}
knight_numbers = {10, 15, 26, 31}


black_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}
white_numbers = {17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}

board = np.array([9, 10, 11, 12, 13, 14, 15, 16, # top is black/lowercase/0 ; bottom is white/uppercase/1
                 1, 2, 3, 0, 0, 6, 7, 8,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 20, 0, 0, 0,
                 0, 0, 0, 4, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 17, 18, 19, 0, 21, 22, 23, 24,
                 25, 26, 27, 28, 29, 30, 31, 32])

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
Epst = [0, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ekn_t, Eb_t, Eq_t, Ek_t, Eb_t, Ekn_t, Er_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ep_t, Ekn_t, Eb_t, Eq_t, Ek_t, Eb_t, Ekn_t, Er_t]
# list that contains all the Piece-Square Tables for quick lookup in evaluation function

initial_castle_rights = {0: True, 1: True, 2: True, 3: True}
empty_castle_rights = {0: False, 1: False, 2: False, 3: False}

MAX_DEPTH = 64
killer_moves = [[None, None] for _ in range(MAX_DEPTH)]

ZOBRIST = [[random.getrandbits(64) for _ in range(64)] for _ in range(33)]
ZOBRIST_SIDE = random.getrandbits(64)
TT = {}

class Position:
    def __init__(self, board, side_to_move, castle_rights, hash):
        self.board = board
        self.side_to_move = side_to_move
        self.castle_rights = castle_rights
        self.hash = hash

class Undo:
    def __init__(self, captured_piece, old_side_to_move, old_castle_rights):
        self.captured_piece = 0
        self.old_castle_rights = None
        self.old_side_to_move = 0

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
            moves.append((start, start + 16))
            moves.append((start, start + 8))
        elif board[start + 8] == 0:
            moves.append((start, start + 8))
        
        if is_valid_pawn_move(start, start + 7) and determine_capturable(board, start + 7, color):
            moves.append((start, start + 7))
        if is_valid_pawn_move(start, start + 9) and determine_capturable(board, start + 9, color):
            moves.append((start, start + 9))

    elif color == 1:
        if ((start // 8 == 6)) and board[start - 16] == 0 and board[start - 8] == 0:
            moves.append((start, start - 16))
            moves.append((start, start - 8))
        elif board[start - 8] == 0: 
            moves.append((start, start - 8))

        if is_valid_pawn_move(start, start - 7) and determine_capturable(board, start - 7, color):
            moves.append((start, start - 7))
        if is_valid_pawn_move(start, start - 9) and determine_capturable(board, start - 9, color):
            moves.append((start, start - 9))

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
                moves.append((start, next_square))
            else:
                if get_color(board, next_square) != color:
                    moves.append((start, next_square))
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
            moves.append((start, target))

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
                moves.append((start_pos, idx))

            else:
                # occupied square -> check capture
                if determine_capturable(board, idx, color):
                    moves.append((start_pos, idx))

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
                moves.append((start_pos, idx))

            # enemy piece
            elif determine_capturable(board, idx, color):
                moves.append((start_pos, idx))

    if castle_rights != None:
        if color == 0: # Black is 0, white is 1
            if castle_rights[0]: # kingside
                if board[5] == 0 and board[6] == 0:
                    if board[7] == 16:
                        if (not is_square_attacked(4, board, 0) and
                            not is_square_attacked(5, board, 0) and
                            not is_square_attacked(6, board, 0)):
                            moves.append((4, 6, 0))

            if castle_rights[1]: # queenside
                if board[1] == 0 and board[2] == 0 and board[3] == 0:
                    if board[0] == 9:
                        if (not is_square_attacked(4, board, 0) and
                            not is_square_attacked(3, board, 0) and
                            not is_square_attacked(2, board, 0)):
                            moves.append((4, 2, 1))
                            
        elif color == 1:
            if castle_rights[2]: # kingside
                if board[61] == 0 and board[62] == 0:
                    if board[63] == 32:
                        if (not is_square_attacked(60, board, 1) and
                            not is_square_attacked(61, board, 1) and
                            not is_square_attacked(62, board, 1)):
                            moves.append((60, 62, 2))

            if castle_rights[3]: # queenside
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
            if value in pawn_numbers:
                determine_pawn_moves(board, moves, i) #ignore_pawn_forwards is for ignoring them when determining attacked squares

            elif value in rook_numbers:
                determine_rook_moves(board, moves, i)

            elif value in knight_numbers:
                determine_knight_moves(board, moves, i)

            elif value in bishop_numbers:
                determine_bishop_moves(board, moves, i)

            elif value in queen_numbers:
                determine_queen_moves(board, moves, i)

            elif value in king_numbers:
                determine_king_moves(board, moves, i, castle_rights)
    return moves

def compute_hash(board, side_to_move):
    h = 0
    for i, piece in enumerate(board):
        if piece != 0:
            h ^= ZOBRIST[piece][i]

    if side_to_move == 1:
        h ^= ZOBRIST_SIDE

    return h

def update_hash(h, piece, start, end, side_to_move):
    h ^= ZOBRIST[piece][start]
    h ^= ZOBRIST[piece][end]
    h ^= ZOBRIST_SIDE

    return h

def make_move(position, move): # all determination of whether a move is legal should be done before make_move. Make_move simply returns a board with the move made, and is used to determine if a move puts a king in check or not.
    start, end, *extra = move
    castle_rights = position.castle_rights.copy()
    undo = [position.board[end], position.castle_rights.copy(), position.side_to_move, position.hash]
    
    new_board = position.board

    if extra == []:

        moved_piece = new_board[start]
        end_piece = new_board[end]

        position.hash ^= ZOBRIST[moved_piece][start]
        position.hash ^= ZOBRIST[moved_piece][end]

        if end_piece != 0:
            position.hash ^= ZOBRIST[end_piece][end]

        position.hash ^= ZOBRIST_SIDE

        new_board[end] = moved_piece
        new_board[start] = 0
        
        if moved_piece in pawn_numbers: # If it is a pawn promotion, turn it into a queen
            if end // 8 == 0:
                new_board[end] = 28
            elif end // 8 == 7:
                new_board[end] = 12

        if (moved_piece == 9 and start == 0) or end_piece == 9: # If queenside Rook
            castle_rights[1] = False
        elif (moved_piece == 16 and start == 7) or end_piece == 16: # If kingside rook
            castle_rights[0] = False
        elif moved_piece == 13 and start == 4: # If king
            castle_rights[0] = castle_rights[1] = False # This section is entirely for black pieces

        elif (moved_piece == 25 and start == 56) or end_piece == 25: # If queenside rook
            castle_rights[3] = False
        elif (moved_piece == 32 and start == 63) or end_piece == 32:
            castle_rights[2] = False
        elif moved_piece == 29 and start == 60:
            castle_rights[2] = castle_rights[3] = False


    else:
        metadata = extra[0] # for castle moves, start and end refer to king position. flags: 0 = black_kingside, 1 = black_queenside, 2 = white_kingside, 3 = white_queenside
        
        new_board[end] = new_board[start]
        new_board[start] = 0

        if metadata == 0:
            new_board[5] = new_board[7]
            new_board[7] = 0
            castle_rights[0] = castle_rights[1] = False

        elif metadata == 1:
            new_board[3] = new_board[0]
            new_board[0] = 0
            castle_rights[0] = castle_rights[1] = False

        elif metadata == 2:
            new_board[61] = new_board[63]
            new_board[63] = 0
            castle_rights[2] = castle_rights[3] = False

        elif metadata == 3:
            new_board[59] = new_board[56]
            new_board[56] = 0
            castle_rights[2] = castle_rights[3] = False

    position.side_to_move = 1 - position.side_to_move
    position.board = new_board
    position.castle_rights = castle_rights

    return position, undo

def find_king(board, color):
    for i, piece in enumerate(board):
        if piece == 0:
            continue

        if piece in king_numbers:
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

            # empty square
            if board[idx] == 0:
                r += dr
                c += dc
                continue

            else:
                # occupied square -> check capture
                enemy_color = get_color(board, idx)
                if enemy_color != color: #if capturable, it means the piece of the opposite color.
                    if (board[idx] in bishop_numbers) or (board[idx] in queen_numbers):
                        return True
                    if (board[idx] in pawn_numbers):
                        if enemy_color == 0 and (r - row) == 1:
                            return True
                        if enemy_color == 1 and (r - row) == -1:
                            return True
                    if (board[idx] in king_numbers) and (r - row) in (-1, 1):
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
                    if (board[next_square] in rook_numbers) or (board[next_square] in queen_numbers):
                        return True
                    if (board[next_square] in king_numbers) and step == 1:
                        return True
                break


    for change in [6, 10, 15, 17, -6, -10, -15, -17]:
        target = square + change

        if not is_valid_knight_move(square, target):
            continue

        piece = board[target]
        target_color = get_color(board, target)

        if target_color != color:
            if piece in knight_numbers:
                return True
        
    return False

def determine_pawn_legality(board, move): # This just makes sure that the pawn move does not go across the board
    start, end, *extra = move
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
    board = position.board.copy()
    moving_color = position.side_to_move

    king_square = find_king(board, moving_color)

    for move in all_moves:

        start, end, *extra = move

        temp_position, undo = make_move(position, move)

        temp_board = temp_position.board

        # if king moved, use new square
        if board[start] in king_numbers:
            check_square = end
        else:
            check_square = king_square

        if not is_square_attacked(check_square, temp_board, moving_color):

            if board[start] in pawn_numbers:
                if determine_pawn_legality(board, move):
                    legal_moves.append(move)
            else:
                legal_moves.append(move)

        undo_move(temp_position, move, undo)

    return legal_moves

def score_move(position, move, depth):

    start, end, *extra = move

    attacker = position.board[start]
    victim = position.board[end]

    score = 0

    # captures first
    if victim != 0:
        score += 10 * abs(Opiece_values[victim])
        score -= abs(Opiece_values[attacker])

    # promotions
    if attacker in pawn_numbers:
        if end // 8 == 0 or end // 8 == 7:
            score += 900

    # killer moves
    if move == killer_moves[depth][0]:
        score += 8000
    elif move == killer_moves[depth][1]:
        score += 7000

    return score

def create_scored_moves(position, legal_moves, depth):
    scored_moves = []
    
    for move in legal_moves:
        score = score_move(position, move, depth)
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

        table_index = 63 - i if is_white else i

        # Material
        Og_eval += Opiece_values[piece]
        eg_eval += Epiece_values[piece]

        # PST
        Og_eval += Opst[piece][table_index]
        eg_eval += Epst[piece][table_index]


        # Game phase
        phase += phase_values[piece]

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
 
    start, end, *extra = move

    moved_piece = position.board[end]

    position.board[start] = moved_piece
    position.board[end] = undo_info[0]

    position.castle_rights = undo_info[1]
 
    position.side_to_move = undo_info[2]

    position.hash = undo_info[3]



def recurse(position, depth, alpha, beta, maximizing):
    best_move = None

    alpha_orig = alpha
    beta_orig = beta
    entry = TT.get(position.hash)

    if entry is not None:
        entry_depth, entry_score, entry_flag, entry_move = entry

        if entry_depth >= depth:
            if entry_flag == "EXACT":
                return entry_score
            elif entry_flag == "LOWER":
                alpha = max(alpha, entry_score)
            elif entry_flag == "UPPER":
                beta = min(beta, entry_score)

            if alpha >= beta:
                return entry_score

    if depth == 0:
        return evaluate_board(position.board)

    all_moves = create_pseudo_moves(
        position.board,
        position.side_to_move,
        position.castle_rights,
    )

    legal_moves = determine_legal_moves(position, all_moves)
    scored_moves = create_scored_moves(position, legal_moves, depth)

    if maximizing:

        best = -99999999

        for scor, move in scored_moves: # scor so it doesnt mix with score for recursion
            start, end = move
            captured_piece = position.board[end]

            temp_position, undo_info = make_move(position, move)

            score = recurse(
                temp_position,
                depth - 1,
                alpha,
                beta,
                False
            )

            undo_move(position, move, undo_info)

            if score > best:
                best = score
                best_move = move

            alpha = max(alpha, score)

            if beta <= alpha:
                # store killer move (only if it's quiet)
                start, end, *extra = move

                if captured_piece == 0 and not (position.board[start] in pawn_numbers and (end // 8 in (0,7))):  # quiet move
                    if move != killer_moves[depth][0]:
                        killer_moves[depth][1] = killer_moves[depth][0]
                        killer_moves[depth][0] = move

                
                break

    else:

        best = 99999999

        for scor, move in scored_moves:
            start, end = move
            captured_piece = position.board[end]

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
                # store killer move (only if it's quiet)
                start, end, *extra = move

                if captured_piece == 0 and not (position.board[start] in pawn_numbers and (end // 8 in (0,7))):  # quiet move
                    if move != killer_moves[depth][0]:
                        killer_moves[depth][1] = killer_moves[depth][0]
                        killer_moves[depth][0] = move

                
                break

    flag = "EXACT"

    if best <= alpha_orig:
        flag = "UPPER"
    elif best >= beta_orig:
        flag = "LOWER"  
    
    TT[position.hash] = (depth, best, flag, best_move)
    
    return best

def find_best_move(position, depth):

    all_moves = create_pseudo_moves(
        position.board,
        position.side_to_move,
        position.castle_rights,
    )

    legal_moves = determine_legal_moves(position, all_moves)
    scored_moves = create_scored_moves(position, legal_moves, depth)

    best_move = None

    if position.side_to_move == 1:
        # WHITE MAXIMIZES

        best_eval = -99999999

        for scor, move in scored_moves:

            temp_position, undo_info = make_move(position, move)

            evaluation = recurse(
                position,
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
                position,
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
    compute_hash(board, 1)
)

best_move = find_best_move(position, 4)

print(best_move)



"""print(evaluate_board(board)) #evaluatoin is behaving weirdly. White pieces should increase evaluation, however they end up decreasing it somehow.
Position = Position(board, 0, initial_castle_rights)

a = create_pseudo_moves(Position.board, 0, Position.castle_rights, False)

print(determine_legal_moves(Position, a))"""


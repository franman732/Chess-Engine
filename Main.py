import numpy as np # THis is intended to maximize white, minimize black. Be able to set turn so it doesnt matter, and always set urself as white.
import random
import time
import cProfile

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

PASSED_OPENING = [0, 5, 10, 20, 35, 60, 100, 0]
PASSED_ENDGAME = [0, 10, 20, 40, 70, 120, 200, 0]

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

REDUCTION_FACTOR = 2 # This is how much depth gets reduced by for null move pruning

ZOBRIST = [[random.getrandbits(64) for _ in range(64)] for _ in range(33)]
ZOBRIST_SIDE = random.getrandbits(64)
ZOBRIST_CASTLE = {
    BK: random.getrandbits(64),
    BQ: random.getrandbits(64),
    WK: random.getrandbits(64),
    WQ: random.getrandbits(64),
}
TT = {}

OPENING_STACKED = 15
ENDING_STACKED = 10
OPENING_ISOLATED = 15
ENDING_ISOLATED = 10

PAWN_ZOBRIST = [[random.getrandbits(64) for _ in range(64)] for _ in range(25)]

PH = {} # Pawn Hash
class Position:
    def __init__(self, board, side_to_move, castle_rights, hash, black_king, white_king, pieces, opening_eval, closing_eval, phase, white_bishops, black_bishops, black_pawns, white_pawns, pawn_hash):
        self.board = board
        self.side_to_move = side_to_move
        self.castle_rights = castle_rights
        self.hash = hash
        self.black_king = black_king
        self.white_king = white_king
        self.pieces = pieces

        self.opening_eval = opening_eval
        self.closing_eval = closing_eval
        self.phase = phase
        self.white_bishops = white_bishops
        self.black_bishops = black_bishops
        self.black_pawns = black_pawns
        self.white_pawns = white_pawns
        self.pawn_hash = pawn_hash

    def update_evaluation(self, move, undo_info, final_move = False):
        global ENDING_ISOLATED, OPENING_ISOLATED, ENDING_STACKED, OPENING_STACKED
        white_stacked = 0
        black_stacked = 0
        white_isolated = 0
        black_isolated = 0

        pawn_o_eval = 0
        pawn_e_eval = 0
        phase = 0

        board = self.board
        O_eval = self.opening_eval
        E_eval = self.closing_eval
        phase = self.phase
        if not(final_move):
            start, end, extra = move
            moved_piece = board[end]
            white_pawns = self.white_pawns
            black_pawns = self.black_pawns
            captured_piece = undo_info[0]

            is_white = moved_piece >= 17
            start_table_index = start if is_white else 63 - start
            end_table_index = end if is_white else 63 - end

            captured_piece_table_index = end if not(is_white) else 63 - end # if capturing piece is white, then capturing piece is black. Thus, is_white must be flipped. 

            O_eval -= Opst[moved_piece][start_table_index] # PST updating subtracting starting pst values
            E_eval -= Epst[moved_piece][start_table_index]
            O_eval += Opst[moved_piece][end_table_index] # PST updating adding ending pst values
            E_eval += Epst[moved_piece][end_table_index]

            if moved_piece in PAWN_NUMBERS:
                row = end >> 3
                if is_white and row == 0:
                    O_eval -= Opst[moved_piece][end_table_index]
                    E_eval -= Epst[moved_piece][end_table_index]
                    O_eval -= Opiece_values[moved_piece]
                    E_eval -= Epiece_values[moved_piece]


                    O_eval += Opst[28][end_table_index]
                    E_eval += Opst[28][end_table_index]
                    O_eval += Opiece_values[28]
                    E_eval += Epiece_values[28]

                elif not(is_white) and row == 7:
                    O_eval -= Opst[moved_piece][end_table_index]
                    E_eval -= Epst[moved_piece][end_table_index]
                    O_eval -= Opiece_values[moved_piece]
                    E_eval -= Epiece_values[moved_piece]


                    O_eval += Opst[12][end_table_index]
                    E_eval += Epst[12][end_table_index]
                    O_eval += Opiece_values[12]
                    E_eval += Epiece_values[12]


            if captured_piece != 0:
                phase -= PHASE_VALUES[captured_piece] # Phase updating

                O_eval -= Opst[captured_piece][captured_piece_table_index]
                E_eval -= Epst[captured_piece][captured_piece_table_index]
                O_eval -= Opiece_values[captured_piece]
                E_eval -= Epiece_values[captured_piece]

                if captured_piece == 27 or captured_piece == 30:
                    self.white_bishops = False
                elif captured_piece == 11 or captured_piece == 14:
                    self.black_bishops = False

            elif extra != -1:
                if extra == 0: # Black kingside
                    O_eval -= Opst[16][63 - 7]
                    E_eval -= Epst[16][63 - 7]

                    O_eval += Opst[16][63 - 5]
                    E_eval += Epst[16][63 - 5]

                elif extra == 1: # Black queenside
                    O_eval -= Opst[9][63] # starting index for black rook in this case is index 0, so 63 - 0 is just 63.
                    E_eval -= Epst[9][63]

                    O_eval += Opst[9][63 - 3]
                    E_eval += Epst[9][63 - 3]

                elif extra == 2: # White kingside
                    O_eval -= Opst[32][63]
                    E_eval -= Epst[32][63]

                    O_eval += Opst[32][61]
                    E_eval += Epst[32][61]

                elif extra == 3: # White Queenside
                    O_eval -= Opst[25][56]
                    E_eval -= Epst[25][56]

                    O_eval += Opst[25][59]
                    E_eval += Epst[25][59]

            self.opening_eval = O_eval
            self.closing_eval = E_eval

        zobrist_evaluation = PH.get(self.pawn_hash, None)
        if zobrist_evaluation == None:
            pawn_Og_eval = 0
            pawn_eg_eval = 0

            for file in range(8):

                w = white_pawns[file]
                b = black_pawns[file]

                if w > 1:
                    white_stacked += w - 1

                if b > 1:
                    black_stacked += b - 1

                if w:
                    left = file > 0 and white_pawns[file - 1]
                    right = file < 7 and white_pawns[file + 1]

                    if not left and not right:
                        white_isolated += w

                if b:
                    left = file > 0 and black_pawns[file - 1]
                    right = file < 7 and black_pawns[file + 1]

                    if not left and not right:
                        black_isolated += b

            pawn_Og_eval -= white_isolated * OPENING_ISOLATED
            pawn_eg_eval -= white_isolated * ENDING_ISOLATED

            pawn_Og_eval += black_isolated * OPENING_ISOLATED
            pawn_eg_eval += black_isolated * ENDING_ISOLATED

            pawn_Og_eval -= white_stacked * OPENING_STACKED
            pawn_eg_eval -= white_stacked * ENDING_STACKED

            pawn_Og_eval += black_stacked * OPENING_STACKED
            pawn_eg_eval += black_stacked * ENDING_STACKED

            O_eval += pawn_Og_eval
            E_eval += pawn_eg_eval

            PH[self.pawn_hash] = (pawn_Og_eval, pawn_eg_eval)
        else:
            pawn_o_eval, pawn_e_eval = zobrist_evaluation
            O_eval += pawn_o_eval
            E_eval += pawn_e_eval

        if final_move:
            eval = (
                O_eval * phase +
                E_eval * (24 - phase)
            ) // 24

            self.phase = phase
            return eval

def determine_capturable(board, end, color):
    if end < 0 or end > 63:
        return False
    
    piece = board[end]
    piece_color = -1 if piece == 0 else 1 if piece >= 17 else 0

    if -1 != piece_color != color:
        return True
    else:
        return False

def determine_pawn_moves(board, moves, start): #Pawn is done. First section includes forwards movements, second section includes capture moves
    piece = board[start]
    color = -1 if piece == 0 else 1 if piece >= 17 else 0
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
    piece = board[start]
    color = -1 if piece == 0 else 1 if piece >= 17 else 0

    for direction in [-1, 1, -8, 8]:
        current = start

        while True:
            next_square = current + direction

            if not is_valid_rook_step(current, next_square, direction):
                break

            piece = board[next_square]
            piece_color = -1 if piece == 0 else 1 if piece >= 17 else 0

            if piece == 0:
                moves.append((start, next_square, -1))
            else:
                if piece_color != color:
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
    piece = board[start]
    color = -1 if piece == 0 else 1 if piece >= 17 else 0

    for offset in [6, 10, 15, 17, -6, -10, -15, -17]:
        target = start + offset

        if not is_valid_knight_move(start, target):
            continue

        target_piece = board[target]
        target_color = -1 if target_piece == 0 else 1 if target_piece >= 17 else 0

        if target_color != color:
            moves.append((start, target, -1))

def determine_bishop_moves(board, moves, start_pos):
    piece = board[start_pos]
    color = -1 if piece == 0 else 1 if piece >= 17 else 0

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
    piece = board[start_pos]
    color = -1 if piece == 0 else 1 if piece >= 17 else 0

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
        piece = board[i]
        piece_color = -1 if piece == 0 else 1 if piece >= 17 else 0
        if piece_color == color:
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
    global OPENING_ISOLATED, ENDING_ISOLATED, OPENING_STACKED, ENDING_STACKED
    start, end, extra = move
    castle_rights = position.castle_rights
    num_pieces = position.pieces
    hash = position.hash
    pawn_hash = position.pawn_hash
    new_board = position.board
    side_to_move = position.side_to_move
    black_pawns = position.black_pawns
    white_pawns = position.white_pawns
    change_white_pawns = []
    change_black_pawns = [] # temporary placeholders to be changed later

    undo = [new_board[end], castle_rights, side_to_move, hash, -1, num_pieces, [position.opening_eval, position.closing_eval, position.phase, position.white_bishops, position.black_bishops, change_white_pawns, change_black_pawns, position.pawn_hash]]

    moved_piece = new_board[start]
    end_piece = new_board[end]

    if moved_piece == 13:
        position.black_king = end

    elif moved_piece == 29:
        position.white_king = end
        
    if extra == -1:

        hash ^= ZOBRIST[moved_piece][start] ^ ZOBRIST[moved_piece][end]

        if end_piece != 0:
            hash ^= ZOBRIST[end_piece][end]
            if not(end_piece in PAWN_NUMBERS) and not(end_piece in KING_NUMBERS):
                position.pieces -= 1  
            elif end_piece in PAWN_NUMBERS:
                pawn_hash ^= PAWN_ZOBRIST[end_piece][end]
                column = end & 7
                if side_to_move:
                    undo[6][6] = [column, -1]
                    black_pawns[column] -= 1
                else:
                    undo[6][5] = [column, -1]
                    white_pawns[column] -= 1

        if moved_piece in PAWN_NUMBERS:
            pawn_hash ^= PAWN_ZOBRIST[moved_piece][start] ^ PAWN_ZOBRIST[moved_piece][end]
            start_column = start & 7
            end_column = end & 7
            if side_to_move:
                undo[6][5] = [start_column, end_column]
                white_pawns[start_column] -= 1
                white_pawns[end_column] += 1
            else:
                undo[6][6] = [start_column, end_column]
                black_pawns[start_column] -= 1
                black_pawns[end_column] += 1

            if end >> 3 == 0: # THis part handles promotions for white
                new_board[end] = 28 
                hash ^= ZOBRIST[moved_piece][end] ^ ZOBRIST[28][end]
                undo[4] = moved_piece

                if end_piece == 0:
                    pawn_hash ^= PAWN_ZOBRIST[moved_piece][start]
                    column = end & 7
                    undo[6][5] = [column, -2]
                    white_pawns[column] -= 1

            elif end >> 3 == 7: # THIs part handles promoitions for black
                new_board[end] = 12
                hash ^= ZOBRIST[moved_piece][end] ^ ZOBRIST[12][end]
                undo[4] = moved_piece

                if end_piece == 0:
                    pawn_hash ^= PAWN_ZOBRIST[moved_piece][start]
                    column = end & 7
                    undo[6][6] = [column, -2]
                    black_pawns[column] -= 1

        hash ^= ZOBRIST_SIDE

        new_board[end] = moved_piece
        new_board[start] = 0
        
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

    position.side_to_move = side_to_move ^ 1
    position.hash = hash
    position.castle_rights = castle_rights
    position.pawn_hash = pawn_hash

    return position, undo

def find_king(board, color):
    for i, piece in enumerate(board):
        if piece == 0:
            continue

        if piece in KING_NUMBERS:
            piece_color = -1 if piece == 0 else 1 if piece >= 17 else 0
            if piece_color == color:
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
                piece_color = -1 if piece == 0 else 1 if piece >= 17 else 0
                if piece_color != color:
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
        target_color = -1 if piece == 0 else 1 if piece >= 17 else 0

        if target_color != color:
            if piece in KNIGHT_NUMBERS:
                return True
        
    return False

def determine_pawn_legality(board, move): # This just makes sure that the pawn move does not go across the board
    start, end, extra = move
    start_col = start % 8
    end_col = end % 8

    if abs(start_col - end_col) != 0:
        end_piece = board[end]
        start_piece = board[start]
        if  -1 != (-1 if end_piece == 0 else 1 if end_piece >= 17 else 0) != (-1 if start_piece == 0 else 1 if start_piece >= 17 else 0):
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
        score += 15000

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
    global OPENING_ISOLATED, ENDING_ISOLATED, OPENING_STACKED, ENDING_STACKED
    white_pawns = [0,0,0,0,0,0,0,0]
    black_pawns = [0,0,0,0,0,0,0,0]

    white_stacked = 0
    black_stacked = 0
    white_isolated = 0
    black_isolated = 0

    pawn_Og_eval = 0
    pawn_eg_eval = 0

    Og_eval = 0
    eg_eval = 0
    phase = 0

    white_bishops = 0
    black_bishops = 0

    hash = 0

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
        if piece == 27 or piece == 30:
            white_bishops += 1
        elif piece == 11 or piece == 14:
            black_bishops += 1

        if 0 < piece < 9:
            hash ^= PAWN_ZOBRIST[piece][i]
            file = i & 7
            black_pawns[file] += 1

        elif 16 < piece < 25:
            hash ^= PAWN_ZOBRIST[piece][i]
            file = i & 7
            white_pawns[file] += 1

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

    for file in range(8):

        w = white_pawns[file]
        b = black_pawns[file]

        if w > 1:
            white_stacked += w - 1

        if b > 1:
            black_stacked += b - 1

        if w:
            left = file > 0 and white_pawns[file - 1]
            right = file < 7 and white_pawns[file + 1]

            if not left and not right:
                white_isolated += w

        if b:
            left = file > 0 and black_pawns[file - 1]
            right = file < 7 and black_pawns[file + 1]

            if not left and not right:
                black_isolated += b

    pawn_Og_eval -= white_isolated * OPENING_ISOLATED
    pawn_eg_eval -= white_isolated * ENDING_ISOLATED

    pawn_Og_eval += black_isolated * OPENING_ISOLATED
    pawn_eg_eval += black_isolated * ENDING_ISOLATED

    pawn_Og_eval -= white_stacked * OPENING_STACKED
    pawn_eg_eval -= white_stacked * ENDING_STACKED

    pawn_Og_eval += black_stacked * OPENING_STACKED # Currently working on adding pawn structure values to evaluate board, such as passed pawns which can be implemented easily into current structure.
    pawn_eg_eval += black_stacked * ENDING_STACKED
 # I separated pawn eval and regular eval so i could save pawn eval as a tuple in hash 

    PH[hash] = (pawn_Og_eval, pawn_eg_eval)

    return Og_eval, eg_eval, phase, white_bishops, black_bishops, white_pawns, black_pawns, hash

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

    position.pieces = undo_info[5]

    position.opening_eval = undo_info[6][0]
    position.closing_eval = undo_info[6][1]
    position.phase = undo_info[6][2]
    position.white_bishops = undo_info[6][3]
    position.black_bishops = undo_info[6][4]
    change_white_pawns = undo_info[6][5]
    change_black_pawns = undo_info[6][6]
    position.pawn_hash = undo_info[6][7]

    white_pawns = position.white_pawns
    black_pawns = position.black_pawns

    if change_white_pawns != []: # (start column, end column and identifier) if identifier = -1 captured piece -2 promotion anything else means its the actual ending file
        start, end = change_white_pawns
        if end >= 0:
            white_pawns[end] -= 1
            white_pawns[start] += 1
        elif end == -1 or end == -2:
            white_pawns[start] += 1

    if change_black_pawns != []:
        start, end = change_black_pawns
        if end >= 0:
            black_pawns[end] -= 1
            black_pawns[start] += 1
        elif end == -1 or end == -2:
            black_pawns[start] += 1

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

def count_non_pawn_or_king(board): # This just counts the number of non pawn and non king pieces in a board. Used for Null move pruning.
    pieces = 0
    
    for value in board:
        if not(value in PAWN_NUMBERS) and not(value in KING_NUMBERS):
            pieces += 1

    return pieces

def recurse(position, depth, alpha, beta, maximizing, allow_null_move):
    found_legal_move = False
    global TT_LOOKUPS, TT_HITS, NUMBER_OF_RECURSIONS
    board = position.board
    NUMBER_OF_RECURSIONS += 1

    if depth == 0:
        eval = position.update_evaluation((), [], True)
        return eval

    first_move = True
    num_pieces = position.pieces
    best_move = None
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
            
        entry_move = entry_move if (entry_depth <= depth) else None

    if (allow_null_move and depth >= REDUCTION_FACTOR + 1 and not(is_square_attacked(position.white_king if position.side_to_move else position.black_king, board, position.side_to_move)) and num_pieces != 0):
        position.side_to_move ^= 1
        position.hash ^= ZOBRIST_SIDE
        
        if maximizing:
            score = recurse(
                position,
                depth - 1 - REDUCTION_FACTOR,
                beta - 1,
                beta, 
                maximizing ^ 1,
                False
                )
        else:
            score = recurse(
                position,
                depth - 1 - REDUCTION_FACTOR,
                alpha,
                alpha + 1,
                maximizing ^ 1,
                False
            )

        position.side_to_move ^= 1
        position.hash ^= ZOBRIST_SIDE

        if maximizing:
            if score >= beta:
                return beta
        else:
            if score <= alpha:
                return alpha
        


    all_moves = create_pseudo_moves(
        board,
        position.side_to_move,
        position.castle_rights,
    )

    scored_moves = create_scored_moves(position, all_moves, depth, entry_move)

    best = -99999999 if maximizing else 99999999

    for _, move in scored_moves:
        start, end, extra = move
        captured_piece = board[end]
        temp_position, undo_info = make_move(position, move) # Initial king square is the king square of the side we want to make the move. SO, if black is moving, black king

        if not(temp_position.side_to_move): # We swap which side we look at because when the move made was done on blacks side, then temp_position side becomes white, since black moved. Swap to get the side that just moved to check if legal
            if is_square_attacked(temp_position.white_king, temp_position.board, 1):
                undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well
                continue
        else:
            if is_square_attacked(temp_position.black_king, temp_position.board, 0):
                undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well
                continue

        position.update_evaluation(move, undo_info)

        found_legal_move = True

        if first_move:
            score = recurse(
                temp_position,
                depth-1,
                alpha,
                beta,
                not maximizing,
                allow_null_move
            )

            first_move = False

            if maximizing:
                alpha = max(alpha, score)

                if score > best:
                    best = score
                    best_move = move
            else:
                beta = min(beta, score)

                if score < best:
                    best = score
                    best_move = move

            undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well

            if alpha >= beta:
                break

        else:
            if maximizing:
                score = recurse(
                    temp_position,
                    depth-1,
                    alpha,
                    alpha+1,
                    False,
                    allow_null_move
                )

                if score > alpha_orig and score < beta:
                    score = recurse(
                        temp_position,
                        depth-1,
                        alpha,
                        beta,
                        False,
                        allow_null_move
                    )

                if score > best:
                    best = score
                    best_move = move

                alpha = max(alpha, score)

                undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well

                if beta <= alpha:
                    # store killer move (only if it's quiet)
                    start, end, extra = move

                    history[start][end] += depth * depth

                    if captured_piece == 0 and not (board[start] in PAWN_NUMBERS and (end // 8 in (0,7))):  # quiet move
                        if move != killer_moves[depth][0]:
                            killer_moves[depth][1] = killer_moves[depth][0]
                            killer_moves[depth][0] = move

                    
                    break

            else:
                score = recurse(
                    temp_position,
                    depth-1,
                    beta-1,
                    beta,
                    True,
                    allow_null_move
                )

                if score < beta_orig and score > alpha:
                    score = recurse(
                        temp_position,
                        depth-1,
                        alpha,
                        beta,
                        True,
                        allow_null_move
                    )

                
                if score < best:
                    best = score
                    best_move = move

                beta = min(beta, score)

                undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well

                if beta <= alpha:
                    # store killer move (only if it's quiet)
                    start, end, extra = move

                    history[start][end] += depth * depth

                    if captured_piece == 0 and not (board[start] in PAWN_NUMBERS and (end // 8 in (0,7))):  # quiet move
                        if move != killer_moves[depth][0]:
                            killer_moves[depth][1] = killer_moves[depth][0]
                            killer_moves[depth][0] = move

                    break
                
    if not found_legal_move: # if legal_move is still false, meaning no legal moves were found
        if maximizing and is_square_attacked(position.white_king, board, 1):
            best = -99999999
        elif not(maximizing) and is_square_attacked(position.black_king, board, 0):
                best = -99999999
        else:
            best = 0
    
    flag = "EXACT"

    if best <= alpha_orig:
        flag = "UPPER"
    elif best >= beta_orig:
        flag = "LOWER"  

    if entry is None or depth >= entry_depth:
        TT[position.hash] = (depth, best, flag, best_move)
    
    return best

def find_best_move(position, depth, starting_move):
    global TT_LOOKUPS, TT_HITS, NUMBER_OF_RECURSIONS
    alpha = -99999999
    beta = 99999999
    side = position.side_to_move    

    alpha_orig = alpha
    beta_orig = beta
    entry_move = None
    entry = TT.get(position.hash)
    first_move = True
    board = position.board
    found_legal_move = False

    if entry is not None:  
        TT_LOOKUPS += 1
        entry_depth, entry_score, entry_flag, entry_move = entry

        if entry_depth >= depth:
            if entry_flag == "EXACT":
                TT_HITS += 1
                return entry_move
            elif entry_flag == "LOWER":
                alpha = max(alpha, entry_score)
            elif entry_flag == "UPPER":
                beta = min(beta, entry_score)

            if alpha >= beta:
                TT_HITS += 1
                return entry_move
            
    all_moves = create_pseudo_moves(
        board,
        side,
        position.castle_rights,
    )

    scored_moves = create_scored_moves(position, all_moves, depth, starting_move)
    best_move = None
    best_eval = -99999999 if side else 99999999

    for _, move in scored_moves:
        start, end, extra = move
        captured_piece = board[end]
        temp_position, undo_info = make_move(position, move) # Initial king square is the king square of the side we want to make the move. SO, if black is moving, black king

        if not(temp_position.side_to_move): # We swap which side we look at because when the move made was done on blacks side, then temp_position side becomes white, since black moved. Swap to get the side that just moved to check if legal
            if is_square_attacked(temp_position.white_king, temp_position.board, 1):
                undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well
                continue
        else:
            if is_square_attacked(temp_position.black_king, temp_position.board, 0):
                undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well
                continue

        found_legal_move = True
        position.update_evaluation(move, undo_info)

        if first_move:
            score = recurse(
                temp_position,
                depth-1,
                alpha,
                beta,
                not side,
                True
            )

            first_move = False

            if side:
                alpha = max(alpha, score)

                if score > best_eval:
                    best_eval = score
                    best_move = move
            else:
                beta = min(beta, score)

                if score < best_eval:
                    best_eval = score
                    best_move = move

            undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well

            if alpha >= beta:
                break

        else:
            if side:
                score = recurse(
                    temp_position,
                    depth-1,
                    alpha,
                    alpha+1,
                    False,
                    True
                )

                if score > alpha_orig and score < beta:
                    score = recurse(
                        temp_position,
                        depth-1,
                        alpha,
                        beta,
                        False,
                        True
                    )

                if score > best_eval:
                    best_eval = score
                    best_move = move

                alpha = max(alpha, score)

                undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well

                if beta <= alpha:
                    # store killer move (only if it's quiet)
                    start, end, extra = move

                    history[start][end] += depth * depth

                    if captured_piece == 0 and not (board[start] in PAWN_NUMBERS and (end // 8 in (0,7))):  # quiet move
                        if move != killer_moves[depth][0]:
                            killer_moves[depth][1] = killer_moves[depth][0]
                            killer_moves[depth][0] = move

                    
                    break

            else:
                score = recurse(
                    temp_position,
                    depth-1,
                    beta-1,
                    beta,
                    True,
                    True
                )

                if score < beta_orig and score > alpha:
                    score = recurse(
                        temp_position,
                        depth-1,
                        alpha,
                        beta,
                        True,
                        True
                    )

                
                if score < best_eval:
                    best_eval = score
                    best_move = move

                beta = min(beta, score)

                undo_move(position, move, undo_info) # undo move undoes the creation of the new king square as well

                if beta <= alpha:
                    # store killer move (only if it's quiet)
                    start, end, extra = move

                    history[start][end] += depth * depth

                    if captured_piece == 0 and not (board[start] in PAWN_NUMBERS and (end // 8 in (0,7))):  # quiet move
                        if move != killer_moves[depth][0]:
                            killer_moves[depth][1] = killer_moves[depth][0]
                            killer_moves[depth][0] = move

                    break

    if not found_legal_move: # if legal_move is still false, meaning no legal moves were found
        if side and is_square_attacked(position.white_king, board, 1):
            best_eval = -99999999
        elif not(side) and is_square_attacked(position.black_king, board, 0):
                best_eval = -99999999
        else:
            best_eval = 0

    flag = "EXACT"

    if best_eval <= alpha_orig:
        flag = "UPPER"
    elif best_eval >= beta_orig:
        flag = "LOWER"  

    if entry is None or depth >= entry_depth:
        TT[position.hash] = (depth, best_eval, flag, best_move)

    return best_move

opening_eval, closing_eval, phase, white_bishops, black_bishops, white_pawns, black_pawns, pawn_hash = evaluate_board(board)

position = Position(
    board,
    1,
    initial_castle_rights,
    compute_hash(board, 1, initial_castle_rights),
    find_king(board, 0),
    find_king(board, 1),
    count_non_pawn_or_king(board),
    
    opening_eval,
    closing_eval,
    phase,
    white_bishops == 2, 
    black_bishops == 2,
    black_pawns,
    white_pawns,
    pawn_hash
)
previous_best_move = None

start_time = time.perf_counter()
for i in range(1, 9):
    previous_best_move = find_best_move(position, i, previous_best_move)
    print("DEPTH: ", i, "MOVE: ", previous_best_move)
end_time = time.perf_counter()

print("TIME TAKEN: ", end_time - start_time)
print(previous_best_move)


print("TTS HITS: ", TT_HITS, " TT LOOKUPS: ", TT_LOOKUPS, " RECURSIONS: ", NUMBER_OF_RECURSIONS, " ELEMENTS IN TT: ", len(TT.values()))

"""print(evaluate_board(board)) #evaluatoin is behaving weirdly. White pieces should increase evaluation, however they end up decreasing it somehow.
Position = Position(board, 0, initial_castle_rights)

a = create_pseudo_moves(Position.board, 0, Position.castle_rights, False)

print(determine_legal_moves(Position, a))"""


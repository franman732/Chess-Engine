import numpy as np # THis is intended to maximize white, minimize black. Be able to set turn so it doesnt matter, and always set urself as white.

pieces = {0:"no", 1:"pawn", 2:"pawn", 3:"pawn", 4:"pawn", 5:"pawn", 6:"pawn", 7:"pawn", 8:"pawn", 9:"rook", 10:"knight", 11:"bishop", 12:"queen", 13:"king", 14:"bishop", 15:"knight", 16:"rook", #lowercase is black, capital is white
          17:"PAWN", 18:"PAWN", 19:"PAWN", 20:"PAWN", 21:"PAWN", 22:"PAWN", 23:"PAWN", 24:"PAWN", 25:"ROOK", 26:"KNIGHT", 27:"BISHOP", 28:"QUEEN", 29:"KING", 30:"BISHOP", 31:"KNIGHT", 32:"ROOK"} #Black is 0, white is 1

Opiece_values = [0, -100, -100, -100, -100, -100, -100, -100, -100, -500, -320, -330, -900, -20000, -330, -320, -500, 100, 100, 100, 100, 100, 100, 100, 100, 500, 320, 330, 900, 20000, 330, 320, 500]
Epiece_values = [0, -120, -120, -120, -120, -120, -120, -120, -120, -520, -300, -340, -900, -20000, -340, -300, -520, 120, 120, 120, 120, 120, 120, 120, 120, 520, 300, 340, 900, 20000, 340, 300, 520]

phase_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 1, 2]

board = np.array([9, 10, 11, 12, 13, 14, 15, 16, # top is black/lowercase/0 ; bottom is white/uppercase/1
                 1, 2, 3, 0, 0, 6, 7, 8,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 4, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
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


knight_moves = [6, 10, 15, 17, -6, -10, -15, -17]

ROOK_DIRECTIONS = [-1, 1, -8, 8]

class Position:
    def __init__(self, board, side_to_move, castle_rights):
        self.board = board
        self.side_to_move = side_to_move
        self.castle_rights = castle_rights

def get_color(board, index):
    if board[index] == 0:
        return -1
    if pieces[board[index]].lower() == pieces[board[index]]:
        return 0
    else:
        return 1

def determine_capturable(board, end, color):
    if end < 0 or end > 63:
        return False
    
    if -1 != get_color(board, end) != color:
        return True
    else:
        return False

def determine_pawn_moves(board, moves, start, ignore_pawn_forwards = False): #Pawn is done. First section includes forwards movements, second section includes capture moves
    color = get_color(board, start)
    if color == 0:
        if not ignore_pawn_forwards: # WHen ignore_pawn_forwards is true, we want to ignore these moves
            if ((1 == start // 8) and board[start + 16] == 0 and board[start + 8] == 0):
                moves.append((start, start + 16))
                moves.append((start, start + 8))
            elif board[start + 8] == 0:
                moves.append((start, start + 8))
        
        if is_valid_pawn_move(start, start + 7):
            moves.append((start, start + 7))
        if is_valid_pawn_move(start, start + 9):
            moves.append((start, start + 9))

    elif color == 1:
        if not ignore_pawn_forwards: # WHen ignore_pawn_forwards is true, we want to ignore these moves
            if ((start // 8 == 6)) and board[start - 16] == 0 and board[start - 8] == 0:
                moves.append((start, start - 16))
                moves.append((start, start - 8))
            elif board[start - 8] == 0: 
                moves.append((start, start - 8))

        if is_valid_pawn_move(start, start - 7):
            moves.append((start, start - 7))
        if is_valid_pawn_move(start, start - 9):
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

    for direction in ROOK_DIRECTIONS:
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

    for offset in knight_moves:
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
                        psudo_moves = create_pseudo_moves(board, 1, True, None)
                        if (not is_square_attacked(board, 4, 1, psudo_moves) and
                            not is_square_attacked(board, 5, 1, psudo_moves) and
                            not is_square_attacked(board, 6, 1, psudo_moves)):
                            moves.append((4, 6, 0))

            if castle_rights[1]: # queenside
                if board[1] == 0 and board[2] == 0 and board[3] == 0:
                    if board[0] == 9:
                        psudo_moves = create_pseudo_moves(board, 1, True, None) if psudo_moves == None else psudo_moves
                        if (not is_square_attacked(board, 4, 1, psudo_moves) and
                            not is_square_attacked(board, 3, 1, psudo_moves) and
                            not is_square_attacked(board, 2, 1, psudo_moves)):
                            moves.append((4, 2, 1))
                            
        elif color == 1:
            if castle_rights[2]: # kingside
                if board[61] == 0 and board[62] == 0:
                    if board[63] == 32:
                        psudo_moves = create_pseudo_moves(board, 0, True, None)
                        if (not is_square_attacked(board, 60, 0, psudo_moves) and
                            not is_square_attacked(board, 61, 0, psudo_moves) and
                            not is_square_attacked(board, 62, 0, psudo_moves)):
                            moves.append((60, 62, 2))

            if castle_rights[3]: # queenside
                if board[59] == 0 and board[58] == 0 and board[57] == 0:
                    if board[56] == 25:
                        psudo_moves = create_pseudo_moves(board, 0, True, None) if psudo_moves == None else psudo_moves
                        if (not is_square_attacked(board, 60, 0, psudo_moves) and
                            not is_square_attacked(board, 59, 0, psudo_moves) and
                            not is_square_attacked(board, 58, 0, psudo_moves)):
                            moves.append((60, 58, 3))

def create_pseudo_moves(board, color, ignore_pawn_forwards, castle_rights): # takes a board state, and returns all possible moves, legal and illegal, given that position; ALso, returns only legal castle moves... whoops
    moves = [] #(start_position, end_position) position is by index number 
    for i, value in enumerate(board):
        if get_color(board, i) == color:
            if pieces[value].lower() == "pawn":
                determine_pawn_moves(board, moves, i, ignore_pawn_forwards) #ignore_pawn_forwards is for ignoring them when determining attacked squares

            elif pieces[value].lower() == "rook":
                determine_rook_moves(board, moves, i)

            elif pieces[value].lower() == "knight":
                determine_knight_moves(board, moves, i)

            elif pieces[value].lower() == "bishop":
                determine_bishop_moves(board, moves, i)

            elif pieces[value].lower() == "queen":
                determine_queen_moves(board, moves, i)

            elif pieces[value].lower() == "king":
                determine_king_moves(board, moves, i, castle_rights)
    return moves

def make_move(position, move): # all determination of whether a move is legal should be done before make_move. Make_move simply returns a board with the move made, and is used to determine if a move puts a king in check or not.
    start, end, *extra = move
    castle_rights = position.castle_rights.copy()

    new_board = position.board.copy()

    if extra == []:

        moved_piece = new_board[start]
        end_piece = new_board[end]

        new_board[end] = moved_piece
        new_board[start] = 0
        
        if pieces[moved_piece].lower() == "pawn": # If it is a pawn promotion, turn it into a queen
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

    return position

def find_king(board, color):
    for i, piece in enumerate(board):
        if piece == 0:
            continue

        name = pieces[piece].lower()

        if name == "king":
            if get_color(board, i) == color:
                return i

    return -1

def is_square_attacked(board, square, enemy_color, moves = None):
    enemy_moves = create_pseudo_moves(board, enemy_color, True, empty_castle_rights) if moves is None else moves # True makes create_pseudo_moves ignore forward moves for the pawn

    for start, end, *extra in enemy_moves:
        if end == square:
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

def determine_legal_moves(position, all_moves): #Takes a board and psudo moves for that board, and returns a complete set of legal moves for that board.
    legal_moves = []

    for move in all_moves:
        start, end, *extra = move
        board = position.board
        castle_rights = position.castle_rights

        moving_color = get_color(board, start)

        # make temporary board
        temp_board = make_move(position, move).board

        # find own king after move
        king_square = find_king(temp_board, moving_color)

        # enemy color
        enemy_color = 1 if moving_color == 0 else 0

        # if king NOT attacked then legal
        if not is_square_attacked(temp_board, king_square, enemy_color):
            if pieces[board[start]].lower() == "pawn":
                if determine_pawn_legality(board, move):
                    legal_moves.append(move)
            else:
                legal_moves.append(move)

        position.board = board
        position.castle_rights = castle_rights

    return legal_moves

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


        print("Piece: ", piece, " Opst: ", Opst[piece][table_index], " Epst: ", Epst[piece][table_index], " OPIECE: ", Opiece_values[piece], " Epiece: ", Epiece_values[piece])
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

print(evaluate_board(board)) #evaluatoin is behaving weirdly. White pieces should increase evaluation, however they end up decreasing it somehow.


# use make_move to create a board. Evaluate board takes a current board state and returns the evaluation. determine legal moves takes psudo moves and returns all legal moves
# pipeline would be start with initial board, produce all possible moves then convert to all legal moves using make_move, then make every legal move using make_move and evaluate them, and then start branching, and when a castle move is
# made, update the passed position object's castle_legal property to false.
# Also remember, if king or rook is moved, invalidate castle_legal properties for that object.

Position = Position(board, 0, initial_castle_rights)

all_moves = create_pseudo_moves(Position.board, 0, False, Position.castle_rights)
print(determine_legal_moves(Position, all_moves))
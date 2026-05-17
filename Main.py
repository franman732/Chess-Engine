import numpy as np

pieces = {0:"no", 1:"pawn", 2:"pawn", 3:"pawn", 4:"pawn", 5:"pawn", 6:"pawn", 7:"pawn", 8:"pawn", 9:"rook", 10:"knight", 11:"bishop", 12:"queen", 13:"king", 14:"bishop", 15:"knight", 16:"rook", #lowercase is black, capital is white
          17:"PAWN", 18:"PAWN", 19:"PAWN", 20:"PAWN", 21:"PAWN", 22:"PAWN", 23:"PAWN", 24:"PAWN", 25:"ROOK", 26:"KNIGHT", 27:"BISHOP", 28:"QUEEN", 29:"KING", 30:"BISHOP", 31:"KNIGHT", 32:"ROOK"} #Black is 0, white is 1

piece_values = {"pawn": 1, "bishop": 3, "knight": 3, "rook": 5, "queen": 9}

board = np.array([9, 10, 11, 12, 13, 14, 15, 16, # top is black/lowercase/0 ; bottom is white/uppercase/1
                 1, 2, 3, 0, 5, 6, 7, 8,
                 0, 0, 0, 0, 20, 0, 0, 0,
                 0, 0, 0, 4, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 17, 18, 19, 0, 21, 22, 23, 24,
                 25, 26, 27, 28, 29, 30, 31, 32])

knight_moves = [6, 10, 15, 17, -6, -10, -15, -17]

ROOK_DIRECTIONS = [-1, 1, -8, 8]

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

def determine_pawn_moves(board, moves, start): #Pawn is done. First section includes forwards movements, second section includes capture moves
    color = get_color(board, start)
    if color == 0:
        if ((1 == start // 8) and board[start + 16] == 0 and board[start + 8] == 0):
            moves.append((start, start + 16))
            moves.append((start, start + 8))
        elif board[start + 8] == 0:
            moves.append((start, start + 8))

        moves.append((start, start + 7))
        moves.append((start, start + 9))

    elif color == 1:
        if ((start // 8 == 6)) and board[start - 16] == 0 and board[start - 8] == 0:
            moves.append((start, start - 16))
            moves.append((start, start - 8))
        elif board[start - 8] == 0: 
            moves.append((start, start - 8))

        moves.append((start, start - 7))
        moves.append((start, start - 9))

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

def determine_king_moves(board, moves, start_pos):
    color = get_color(board, start_pos)

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

def create_psudo_moves(board, color): # takes a board state, and returns all possible moves, legal and illegal, given that position
    moves = [] #(start_position, end_position) position is by index number 
    for i, value in enumerate(board):
        if get_color(board, i) == color:
            if pieces[value].lower() == "pawn":
                determine_pawn_moves(board, moves, i)

            elif pieces[value].lower() == "rook":
                determine_rook_moves(board, moves, i)

            elif pieces[value].lower() == "knight":
                determine_knight_moves(board, moves, i)

            elif pieces[value].lower() == "bishop":
                determine_bishop_moves(board, moves, i)

            elif pieces[value].lower() == "queen":
                determine_queen_moves(board, moves, i)

            elif pieces[value].lower() == "king":
                determine_king_moves(board, moves, i)
    return moves

def make_move(board, move):
    start, end = move

    new_board = board.copy()

    new_board[end] = new_board[start]
    new_board[start] = 0

    return new_board

def find_king(board, color):
    for i, piece in enumerate(board):
        if piece == 0:
            continue

        name = pieces[piece].lower()

        if name == "king":
            if get_color(board, i) == color:
                return i

    return -1

def is_square_attacked(board, square, enemy_color):
    enemy_moves = create_psudo_moves(board, enemy_color)

    for start, end in enemy_moves:
        if end == square:
            return True
    
    return False

def determine_pawn_legality(board, move):
    start, end = move
    start_col = start % 8
    end_col = end % 8

    if abs(start_col - end_col) != 0:
        if  -1 != get_color(board, end) != get_color(board, start):
            return True
    else:
        return True

    return False

def determine_legal_moves(board, all_moves):
    legal_moves = []

    for move in all_moves:
        start, end = move

        moving_color = get_color(board, start)

        # make temporary board
        temp_board = make_move(board, move)

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

    return legal_moves


all_moves = create_psudo_moves(board, 0)
print(determine_legal_moves(board, all_moves))
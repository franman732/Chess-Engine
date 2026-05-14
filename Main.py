import numpy as np

pieces = {0:"no", 1:"pawn", 2:"pawn", 3:"pawn", 4:"pawn", 5:"pawn", 6:"pawn", 7:"pawn", 8:"pawn", 9:"rook", 10:"knight", 11:"bishop", 12:"queen", 13:"king", 14:"bishop", 15:"knight", 16:"rook", #lowercase is black, capital is white
          17:"PAWN  ", 18:"PAWN", 19:"PAWN", 20:"PAWN", 21:"PAWN", 22:"PAWN", 23:"PAWN", 24:"PAWN", 25:"ROOK", 26:"KNIGHT", 27:"BISHOP", 28:"QUEEN", 29:"KING", 30:"BISHOP", 31:"KNGIHT", 32:"ROOK"} #Black is 0, white is 1

board = np.array([9, 10, 11, 12, 13, 14, 15, 16, # top is black/lowercase/0 ; bottom is white/uppercase/1
                 1, 2, 3, 4, 5, 6, 7, 8,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 17, 18, 19, 20, 21, 22, 23, 24,
                 25, 26, 27, 28, 29, 30, 31, 32])

knight_moves = [6, 10, 15, 17, -6, -10, -15, -17]

ROOK_DIRECTIONS = [-1, 1, -8, 8]

def get_color(board, index):
    if board[index] == 0:
        return -1
    if pieces[board(index)].lower == pieces[board(index)]:
        return 0
    else:
        return 1

def determine_capturable(board, end, color):
    if get_color(board(end)) != color:
        return True
    else:
        return False

def determine_pawn_moves(board, moves, start): #Pawn is done. First section includes forwards movements, second section includes capture moves
    color = get_color(board, start)
    if color == 0:
        if ((1 == start // 8) and board(start + 16) == 0 and board(start + 8) == 0):
            moves.append((start, start + 16))
            moves.append((start, start + 8))
        elif board(start + 8) == 0:
            moves.append((start, start + 8))

        if determine_capturable(board, (start + 7), color):
            moves.append((start, start + 7))
        elif determine_capturable(board, (start + 7), color):
            moves.append((start, start + 9))

    elif color == 1:
        if ((start // 8 == 6)) and board(start - 16) == 0 and board(start - 8) == 0:
            moves.append((start, start - 16))
            moves.append((start, start - 8))
        elif board(start - 8) == 0: 
            moves.append((start, start - 8))

        if determine_capturable(board, (start + 7), color):
            moves.append((start, start + 7))
        elif determine_capturable(board, (start + 9), color):
            moves.append((start, start + 9))

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
                if get_color(piece) != color:
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
        target_color = get_color(piece)

        if target_color != color:
            moves.append((start, target))

def determine_bishop_moves(board, moves, start):
    col = start % 8
    row = start // 8

    counter = 1
    while ((col != 8 and row != 8) and 

def determine_queen_moves(board, moves, start):
    return

def determine_king_moves(board, moves, start):
    return

def create_psudo_moves(board): # takes a board state, and returns all possible moves, legal and illegal, given that position
    moves = [] #(start_position, end_position) position is by index number 
    for i, value in enumerate(board):
        if pieces[value].lower == "pawn":
            determine_pawn_moves(board, moves, i)

        elif pieces[value].lower == "rook":
            determine_rook_moves(board, moves, i)

        elif pieces[value].lower == "knight":
            determine_knight_moves(board, moves, i)

        elif pieces[value].lower == "bishop":
            determine_bishop_moves(board, moves, i)

        elif pieces[value].lower == "queen":
            determine_queen_moves(board, moves, i)

        elif pieces[value].lower == "king":
            determine_king_moves(board, moves, i)
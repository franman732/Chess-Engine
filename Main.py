import numpy as np

pieces = {0:"no", 1:"pawn", 2:"pawn", 3:"pawn", 4:"pawn", 5:"pawn", 6:"pawn", 7:"pawn", 8:"pawn", 9:"rook", 10:"knight", 11:"bishop", 12:"queen", 13:"king", 14:"bishop", 15:"knight", 16:"rook", #lowercase is black, capital is white
          17:"PAWN  ", 18:"PAWN", 19:"PAWN", 20:"PAWN", 21:"PAWN", 22:"PAWN", 23:"PAWN", 24:"PAWN", 25:"ROOK", 26:"KNIGHT", 27:"BISHOP", 28:"QUEEN", 29:"KING", 30:"BISHOP", 31:"KNGIHT", 32:"ROOK"} #Black is 0, white is 1

board = np.array(9, 10, 11, 12, 13, 14, 15, 16, # top is black/lowercase/0 ; bottom is white/uppercase/1
                 1, 2, 3, 4, 5, 6, 7, 8,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0,
                 17, 18, 19, 20, 21, 22, 23, 24,
                 25, 26, 27, 28, 29, 30, 31, 32)

def get_color(board, index):
    if board[index] == 0:
        return -1
    if pieces[board(index)].lower == pieces[board(index)]:
        return 0
    else:
        return 1

def determine_pawn_moves(board, moves, start):
    color = get_color(board, start)
    if color == 0:
        if ((1 == start // 8) and board(start + 16) == 0 and board(start + 8) == 0):
            moves.append(start, start + 16)
            moves.append(start, start + 8)
        elif board(start + 8) == 0:
            moves.append(start, start + 8)

        if 
    elif color == 1:
        if ((start // 8 == 6 and color == 1)) and board(start - 16) == 0 and board(start - 8) == 0:
            moves.append(start, start - 16)
            moves.append(start, start - 8)
        elif board(start - 8) == 0: 
            moves.append(start, start - 8)
    elif 

def determine_rook_moves(board, moves, start):
    col = start % 8 
    while col >= 0:
        if moves.append(start, start - 1)
        col -= 1

    col = start % 8 
    while col <= 8:
        moves.append(start, start + 1)
        col += 1

    row = start // 8
    while row >= 0:
        moves.append()

def determine_knight_moves(board, moves, start):
    return

def determine_bishop_moves(board, moves, start):
    return

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
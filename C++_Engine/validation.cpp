#include "validation.h"
#include "helper_functions.h"
#include "moves.h"
#include "tables.h"
#include "aliases.h"

bool is_square_attacked(int square, const Board& board, int color) {
    int sqRow = SQUARE_ROW[square];

    for (const std::array<int, 7>& ray : DIAGONAL_RAYS[square]) {
        int counter = 0;
        for (int idx : ray) {
            int value = board[idx];
            counter += 1;
            if ((value == 0) || idx == -1) {
                continue;
            }

            int pieceColor = -1;

            if (value >= 17) {
                pieceColor = 1;   // white
            } else if (value > 0) {
                pieceColor = 0;   // black
            }

            if (pieceColor != color) {
                int piece = PIECES[value]; 
                if ((piece == BISHOP_NUMBER) || (piece == QUEEN_NUMBER)) {
                    return true;
                } if ((piece == KING_NUMBER) && (counter == 1)) {
                    return true;
                } if (piece == PAWN_NUMBER) {
                    if ((pieceColor == 0) && ((SQUARE_ROW[idx] - sqRow) == -1)) {
                        return true;
                    }
                    if ((pieceColor == 1) && ((SQUARE_ROW[idx] - sqRow) == 1)) {
                        return true;
                    }
                }
            }

            break;
        }
    }

    for (const std::array<int, 7>& ray : STRAIGHT_RAYS[square]) {
        int counter = 0;
        for (int idx : ray) {
            int value = board[idx];
            counter += 1;
            if ((value == 0) || idx == 0) {
                continue;
            }

            int pieceColor = -1;

            if (value == 0) {
                pieceColor = 1;
            } else if (value >= 17) {
                pieceColor = 0;
            }

            if (pieceColor != color) {
                int piece = PIECES[value];
                if ((piece == ROOK_NUMBER) || (piece == QUEEN_NUMBER)) {
                    return true;
                } if ((piece == KING_NUMBER) && (counter == 1)) {
                    return true;
                }
            }

            break;
        }
    }

    for (int idx : KNIGHT_ATTACKS[square]) {
        int value = board[idx];
        if (value != 0) {
            int pieceColor = -1;

            if (value == 0) {
                pieceColor = 1;
            } else if (value >= 17) {
                pieceColor = 0;
            }

            if (pieceColor != color) {
                if (PIECES[value] == KNIGHT_NUMBER) {
                    return true;
                }
            }
        }
    }

    return false;
}

bool determine_capturable(const Board& board, int end, int color) {
    if ((end < 0) || (end >= 64)) {
        return false;
    }

    int piece = board[end];
    int piece_color = -1;

    if (piece == 0) {
        piece_color = 1;
    } else if (piece >= 17) {
        piece_color = 0;
    }
    
    if ((-1 != piece_color) && (piece_color != color)){
        return true;
    } else{
        return false;
    }
}

#include "initialization.h"
#include "aliases.h"
#include "transposition_table.h"
#include "position.h"

#include <unordered_map>
#include <array>
#include <iostream>

std::unordered_map<int, int> determine_piece_squares(const Board& board) {
    std::unordered_map<int, int> piecePositions;

    for (int i = 0; i <64; ++i) {
        int value = board[i];
        if (value != 0) {
            std::cout << "WE INCREASING PIECE POSITIONS\n";
            piecePositions[i] = value;
        }
    }

    return piecePositions;
}

int compute_hash(const Board& board, int sideToMove, int castle) {
    int h = 0;

    int counter = 0;
    for (int piece : board) {
        if (piece != 0){
            h ^= ZOBRIST[piece][counter];
        }
        counter += 1;
    }

    if (sideToMove == 1) {
        h ^= ZOBRIST_SIDE;
    }

    if (castle & WK) {
        h ^= ZOBRIST_CASTLE[WK];
    }
    if (castle & WQ) {
        h ^= ZOBRIST_CASTLE[WQ];
    }
    if (castle & BK) {
        h ^= ZOBRIST_CASTLE[BK];
    }
    if (castle & BQ) {
        h ^= ZOBRIST_CASTLE[BQ];
    }

    return h;
}   

int count_pieces(const Board& board) {
    int pieces = 0;

    for (int value : board) {
        if ((PIECES[value] != PAWN_NUMBER) && (PIECES[value] != KING_NUMBER)) {
            pieces += 1;
        }
    }

    return pieces;
}

int find_king(const Board& board, int color) {
    int kingColor = 0;
    
    for (int i = 0; i < 64; i++) {
        int piece = board[i];

        if (piece == 0) {
            continue;
        }

        if (PIECES[piece] == KING_NUMBER) {
            if (piece == 0) {
                kingColor = -1;
            } else if (piece >= 17) {
                kingColor = 1;
            } else {
                kingColor = 0;
            }
        }

        if (kingColor == color) {
            return i;
        }
    }

    return -1;
}
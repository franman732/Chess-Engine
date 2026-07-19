#include "position.h"
#include "initialization.h"
#include "psuedo_move_generation.h"
#include "aliases.h"
#include "evaluation.h"
#include "search.h"
#include "transposition_table.h"

#include <tuple>
#include <array>
#include <iostream>
#include <vector>

int main() {
    std::cout << "Program started\n";
    Board board = {9, 10, 11, 12, 13, 14, 15, 16, // top is black/lowercase/0 ; bottom is white/uppercase/1
                                1, 2, 3, 0, 0, 6, 7, 8,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 20, 0, 0, 0,
                                0, 0, 0, 4, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                17, 18, 19, 0, 21, 22, 23, 24,
                                25, 26, 27, 28, 29, 30, 31, 32};
    int sideToMove = 1; 
    int castleRights = 15;
    
    evaluation initialQualities = evaluate_board(board);

    Position pos;

    pos.board = board;
    pos.sideToMove = sideToMove; // 1 is white, 0 is black; bottom is white, top is black
    pos.castleRights = castleRights; // 15 is 1111 in binary, which means all castles are legal.
    pos.hash = compute_hash(board, sideToMove, castleRights);
    pos.blackKing = find_king(board, 0);
    pos.whiteKing = find_king(board, 1);
    pos.pieces = count_pieces(board);
    
    pos.evalInfo = initialQualities;

    pos.pieceLocations = determine_piece_squares(board);

    AMove previousBestMove = {-1, -1, -1};

    TT_tracker tracker = {0, 0, 0};

    std::cout << "Generating Pseudo Moves\n";
    for (int i = 1; i < 11; i ++) {
        AMove previousBestMove = Find_Best_Move(pos, i, previousBestMove, tracker);
        std::cout << "DEPTH: " << i
                    << " MOVE: ("
                    << std::get<0>(previousBestMove) << ", "
                    << std::get<1>(previousBestMove) << ", "
                    << std::get<2>(previousBestMove) << ")\n";
    }

    std::cout << std::get<0>(previousBestMove) << ", "
            << std::get<1>(previousBestMove) << ", "
            << std::get<2>(previousBestMove) << ")\n";
}

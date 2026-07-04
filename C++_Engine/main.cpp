#include "position.h"
#include "initialization.h"
#include "psuedo_move_generation.h"

#include <tuple>
#include <array>
#include <iostream>
#include <vector>

int main() {
    std::cout << "Program started\n";
    std::array<int, 64> board = {9, 10, 11, 12, 13, 14, 15, 16, // top is black/lowercase/0 ; bottom is white/uppercase/1
                                1, 2, 3, 0, 0, 6, 7, 8,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 20, 0, 0, 0,
                                0, 0, 0, 4, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0,
                                17, 18, 19, 0, 21, 22, 23, 24,
                                25, 26, 27, 28, 29, 30, 31, 32};
    int sideToMove = 1; 
    int castleRights = 15;
    
    Position pos;

    pos.sideToMove = sideToMove; // 1 is white, 0 is black; bottom is white, top is black
    pos.castleRights = castleRights; // 15 is 1111 in binary, which means all castles are legal.
    pos.board = board;
    pos.pieceLocations = determine_piece_squares(board);
    std::cout << "Generating Pseudo Moves\n";
    std::vector<std::tuple<int, int, int>> pseudomoves = create_pseudo_moves(pos);

    std::cout << "Printing Pseudo Moves!\n";
    for (const auto& [from_square, to_square, flags] : pseudomoves) {
    std::cout << "From: " << from_square 
              << ", To: " << to_square 
              << ", Flags: " << flags << "\n";
    }
}


//main();
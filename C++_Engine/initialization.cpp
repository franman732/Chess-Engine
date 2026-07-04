#include "initialization.h"

#include <unordered_map>
#include <array>
#include <iostream>

std::unordered_map<int, int> determine_piece_squares(const std::array<int, 64>& board) {
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
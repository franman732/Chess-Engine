#pragma once
#include "helper_functions.h"

#include <array>

constexpr bool valid_knight_move(int start, int target) {
    if ((target < 0) || (target >= 64)) {
        return false;
    }

    int startFile = start & 7;
    int targetFile = target & 7;

    int diff = abs_constexpr(startFile - targetFile);

    return ((diff == 1) || (diff == 2));
}

constexpr bool valid_pawn_move(int start, int target) { // This also works for validating king moves.
    if ((target < 0) || (target >= 64)) {
        return false;
    }

    int startFile = start & 7;
    int targetFile = target & 7;

    int diff = abs_constexpr(startFile - targetFile);

    return ((diff == 0) || (diff == 1));
}

bool is_square_attacked(int square, const std::array<int, 64>& board, int color);
bool determine_capturable(const std::array<int, 64>& board, int end, int color);

#pragma once

#include <unordered_map>
#include "position.h"


std::unordered_map<int, int> determine_piece_squares(const std::array<int, 64>& board);
#pragma once

#include <unordered_map>
#include "position.h"
#include "aliases.h"


std::unordered_map<int, int> determine_piece_squares(const Board& board);

int compute_hash(const Board& board, int sideToMove, int castle);

int count_pieces(const Board& board);
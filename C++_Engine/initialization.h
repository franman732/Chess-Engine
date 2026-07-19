#pragma once

#include "aliases.h"


#include <unordered_map>

std::unordered_map<int, int> determine_piece_squares(const Board& board);

int compute_hash(const Board& board, int sideToMove, int castle);

int count_pieces(const Board& board);

int find_king(const Board& board, int color);
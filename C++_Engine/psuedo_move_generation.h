#pragma once

#include "position.h"

#include <vector>
#include <tuple>

void determine_pawn_moves(const std::array<int, 64>& board, std::vector<std::tuple<int, int, int>>& moves, int start);
void determine_rook_moves(const std::array<int, 64>& board, std::vector<std::tuple<int, int, int>>& moves, int start);
void determine_bishop_moves(const std::array<int, 64>& board, std::vector<std::tuple<int, int, int>>& moves, int start);
void determine_queen_moves(const std::array<int, 64>& board, std::vector<std::tuple<int, int, int>>& moves, int start);
void determine_knight_moves(const std::array<int, 64>& board, std::vector<std::tuple<int, int, int>>& moves, int start);
void determine_king_moves(const std::array<int, 64>& board, std::vector<std::tuple<int, int, int>>& moves, int start, int castleRights);

std::vector<std::tuple<int, int, int>> create_pseudo_moves(Position& pos);
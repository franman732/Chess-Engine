#pragma once

#include "position.h"
#include "aliases.h"

#include <vector>
#include <tuple>

void determine_pawn_moves(const Board& board, moveList& moves, int start);
void determine_rook_moves(const Board& board, moveList& moves, int start);
void determine_bishop_moves(const Board& board, moveList& moves, int start);
void determine_queen_moves(const Board& board, moveList& moves, int start);
void determine_knight_moves(const Board& board, moveList& moves, int start);
void determine_king_moves(const Board& board, moveList& moves, int start, int castleRights);

moveList create_pseudo_moves(Position& pos);
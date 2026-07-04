#pragma once // This will contain all the information for dealing with evaluation

#include <random>
#include <cstdint> 
#include <unordered_map>
#include <tuple>
#include <array>

std::array<int, 33> OPENING_PIECE_VALUES;
std::array<int, 33> ENDING_PIECE_VALUES;

std::array<int, 33> PHASE_VALUES;

std::array<int, 64> OPENING_PAWN_TABLE;
std::array<int, 64> OPENING_BISHOP_TABLE;
std::array<int, 64> OPENING_QUEEN_TABLE;
std::array<int, 64> OPENING_KING_TABLE;
std::array<int, 64> OPENING_KNIGHT_TABLE;

std::array<int, 64> CLOSING_PAWN_TABLE;
std::array<int, 64> CLOSING_BISHOP_TABLE;
std::array<int, 64> CLOSING_QUEEN_TABLE;
std::array<int, 64> CLOSING_KING_TABLE;
std::array<int, 64> CLOSING_KNIGHT_TABLE;

std::array<int, 8> PASSED_OPENING;
std::array<int, 8> PASSED_CLOSING;

std::array<int, 17> OPST;
std::array<int, 17> CPST;

int OPENING_STACKED;
int ENDING_STACKED;
int OPENING_ISOLATED;
int ENDING_ISOLATED;

int MAX_KILLER_DEPTH; // I have to redo killer moves here because C++ does ont allow dynamic memory like python. I cannot have it start as None and then become 

std::array<std::array<int, 2>, 64> KILLER_MOVES;
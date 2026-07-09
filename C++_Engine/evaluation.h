#pragma once // This will contain all the information for dealing with evaluation

#include "aliases.h"
#include "moves.h"

#include <random>
#include <cstdint> 
#include <unordered_map>
#include <tuple>
#include <array>

std::array<int, 33> OPENING_PIECE_VALUES;
std::array<int, 33> ENDING_PIECE_VALUES;

std::array<int, 33> PHASE_VALUES;

std::array<int, 8> PASSED_OPENING;
std::array<int, 8> PASSED_CLOSING;

std::array<int, 17> OPST;
std::array<int, 17> CPST;

constexpr int OPENING_STACKED = 15;
constexpr int ENDING_STACKED = 10;
constexpr int OPENING_ISOLATED = 15;
constexpr int ENDING_ISOLATED = 10;

undoEvaluation evaluate_board(const Board& board);
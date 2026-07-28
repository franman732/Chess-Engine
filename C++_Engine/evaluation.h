#pragma once // This will contain all the information for dealing with evaluation

#include "aliases.h"
#include "moves.h"

#include <random> 
#include <unordered_map>
#include <tuple>
#include <array>

constexpr std::array<int, 33> OPENING_PIECE_VALUES = {0, -100, -100, -100, -100, -100, -100, -100, -100, -500, -320, -330, -900, -20000, -330, -320, -500, 100, 100, 100, 100, 100, 100, 100, 100, 500, 320, 330, 900, 20000, 330, 320, 500};
constexpr std::array<int, 33> ENDING_PIECE_VALUES = {0, -120, -120, -120, -120, -120, -120, -120, -120, -520, -300, -340, -900, -20000, -340, -300, -520, 120, 120, 120, 120, 120, 120, 120, 120, 520, 300, 340, 900, 20000, 340, 300, 520};

constexpr std::array<int, 33> PHASE_VALUES = {0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 4, 0, 1, 1, 2};

constexpr std::array<int, 8> PASSED_OPENING = {0, 5, 10, 20, 35, 60, 100, 0};
constexpr std::array<int, 8> PASSED_CLOSING = {0, 10, 20, 40, 70, 120, 200, 0};

constexpr int OPENING_STACKED = 15;
constexpr int ENDING_STACKED = 10;
constexpr int OPENING_ISOLATED = 15;
constexpr int ENDING_ISOLATED = 10;

evaluation evaluate_board(const Board& board);
#pragma once

#include "aliases.h"
#include "position.h"
#include "transposition_table.h"

constexpr int REDUCTION_FACTOR = 2;

float recurse(Position& pos, int depth, float alpha, float beta, int maximizing, bool allowNullMove, bool allowLMR, TT_tracker& tracker);

AMove Find_Best_Move(Position pos, int depth, AMove startingMove, TT_tracker& tracker);
#pragma once

#include "aliases.h"
#include "position.h"
#include "transposition_table.h"

int REDUCTION_FACTOR = 2;

float recurse(Position pos, int depth, float alpha, float beta, int maximizing, int allowNullMove, int allowLMR, TT_tracker& tracker);

AMove Find_Best_Move(Position pos, int depth, AMove startingMove, TT_tracker& tracker);
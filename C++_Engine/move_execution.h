#pragma once

#include "moves.h"
#include "aliases.h"
#include "position.h"

undoMove make_move(Position& pos, AMove move);

void undo_move(Position& pos, AMove move, undoMove undoInfo);
#include "position.h"
#include "moves.h"
#include "aliases.h"

#include <array>

const int MAXDEPTH = 8;

inline std::array<std::array<AMove, 2>, MAXDEPTH> killerMoves = [] {
    std::array<std::array<AMove, 2>, MAXDEPTH> arr{};
    arr.fill({AMove{-1, -1, -1}, AMove{-1, -1, -1}});
    return arr;
}();

std::array<std::array<int, 64>, 64> history{};

int score_move(Position pos, AMove move, int depth, AMove bestMove);

scoredMoves create_scored_moves(Position pos, moveList legalMoves, int depth, AMove bestMove);

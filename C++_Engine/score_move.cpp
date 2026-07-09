#include "score_move.h"
#include "position.h"
#include "moves.h"
#include "aliases.h"

#include <algorithm>

int score_move(Position pos, AMove move, int depth, AMove bestMove) {
    auto& [start, end, extra] = move;
    
    int attacker = pos.board[start];
    int victim = pos.board[end];

    int score = 0;

    if (move == bestMove) {
        score += 15000;
    }

    if (victim == 0) {
        score += history[start][end];
    }

    if (victim != 0) {
        score += 10000;
        score += 10 * victim;
        score -= attacker;
    }

    if (PIECES[attacker] == PAWN_NUMBER) {
        if ((end / 8 == 0) || (end / 8 == 7 )) {
            score += 100000;
        }
    }

    if (move == killerMoves[depth][0]) {
        score += 8000;
    } else if (move == killerMoves[depth][1]) {
        score += 7000;
    }

    return score;
}

scoredMoves create_scored_moves(Position pos, moveList legalMoves, int depth, AMove bestMove) {
    scoredMoves scoredMoves{};

    for (AMove& move : legalMoves) {
        int score = score_move(pos, move, depth, bestMove);
        scoredMoves.emplace_back(score, move);
    }

    std::sort(scoredMoves.begin(), scoredMoves.end(),
        [](const scoredMove& a, const scoredMove& b) {
            return a.first > b.first;
        });

    return scoredMoves;
}
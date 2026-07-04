#pragma once // This contains all the information necessary for position

#include "moves.h"

#include <tuple>
#include <vector>
#include <variant>
#include <array>
#include <unordered_map>

class Position {
    public:
        int sideToMove;
        std::array<int, 64> board;
        int castleRights;
        /*uint64_t hash;
        int blackKing;
        int whiteKing;
        int pieces;

        int openingEval;
        int closingEval;
        int phase;
        int whiteBishops;
        int blackBishops;
        int whitePawns;
        int blackPawns;
        uint64_t pawnHash;*/

        std::unordered_map<int, int> pieceLocations;

    private:
        void update_evaluation(std::tuple<int, int, int> move, const undoMove& undoInfo, bool finalMove);
};
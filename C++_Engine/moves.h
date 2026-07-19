#pragma once // This will contain all the information necessary for dealing with moves.

#include <tuple>
#include <vector>
#include <array>
#include <cstdint>

inline constexpr int WK = 4;
inline constexpr int WQ = 8;
inline constexpr int BK = 1; // These 4 values will just be used for changing castle rights.
inline constexpr int BQ = 2;

inline constexpr int KING_NUMBER = 6;
inline constexpr int PAWN_NUMBER = 1;
inline constexpr int ROOK_NUMBER = 2;
inline constexpr int BISHOP_NUMBER = 4;
inline constexpr int QUEEN_NUMBER = 5;
inline constexpr int KNIGHT_NUMBER = 3;

inline constexpr std::array<int, 33> PIECES = {0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 4, 3, 2};

struct evaluation {
    int openingEval;
    int closingEval;
    int phase;
    bool whiteBishops;
    bool blackBishops;
    std::array<int, 8> whitePawns;
    std::array<int, 8> blackPawns;
    uint64_t pawnHash;
};

struct undoEvaluation {
    int openingEval;
    int closingEval;
    int phase;
    bool whiteBishops;
    bool blackBishops;
    std::array<int, 2> changeWhitePawns;
    std::array<int, 2> changeBlackPawns;
    uint64_t pawnHash;
};

struct undoMove {
    int capturedPiece; int castleRights; int sideToMove; uint64_t hash; int promotion; int numPieces; undoEvaluation undoEval; 
};
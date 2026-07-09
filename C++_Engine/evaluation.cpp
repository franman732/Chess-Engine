#include "moves.h"
#include "aliases.h"
#include "evaluation.h"
#include "PSTs.h"
#include "transposition_table.h"

#include <array>

undoEvaluation evaluate_board(const Board& board) {
    undoEvaluation undoEval;
    
    std::array<int, 8> whitePawns = {};
    std::array<int, 8> blackPawns = {};

    int whiteStacked = 0;
    int blackStacked = 0;
    int whiteIsolated = 0;
    int blackIsolated = 0;

    int pawnOGEval = 0;
    int pawnEGEval = 0;

    int OGEval = 0;
    int EGEval = 0;

    int phase = 0;

    int whiteBishops = 0;
    int blackBishops = 0;

    int pawnHash = 0;

    int counter = 0;
    for (int piece : board) {
        if (piece == 0) {
            continue;
        }

        bool isWhite = (piece >= 17);

        int tableIndex = counter;
        if (!isWhite) {
            tableIndex = (63 - counter);
        }

        OGEval += OPENING_PIECE_VALUES[piece];
        EGEval += ENDING_PIECE_VALUES[piece];

        OGEval += OPST[piece][tableIndex];
        EGEval += EPST[piece][tableIndex];

        phase += PHASE_VALUES[piece];

        if ((piece == 27) || (piece == 30)) {
            whiteBishops += 1;
        } else {
            if ((piece == 11) || (piece == 14)) {
                blackBishops += 1;
            }
        }

        if ((0 < piece) && (piece < 9)) {
            pawnHash ^= PAWN_ZOBRIST[piece][counter];
            int file = counter & 7;
            blackPawns[file] += 1;
        } else {
            if ((16 < piece) && (piece < 25)) {
                pawnHash ^= PAWN_ZOBRIST[piece][counter];
                int file = counter & 7;
                whitePawns[file] += 1;
            }
        }
    }

    if (whiteBishops >= 2) {
        OGEval += 50;
        EGEval += 50;
    }

    if (blackBishops >= 2) {
        OGEval -= 50;
        EGEval -= 50;
    }

    if (phase > 24) {
        phase = 24;
    } 

    for (int file = 0; file < 8; file++) {
        int w = whitePawns[file];
        int b = blackPawns[file];

        if (w > 1) {
            whiteStacked += (w - 1);
        }
        if (b > 1) {
            blackStacked += (b - 1);
        }

        if (w) {
            bool left = ((file > 0) && (whitePawns[file - 1]));
            bool right = ((file < 7) && (whitePawns[file + 1]));

            if ((!left) && (!right)) {
                whiteIsolated += w;
            }
        }

        if (b) {
            bool left = ((file > 0) && (blackPawns[file - 1]));
            bool right = ((file < 7) && (blackPawns[file + 1]));

            if ((!left) && (!right)) {
                blackIsolated += b;
            }
        }
    }

    pawnOGEval -= whiteIsolated * OPENING_ISOLATED;
    pawnEGEval -= whiteIsolated * ENDING_ISOLATED;

    pawnOGEval += blackIsolated * OPENING_ISOLATED;
    pawnEGEval += blackIsolated * ENDING_ISOLATED;

    pawnOGEval -= whiteStacked * OPENING_STACKED;
    pawnEGEval -= whiteStacked * ENDING_STACKED;

    pawnOGEval += blackStacked * OPENING_STACKED;
    pawnEGEval += blackStacked * ENDING_STACKED;

    std::pair<int, int> pair{pawnOGEval, pawnEGEval};

    PAWN_HASH_TABLE[pawnHash] = pair;

        int openingEval;
    int closingEval;
    int phase;
    bool whiteBishops;
    bool blackBishops;
    std::array<int, 8> changeWhitePawns;
    std::array<int, 8> changeBlackPawns;
    uint64_t pawnHash;

    undoEval.openingEval = OGEval;
    undoEval.closingEval = EGEval;
    undoEval.phase = phase;
    undoEval.whiteBishops = whiteBishops;
    undoEval.blackBishops = blackBishops;
    undoEval.WhitePawns = changeWhitePawns;
    undoEval.BlackPawns = changeBlackPawns;
    undoEval.pawnHash = pawnHash;
    
    return undoEval;
}
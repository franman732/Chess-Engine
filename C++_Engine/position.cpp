#include "position.h"
#include "aliases.h"
#include "moves.h"
#include "evaluation.h"
#include "PSTs.h"
#include "transposition_table.h"

#include <cstdint> 
#include <tuple>

float Position::update_evaluation(AMove move, const undoMove& undoInfo, bool finalMove) {
    int whiteStacked = 0;
    int blackStacked = 0;
    int whiteIsolated = 0;
    int blackIsolated = 0;

    float pawnOEval = 0;
    float pawnEEval = 0;

    std::tuple zobristEvaluation = std::make_tuple(0.1234567, 0.1234567); // I assigned a weird decimal so i can check for that decimal. The odds that the hash actually contains that decimal is practcally zero. Also, it intiailizes both values to floats.
    
    bool isWhite;
    int startTableIndex;
    int endTableIndex;
    int capturedPieceTableIndex;

    auto [start, end, extra] = move;
    int movedPiece = board[end];
    int capturedPiece = undoInfo.capturedPiece;

    if (!(finalMove)) {
        if (movedPiece >= 17) {
            isWhite = true;
        } else {
            isWhite = false;
        }
    

        if (isWhite) {
            startTableIndex = start;
            endTableIndex = end;
        } else {
            startTableIndex = 63 - start;
            endTableIndex = 63 - end;
        }

        if (!(isWhite)) {
            capturedPieceTableIndex = end;
        } else {
            capturedPieceTableIndex = 63 - end;
        }

        evalInfo.openingEval -= OPST[movedPiece][startTableIndex];
        evalInfo.closingEval -= EPST[movedPiece][startTableIndex];
        evalInfo.openingEval += OPST[movedPiece][endTableIndex];
        evalInfo.closingEval += EPST[movedPiece][endTableIndex];

        if (PIECES[movedPiece] == PAWN_NUMBER) {
            int row = end >> 3;
            if (isWhite && (row == 0)) {
                evalInfo.openingEval -= OPST[movedPiece][endTableIndex];
                evalInfo.closingEval -= EPST[movedPiece][endTableIndex];
                evalInfo.openingEval -= OPENING_PIECE_VALUES[movedPiece];
                evalInfo.closingEval -= ENDING_PIECE_VALUES[movedPiece];

                evalInfo.openingEval += OPST[28][endTableIndex];
                evalInfo.closingEval += EPST[28][endTableIndex];
                evalInfo.openingEval += OPENING_PIECE_VALUES[28];
                evalInfo.closingEval += ENDING_PIECE_VALUES[28];
            } else if ((!isWhite) && (row == 7)) {
                evalInfo.openingEval -= OPST[movedPiece][endTableIndex];
                evalInfo.closingEval -= EPST[movedPiece][endTableIndex];
                evalInfo.openingEval -= OPENING_PIECE_VALUES[movedPiece];
                evalInfo.closingEval -= ENDING_PIECE_VALUES[movedPiece];

                evalInfo.openingEval += OPST[12][endTableIndex];
                evalInfo.closingEval += EPST[12][endTableIndex];
                evalInfo.openingEval += OPENING_PIECE_VALUES[12];
                evalInfo.closingEval += ENDING_PIECE_VALUES[12];

            }
        }

        if (capturedPiece != 0) {
            evalInfo.phase -= PHASE_VALUES[capturedPiece];

            evalInfo.openingEval -= OPST[capturedPiece][capturedPieceTableIndex];
            evalInfo.closingEval -= EPST[capturedPiece][capturedPieceTableIndex];
            evalInfo.openingEval -= OPENING_PIECE_VALUES[capturedPiece];
            evalInfo.closingEval -= ENDING_PIECE_VALUES[capturedPiece];

            if ((capturedPiece == 27) || (capturedPiece == 30)) {
                evalInfo.whiteBishops = false;
            } else if ((capturedPiece == 11) || (capturedPiece == 14)) {
                evalInfo.blackBishops = false;
            }
        } else if (extra != -1) {
            if (extra == 0) {
                evalInfo.openingEval -= OPST[16][63 - 7];
                evalInfo.closingEval -= EPST[16][63 - 7];

                evalInfo.openingEval += OPST[16][63 - 5];
                evalInfo.closingEval += EPST[16][63 - 5];
            } else if (extra == 1) {
                evalInfo.openingEval -= OPST[9][63];
                evalInfo.closingEval -= EPST[9][63];

                evalInfo.openingEval += OPST[9][63 - 3];
                evalInfo.closingEval += EPST[9][63 - 3];
            } else if (extra == 2) {
                evalInfo.openingEval -= OPST[32][63];
                evalInfo.closingEval -= EPST[32][63];

                evalInfo.openingEval += OPST[32][61];
                evalInfo.closingEval += EPST[32][61];
            } else if (extra == 3) {
                evalInfo.openingEval -= OPST[25][56];
                evalInfo.closingEval -= EPST[25][56];

                evalInfo.openingEval += OPST[25][59];
                evalInfo.closingEval += EPST[25][59];
            }
        }
    }

    auto it = PAWN_HASH_TABLE.find(evalInfo.pawnHash);
    if (it != PAWN_HASH_TABLE.end()) {
        zobristEvaluation = it->second; // This checks whether this hash is in the Transposition table or not
    }

    if ((std::get<0>(zobristEvaluation) == 0.1234567) && (std::get<1>(zobristEvaluation) == 0.1234567)) {
        for (int file = 0; file < 8; file++) {
            int w = evalInfo.whitePawns[file];
            int b = evalInfo.blackPawns[file];

            if (w > 1) {
                whiteStacked += (w - 1);
            }

            if (b > 1) {
                blackStacked += (b - 1);
            }

            if (w) {
                bool left = ((file > 0) && (evalInfo.whitePawns[file - 1]));
                bool right = ((file < 7) && (evalInfo.whitePawns[file + 1]));

                if ((!left) && (!right)) {
                    whiteIsolated += w;
                }
            }

            if (b) {
                bool left = ((file > 0) && (evalInfo.blackPawns[file - 1]));
                bool right = ((file < 7) && (evalInfo.blackPawns[file + 1]));

                if ((!left) && (!right)) {
                    blackIsolated += b;
                }
            }
        }

        pawnOEval -= whiteIsolated * OPENING_ISOLATED;
        pawnEEval -= whiteIsolated * ENDING_ISOLATED;

        pawnOEval += blackIsolated * OPENING_ISOLATED;
        pawnEEval += blackIsolated * ENDING_ISOLATED;

        pawnOEval -= whiteStacked * OPENING_STACKED;
        pawnEEval -= whiteStacked * ENDING_STACKED;

        pawnOEval += blackStacked * OPENING_STACKED;
        pawnEEval += blackStacked * ENDING_STACKED;

        evalInfo.openingEval += pawnOEval;
        evalInfo.closingEval += pawnEEval;

        PAWN_HASH_TABLE[evalInfo.pawnHash] = std::make_tuple(pawnOEval, pawnEEval);
    } else {
        auto [pawnOEval, pawnEEval] = zobristEvaluation;
        evalInfo.openingEval += pawnOEval;
        evalInfo.closingEval += pawnEEval;
    }

    if (finalMove) {
        return (((evalInfo.openingEval * evalInfo.phase) + (evalInfo.closingEval * (24 - evalInfo.phase))) / 24);
    }
}
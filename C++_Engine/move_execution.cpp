#include "moves.h"
#include "aliases.h"
#include "position.h"
#include "transposition_table.h"

#include <array>
#include <vector>
#include <unordered_map>
#include <cstdint>

undoMove make_move(Position& pos, AMove move) {
    auto [start, end, extra] = move;
    int castleRights = pos.castleRights;
    int numPieces = pos.pieces;
    uint64_t hash = pos.hash;
    uint64_t pawnHash = pos.evalInfo.pawnHash;
    Board& board = pos.board;
    int sideToMove = pos.sideToMove;
    std::array<int, 8>& blackPawns = pos.evalInfo.blackPawns;
    std::array<int, 8>& whitePawns = pos.evalInfo.whitePawns;
    std::unordered_map<int, int>& piecePos = pos.pieceLocations;

    std::array<int, 2> changeWhitePawns = {-1, -1};
    std::array<int, 2> changeBlackPawns = {-1, -1};

    undoMove undo;
    undo.capturedPiece = board[end];
    undo.castleRights = castleRights;
    undo.sideToMove = sideToMove;
    undo.hash = hash;
    undo.promotion = -1; // Initialized to -1, meaning no promotion. Will be changed later.
    undo.numPieces = numPieces;

    undo.undoEval.openingEval = pos.evalInfo.openingEval;
    undo.undoEval.closingEval = pos.evalInfo.closingEval;
    undo.undoEval.phase = pos.evalInfo.phase;
    undo.undoEval.whiteBishops = pos.evalInfo.whiteBishops;
    undo.undoEval.blackBishops = pos.evalInfo.blackBishops;
    undo.undoEval.changeWhitePawns = changeWhitePawns;
    undo.undoEval.changeBlackPawns = changeBlackPawns;
    undo.undoEval.pawnHash = pos.evalInfo.pawnHash;

    int movedPiece = board[start];
    int endPiece = board[end];

    if (movedPiece == 13) {
        pos.blackKing = end;
    } else if (movedPiece == 29) {
        pos.whiteKing = end;
    }

    piecePos.erase(start);
    piecePos[end] = movedPiece;

    if (extra == -1) {
        hash ^= ZOBRIST[movedPiece][start] ^ ZOBRIST[movedPiece][end];

        if (endPiece != 0) {
            hash ^= ZOBRIST[endPiece][end];
            if ((!(PIECES[endPiece] == PAWN_NUMBER)) && (!(PIECES[endPiece] == KING_NUMBER))) {
                pos.pieces -= 1;
            } else if (PIECES[endPiece] == PAWN_NUMBER) {
                pawnHash ^= PAWN_ZOBRIST[endPiece][end];
                int col = end & 7;
                if (sideToMove) {
                    undo.undoEval.changeWhitePawns = {col, -1};
                    blackPawns[col] -= 1;
                } else {
                    undo.undoEval.changeBlackPawns = {col, -1};
                    whitePawns[col] -= 1;
                }
            }
        }

        board[end] = movedPiece;
        board[start] = 0;

        if (PIECES[movedPiece] == PAWN_NUMBER) {
            pawnHash ^= PAWN_ZOBRIST[movedPiece][start] ^ PAWN_ZOBRIST[movedPiece][end];
            int startCol = start & 7;
            int endCol = end & 7;

            if (sideToMove) {
                undo.undoEval.changeWhitePawns = {startCol, endCol};
                whitePawns[startCol] -= 1;
                whitePawns[endCol] += 1;
            } else {
                undo.undoEval.changeBlackPawns = {startCol, endCol};
                blackPawns[startCol] -= 1;
                blackPawns[endCol] += 1;
            }

            if ((end >> 3) == 0) {
                piecePos[end] = 28;

                board[end] = 28;
                hash ^= ZOBRIST[movedPiece][end] ^ ZOBRIST[28][end];
                undo.promotion = movedPiece;

                if (endPiece == 0) {
                    pawnHash ^= PAWN_ZOBRIST[movedPiece][start];
                    int col = end & 7;
                    undo.undoEval.changeWhitePawns = {col, -2};
                    whitePawns[col] -= 1;
                } 

            } else if ((end >> 3) == 7) {
                piecePos[end] = 12;

                board[end] = 12;
                hash ^= ZOBRIST[movedPiece][end] ^ ZOBRIST[12][end];
                undo.promotion = movedPiece;

                if (endPiece == 0) {
                    pawnHash ^= PAWN_ZOBRIST[movedPiece][start];
                    int col = end & 7;
                    undo.undoEval.changeBlackPawns = {col, -2};
                    blackPawns[col] -= 1;
                }
            }
        }

        hash ^= ZOBRIST_SIDE;

        if ((((movedPiece == 9) && (start == 0)) || (endPiece == 9)) && (castleRights & BQ)) {
            castleRights &= ~BQ;
            hash ^= ZOBRIST_CASTLE[BQ];
        } else if ((((movedPiece == 16) && (start == 7)) || (endPiece == 16)) && (castleRights & BK)) {
            castleRights &= ~BK;
            hash ^= ZOBRIST_CASTLE[BK];
        } else if (((movedPiece == 13) && (start == 4)) && ((castleRights & BK) || (castleRights & BQ))) {
            if (castleRights & BK) {
                hash ^= ZOBRIST_CASTLE[BK];
                castleRights &= ~BK;
            } else if (castleRights & BQ) {
                hash ^= ZOBRIST_CASTLE[BQ];
                castleRights &= ~BQ;
            }

        } else if ((((movedPiece == 25) && (start == 56)) || (endPiece == 25)) && (castleRights & WQ)) {
            castleRights &= ~WQ;
            hash ^= ZOBRIST_CASTLE[WQ];
        } else if ((((movedPiece == 32) && (start == 63)) || (endPiece == 32)) && (castleRights & WK)) {
            castleRights &= ~WK;
            hash ^= ZOBRIST_CASTLE[WK];
        } else if (((movedPiece == 29) && (start == 60)) && ((castleRights & WK) || (castleRights & WQ))) {
            if (castleRights & WK) {
                hash ^= ZOBRIST_CASTLE[WK];
                castleRights &= ~WK;
            } else if (castleRights & WQ) {
                hash ^= ZOBRIST_CASTLE[WQ];
                castleRights &= ~WQ;
            }
        }

    } else {
        hash ^= ZOBRIST[board[start]][start] ^ ZOBRIST[board[start]][end];

        board[end] = movedPiece;
        board[start] = 0;

        hash ^= ZOBRIST_SIDE;

        if (extra == 0) {
            hash ^= ZOBRIST[16][7] ^ ZOBRIST[16][5];

            piecePos[5] = board[7];
            piecePos.erase(7);

            board[5] = board[7];
            board[7] = 0;
            castleRights &= ~BQ & ~BK;
            hash ^= ZOBRIST_CASTLE[BQ] ^ ZOBRIST_CASTLE[BK];

        } else if (extra == 1) {
            hash ^= ZOBRIST[9][0] ^ ZOBRIST[9][3];

            piecePos[3] = board[0];
            piecePos.erase(0);

            board[3] = board[0];
            board[0] = 0;
            castleRights &= ~BQ & ~BK;
            hash ^= ZOBRIST_CASTLE[BQ] ^ ZOBRIST_CASTLE[BK];

        } else if (extra == 2) {
            hash ^= ZOBRIST[32][63] ^ ZOBRIST[32][61];

            piecePos[61] = board[63];
            piecePos.erase(63);

            board[61] = board[63];
            board[63] = 0;
            castleRights &= ~WQ & ~WK;
            hash ^= ZOBRIST_CASTLE[WQ] ^ ZOBRIST_CASTLE[WK];

        } else if (extra == 3) {
            hash ^= ZOBRIST[25][56] ^ ZOBRIST[25][59];

            piecePos[59] = board[56];
            piecePos.erase(56);

            board[59] = board[56];
            board[56] = 0;
            castleRights &= ~WQ & ~WK;
            hash ^= ZOBRIST_CASTLE[WQ] ^ ZOBRIST_CASTLE[WK];
        }
    }

    pos.sideToMove = sideToMove ^ 1;
    pos.hash = hash;
    pos.castleRights = castleRights;
    pos.evalInfo.pawnHash = pawnHash;

    return undo;
}

void undo_move(Position& pos, AMove move, undoMove& undoInfo) {
    auto [start, end, extra] = move;
    Board& board = pos.board;

    int movedPiece = board[end];
    int capturedPiece = undoInfo.capturedPiece;

    board[start] = movedPiece;
    board[end] = capturedPiece;

    pos.castleRights = undoInfo.castleRights;
    pos.sideToMove = undoInfo.sideToMove;

    pos.hash = undoInfo.hash;
    int originalPiece = undoInfo.promotion;

    if (movedPiece == 13) {
        pos.blackKing = start;
    } else if (movedPiece == 29) {
        pos.whiteKing = start;
    }

    std::unordered_map<int, int>& piecePositions = pos.pieceLocations;

    pos.pieces = undoInfo.numPieces;

    pos.evalInfo.openingEval = undoInfo.undoEval.openingEval;
    pos.evalInfo.closingEval = undoInfo.undoEval.closingEval;
    pos.evalInfo.phase = undoInfo.undoEval.phase;
    pos.evalInfo.whiteBishops = undoInfo.undoEval.whiteBishops;
    pos.evalInfo.blackBishops = undoInfo.undoEval.blackBishops;
    auto changeWhitePawns = undoInfo.undoEval.changeWhitePawns;
    auto changeBlackPawns = undoInfo.undoEval.changeBlackPawns;
    pos.evalInfo.pawnHash = undoInfo.undoEval.pawnHash;

    std::array<int, 8>& blackPawns = pos.evalInfo.blackPawns;
    std::array<int, 8>& whitePawns = pos.evalInfo.whitePawns;

    piecePositions[start] = piecePositions[end];
    piecePositions.erase(end);

    if (capturedPiece != 0) {
        piecePositions[end] = capturedPiece;
    }

    if (undoInfo.promotion != -1) {
        board[start] = originalPiece;
        piecePositions[start] = originalPiece;
    }

    if (!(changeWhitePawns.empty())) {
        int start = changeWhitePawns[0];
        int end = changeWhitePawns[1];

        if (end >= 0) {
            whitePawns[end] -= 1;
            whitePawns[start] += 1;
        } else if ((end == -1) || (end == -2)) {
            whitePawns[start] += 1;
        }
    }

    if (!(changeBlackPawns.empty())) {
        int start = changeBlackPawns[0];
        int end = changeBlackPawns[1];

        if (end >= 0) {
            blackPawns[end] -= 1;
            blackPawns[start] += 1;
        } else if ((end == -1) || (end == -2)) {
            blackPawns[start] += 1;
        }
    }

    if (extra != -1) {
        if (extra == 0) {
            board[7] = board[5];
            board[5] = 0;

            piecePositions[7] = piecePositions[5];
            piecePositions.erase(5);
        } else if (extra == 0) {
            board[0] = board[3];
            board[3] = 0;

            piecePositions[0] = piecePositions[3];
            piecePositions.erase(3);
        } else if (extra == 0) {
            board[63] = board[61];
            board[61] = 0;

            piecePositions[63] = piecePositions[61];
            piecePositions.erase(61);
        } else if (extra == 0) {
            board[56] = board[59];
            board[59] = 0;

            piecePositions[56] = piecePositions[59];
            piecePositions.erase(59);
        } 
    }
}   
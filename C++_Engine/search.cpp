#include "Search.h"
#include "aliases.h"
#include "position.h"
#include "transposition_table.h"
#include "psuedo_move_generation.h"
#include "score_move.h"
#include "move_execution.h"
#include "validation.h"

#include <string>
#include <iostream>
#include <algorithm>

AMove Find_Best_Move(Position pos, int depth, AMove startingMove, TT_tracker& tracker) {
   // std::cout << "Entering Find_Best_Move\n";
    float alpha = -99999999;
    float beta = 99999999;
    int side = pos.sideToMove;
    float bestEval;

    float origAlpha = alpha;
    float origBeta = beta;
    AMove entryMove = {-1, -1, -1};
    TT_Info entry = {-1, -1, "", {-1, -1, -1}}; // Default value.
    int firstMove = 0;
    Board& board = pos.board;
    bool foundLegalMove = false;

    auto it = TT.find(pos.hash);
    if (it != TT.end()) {
        entry = it->second; // This checks whether this hash is in the Transposition table or not
    }

    if (entry.depth != -1) { // IF it is in the transposition table, then depth wont equal -1.
        tracker.TT_Lookups += 1;
        auto [entryDepth, entryScore, entryFlag, entryMove] = entry;

        if (entryDepth >= depth) {
            if (entryFlag == "EXACT") {
                tracker.TT_Hits += 1;
                //std::cout << "WE RETURNED TT \n";
                return entryMove;
            } else if (entryFlag == "LOWER") {
                alpha = std::max(alpha, entryScore);
            } else if (entryFlag == "UPPER") {
                beta = std::min(beta, entryScore);
            }

            if (alpha >= beta) {
                tracker.TT_Hits += 1;
                //std::cout << "WE RETURNED TT \n";
                return entryMove;
            }
        }
    }
    //std::cout << "We passed TT!\n";

    moveList allMoves = create_pseudo_moves(pos);
    scoredMoves scoredMovesList = create_scored_moves(pos, allMoves, depth, startingMove);
    AMove bestMove = {-1, -1, -1};

    //std::cout << "WE PASSED MAKING MOVES\n";

    if (side) {
        bestEval = -99999999 - depth;
    } else {
        bestEval = 99999999 - depth;
    }

    for (int i = 0; i < scoredMovesList.size(); i++) {
        AMove move = scoredMovesList[i].second;
        auto [start, end, extra] = move;
        int capturedPiece = board[end];
        undoMove undoInfo = make_move(pos, move);
    //std::cout << "WE PASSED UNDOINFO\n";

        //std::cout << "WE PASSED UNDOINFO\n";
        if (!(pos.sideToMove)) {
            if (is_square_attacked(pos.whiteKing, pos.board, 1)) {
                undo_move(pos, move, undoInfo);
                continue;
            }
        } else {
            if (is_square_attacked(pos.blackKing, pos.board, 0)) {
                undo_move(pos, move, undoInfo);
                continue;
            }
        }


        //std::cout << "WEE PASSED CHECKMATE CHECKING\n";

        foundLegalMove = true;
        pos.update_evaluation(move, undoInfo);
        firstMove += 1;

        if (firstMove == 1) {
            float score = recurse(pos, depth - 1, alpha, beta, !side, true, true, tracker);

            if (side) {
                alpha  = std::max(alpha, score);

                if (score > bestEval) {
                    bestEval = score;
                    bestMove = move;
                }
            } else {
                beta = std::min(beta, score);

                if (score < bestEval) {
                    bestEval = score;
                    bestMove = move;
                }
            }

            undo_move(pos, move, undoInfo);

            if (alpha >= beta) {
                break;
            } 
        } else {
            if (side) {
                float score = recurse(pos, depth - 1, alpha, alpha + 1, false, true, true, tracker);

                if ((score > origAlpha) && (score < beta)) {
                    score = recurse(pos, depth - 1, alpha, beta, false, true, true, tracker);
                }

                if (score > bestEval) {
                    bestEval = score;
                    bestMove = move;
                }

                alpha = std::max(alpha, score);

                undo_move(pos, move, undoInfo);

                if (beta <= alpha) {
                    auto [start, end, extra] = move;

                    history[start][end] += (depth * depth);

                    if ((capturedPiece == 0) && (!((PIECES[board[start]] == PAWN_NUMBER) && ((end >> 3 == 0) || (end >> 3 == 7))))) {
                        if (move != (killerMoves[depth][0])) {
                            killerMoves[depth][1] = killerMoves[depth][0];
                            killerMoves[depth][0] = move;
                        }
                    }
                    break;
                }
            } else {
                float score = recurse(pos, depth - 1, beta - 1, beta, true, true, true, tracker);

                if ((score < origBeta) && (score > origAlpha)) {
                    score = recurse (pos, depth - 1, alpha, beta, true, true, true, tracker);
                }

                if (score < bestEval) {
                    bestEval = score;
                    bestMove = move;
                }

                beta = std::min(beta, score);

                undo_move(pos, move, undoInfo);

                if (beta <= alpha) {
                    auto [start, end, extra] = move;

                    history[start][end] += (depth * depth);

                    if ((capturedPiece == 0) && (!((PIECES[board[start]] == PAWN_NUMBER) && ((end >> 3 == 0) || (end >> 3 == 7))))) {
                        if (move != (killerMoves[depth][0])) {
                            killerMoves[depth][1] = killerMoves[depth][0];
                            killerMoves[depth][0] = move;
                        }
                    } 

                    break;
                }
            }

        }
    }

    if (!(foundLegalMove)) {
        if (side && is_square_attacked(pos.whiteKing, board, 1)) {
            bestEval = -99999999 - depth;
        } else if ((!side) && is_square_attacked(pos.blackKing, board, 0)) {
            bestEval = 99999999 - depth;
        } else {
            bestEval = 0;
        }
    }

    std::string flag = "EXACT";

    if (bestEval <= origAlpha) {
        flag = "UPPER";
    } else if (bestEval >= origBeta) {
        flag = "LOWER";
    }

    if ((entry.depth == -1) || (depth >= entry.depth)) {
        TT[pos.hash] = TT_Info{depth, bestEval, flag, bestMove};
    }

    return bestMove;
}

float recurse(Position& pos, int depth, float alpha, float beta, int maximizing, bool allowNullMove, bool allowLMR, TT_tracker& tracker) {
    bool foundLegalMove = false;
    tracker.numberOfRecursions += 1;

    if (depth == 0) {
        float eval = pos.update_evaluation(AMove(-1, -1, -1), undoMove(), true);
        return eval;
    }

    int firstMove = 0;
    AMove bestMove;
    float origAlpha = alpha;
    float origBeta = beta;
    float best;

    AMove entryMove;

    float score;
    TT_Info entry = {-1, -1, "", {-1, -1, -1}};

    auto it = TT.find(pos.hash);
    if (it != TT.end()) {
        entry = it->second; // This checks whether this hash is in the Transposition table or not
    }

    if (entry.depth != -1) { // IF it is in the transposition table, then depth wont equal -1.
        tracker.TT_Lookups += 1;
        auto [entryDepth, entryScore, entryFlag, entry_Move] = entry;

        if (entryDepth >= depth) {
            if (entryFlag == "EXACT") {
                tracker.TT_Hits += 1;
                return entryScore;
            } else if (entryFlag == "LOWER") {
                alpha = std::max(alpha, entryScore);
            } else if (entryFlag == "UPPER") {
                beta = std::min(beta, entryScore);
            }

            if (alpha >= beta) {
                tracker.TT_Hits += 1;
                return entryScore;
            }
        }

        if (entryDepth <= depth) {
            entryMove = entry_Move;
        } else {
            entryMove = {-1, -1, -1};
        }
    }

    bool isKingAttacked;

    if (pos.sideToMove) {
        isKingAttacked = is_square_attacked(pos.whiteKing, pos.board, pos.sideToMove);
    } else {
        isKingAttacked = is_square_attacked(pos.blackKing, pos.board, pos.sideToMove);
    }

    if (allowNullMove && (depth >= REDUCTION_FACTOR + 1) && (!isKingAttacked) && (pos.pieces != 0)) {
        pos.sideToMove ^= 1;
        pos.hash ^= ZOBRIST_SIDE;

        if (maximizing) {
            score = recurse(pos, depth - 1 - REDUCTION_FACTOR, beta - 1, beta, maximizing ^ 1, false, false, tracker);
        } else {
            score = recurse(pos, depth - 1 - REDUCTION_FACTOR, alpha, alpha + 1, maximizing ^ 1, false, false, tracker);
        }

        pos.sideToMove ^= 1;
        pos.hash ^= ZOBRIST_SIDE;

        if (maximizing) {
            if (score >= beta) {
                return beta;
            }
        } else {
            if (score <= alpha) {
                return alpha;
            }
        }
    }

    //std::cout << "Entering Find_Best_Move\n";
    
    moveList allMoves = create_pseudo_moves(pos);

    //std::cout << "Pseudo moves generated: " << allMoves.size() << '\n';

    scoredMoves scoredMovesList = create_scored_moves(pos, allMoves, depth, entryMove);

    //std::cout << "Scored moves: " << scoredMovesList.size() << '\n';

    if (maximizing) {
        best = -99999999 - depth;
    } else {
        best = 99999999 - depth;
    }

    for (int i = 0; i < scoredMovesList.size(); i++) {
        //std::cout << "Trying move " << i << '\n';
        
        AMove move = scoredMovesList[i].second;
        auto [start, end, extra] = move;

        int capturedPiece = pos.board[end];
        undoMove undoInfo = make_move(pos, move);

        if (!(pos.sideToMove)) {
            if (is_square_attacked(pos.whiteKing, pos.board, 1)) {
                undo_move(pos, move, undoInfo);
                continue;
            }
        } else {
            if (is_square_attacked(pos.blackKing, pos.board, 0)) {
                undo_move(pos, move, undoInfo);
                continue;
            }
        }

        pos.update_evaluation(move, undoInfo);
        firstMove += 1;
        foundLegalMove = true;
        //std::cout << "Calling recurse depth=" << depth-1 << '\n';
        if (firstMove == 1) {
            score = recurse(pos, depth - 1, alpha, beta, maximizing ^ 1, allowNullMove, true, tracker);

            if (maximizing) {
                alpha = std::max(alpha, score);

                if (score > best) {
                    best = score;
                    bestMove = move;
                }
            } else {
                beta = std::min(beta, score);

                if (score < best) {
                    best = score;
                    bestMove = move;
                }
            }

            undo_move(pos, move, undoInfo);

            if (alpha >= beta) {
                break;
            }
        } else {
            bool useLMR = ((firstMove > 3) && (depth > 2) && (capturedPiece == 0) && (move != killerMoves[depth][1]) && (move != entry.bestMove) && (allowLMR));

            if (maximizing) {
                if (useLMR) {
                    score = recurse(pos, depth - 2, alpha, alpha + 1, false, allowNullMove, false, tracker);

                    if (score > alpha) {
                        score = recurse(pos, depth - 1, alpha, beta, false, allowNullMove, true, tracker);
                    }
                } else {
                    score = recurse(pos, depth - 1, alpha, alpha + 1, false, allowNullMove, true, tracker);

                    if ((score < beta) && (score > alpha)) {
                        score = recurse(pos, depth - 1, alpha, beta, false, allowNullMove, true, tracker);
                    }
                }

                if (score > best) {
                    best = score;
                    bestMove = move;
                }

                alpha = std::max(alpha, score);
                undo_move(pos, move, undoInfo);

                if (beta <= alpha) {
                    auto [start, end, extra] = move;

                    history[start][end] += (depth * depth);

                    if ((capturedPiece == 0) && (!((PIECES[pos.board[start]] == PAWN_NUMBER) && ((end >> 3 == 0) || (end >> 3 == 7))))) {
                        if (move != killerMoves[depth][0]) {
                            killerMoves[depth][1] = killerMoves[depth][0];
                            killerMoves[depth][0] = move;
                        }
                    }

                    break;
                }
            } else {
                if (useLMR) {
                    score = recurse(pos, depth - 2, beta - 1, beta, true, allowNullMove, false, tracker);

                    if (score < beta) {
                        score = recurse(pos, depth - 1, alpha, beta, true, allowNullMove, true, tracker);
                    } 
                }  else {
                    score = recurse(pos, depth - 1, beta - 1, beta, true, allowNullMove, true, tracker);

                    if ((score < beta) && (score > alpha)) {
                        score = recurse(pos, depth - 1 , alpha, beta, true, allowNullMove, true, tracker);
                    }
                }

                if (score < best) {
                    best = score;
                    bestMove = move;
                }

                beta = std::min(beta, score);
                undo_move(pos, move, undoInfo);

                if (beta <= alpha) {
                    auto [start, end, extra] = move;

                    history[start][end] += (depth * depth);

                    if ((capturedPiece == 0) && (!((PIECES[pos.board[start]] == PAWN_NUMBER) && ((end >> 3 == 0) || (end >> 3 == 7))))) {
                        if (move != killerMoves[depth][0]) {
                            killerMoves[depth][1] = killerMoves[depth][0];
                            killerMoves[depth][0] = move;
                        }
                    }

                    break;
                }
            }

        }
    }

    if (!foundLegalMove) {
        if ((maximizing) && (is_square_attacked(pos.whiteKing, pos.board, 1))) {
            best = -99999999 - depth;
        } else if ((!maximizing) && (is_square_attacked(pos.blackKing, pos.board, 0))) {
            best = 99999999 - depth;
        } else {
            best = 0;
        }
    }

    std::string flag = "EXACT";

    if (best <= origAlpha) {
        flag = "UPPER";
    } else if (best >= origBeta) {
        flag = "LOWER";
    }

    if ((entry.depth == -1) || (depth >= entry.depth)) {
        TT[pos.hash] = TT_Info{depth, best, flag, bestMove};
    }

    return best;
}
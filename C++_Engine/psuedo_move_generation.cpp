#include "position.h"
#include "psuedo_move_generation.h"
#include "moves.h"
#include "tables.h"
#include "validation.h"
#include "aliases.h"

#include <array>
#include <vector>
#include <iostream>

void determine_sliding_moves(const Board& board, moveList& moves, const Raytable& slidingRay, int start) {
    int piece = board[start];
    int color;

    if (piece == 0) {
        color = -1;
    } else if (piece >= 17) {
        color = 1;
    } else {
        color = 0;
    }

    for (const auto& ray : slidingRay[start]) {
        for (int idx : ray) {
            if (idx == -1) {
                break;
            }
            int targetPiece = board[idx];
            if (targetPiece == 0) {
                moves.emplace_back(start, idx, -1);
            } else {
                int targetColor;
                if (targetPiece >= 17) {
                    targetColor = 1;
                } else {
                    targetColor = 0;
                }

                if (targetColor != color) {
                    moves.emplace_back(start, idx, -1);
                }
                break;
            }
        }
    }
}

void determine_pawn_moves(const Board& board, moveList& moves, int start) {
    int piece = board[start];
    int color;

    if (piece == 0) {
        color = -1;
    } else if (piece >= 17) {
        color = 1;
    } else {
        color = 0;
    }

    if (color == 0) {
        if ((1 == start >> 3) && (board[start + 16] == 0) && (board[start + 8] == 0)) {
            moves.emplace_back(start, start + 16, -1);
            moves.emplace_back(start, start + 8, -1);
        } else if (board[start + 8] == 0) {
            moves.emplace_back(start, start + 8, -1);
        }

        if (valid_pawn_move(start, start + 7) && determine_capturable(board, start + 7, color)) {
            moves.emplace_back(start, start + 7, -1);
        }
        if (valid_pawn_move(start, start + 9) && determine_capturable(board, start + 9, color)) {
            moves.emplace_back(start, start + 9, -1);
        }
    }
    else if (color == 1) {
        if ((6 == start >> 3) && (board[start - 16] == 0) && (board[start - 8] == 0)) {
            moves.emplace_back(start, start - 16, -1);
            moves.emplace_back(start, start - 8, -1);
        } else if (board[start - 8] == 0) {
            moves.emplace_back(start, start - 8, -1);
        }

        if (valid_pawn_move(start, start - 7) && determine_capturable(board, start - 7, color)) {
            moves.emplace_back(start, start - 7, -1);
        }
        if (valid_pawn_move(start, start - 9) && determine_capturable(board, start - 9, color)) {
            moves.emplace_back(start, start - 9, -1);
        }
    }
}

void determine_bishop_moves(const Board& board, moveList& moves, int start) {
    determine_sliding_moves(board, moves, DIAGONAL_RAYS, start);
}

void determine_rook_moves(const Board& board, moveList& moves, int start) {
    determine_sliding_moves(board, moves, STRAIGHT_RAYS, start);
}

void determine_queen_moves(const Board& board, moveList& moves, int start) {
    determine_sliding_moves(board, moves, STRAIGHT_RAYS, start);
    determine_sliding_moves(board, moves, DIAGONAL_RAYS, start);
}

void determine_knight_moves(const Board& board, moveList& moves, int start) {
    int piece = board[start];
    int color;

    if (piece == 0) {
        color = -1;
    } else if (piece >= 17) {
        color = 1;
    } else {
        color = 0;
    }

    std::cout << "WE SHOULD BE CHECKING NIGHT ATTACK LIST\n";
    for (const auto idx: KNIGHT_ATTACKS[start]) {
        std::cout << "WE IN KNIGHT ATTACK LIST\n";
        if (idx == -1) {
            continue;
        }
        int targetPiece = board[idx];
        if (targetPiece == 0) {
            moves.emplace_back(start, idx, -1);
        } else {
            if (determine_capturable(board, idx, color)) {
                moves.emplace_back(start, idx, -1);
            }
        }
    }
}

void determine_king_moves(const Board& board, moveList& moves, int start, int castleRights) {
    int piece = board[start];
    int color;

    if (piece == 0) {
        color = -1;
    } else if (piece >= 17) {
        color = 1;
    } else {
        color = 0;
    }

    for (const auto idx : KING_ATTACKS[start]) {
        if (idx == -1) {
            break;
        }
        int targetPiece = board[idx];
        if (targetPiece == 0) {
            moves.emplace_back(start, idx, -1);
        } else {
            if (determine_capturable(board, idx, color)) {
                moves.emplace_back(start, idx, -1);
                break;
            }
        }
    }

    if (castleRights != 0) {
        if (color) {
            if (castleRights & WK) {
                if ((board[61] == 0) && (board[62] == 0)) {
                    if (board[63] == 32) {
                        if ((!is_square_attacked(60, board, 1)) && (!is_square_attacked(61, board, 1)) && (!is_square_attacked(62, board, 1))) {
                            moves.emplace_back(60, 62, 2);
                        }
                    }
                }
            }

            if (castleRights & WQ) {
                if ((board[59] == 0) && (board[58] == 0) && (board[57] == 0)) {
                    if (board[56] == 25) {
                        if((!is_square_attacked(60, board, 1)) && (!is_square_attacked(59, board, 1)) && (!is_square_attacked(58, board, 1))) {
                            moves.emplace_back(60, 58, 3);
                        }
                    }
                }
            }
        }

        else {
            if (castleRights & BK) {
                if ((board[5] == 0) && (board[6] == 0)) {
                    if (board[7] == 16) {
                        if ((!is_square_attacked(4, board, 0)) && (!is_square_attacked(5, board, 0)) && (!is_square_attacked(6, board, 0))) {
                            moves.emplace_back(4, 6, 0);
                        }
                    }
                } 
            }

            if (castleRights & BQ) {
                if ((board[1] == 0) && (board[2] == 0) && (board[3] == 0)) {
                    if (board[0] == 9) {
                        if ((!is_square_attacked(4, board, 0)) && (!is_square_attacked(3, board, 0)) && (!is_square_attacked(2, board, 0))) {
                            moves.emplace_back(4, 2, 1);
                        }
                    }
                } 
            }
        }
    }
}


moveList create_pseudo_moves(Position& pos) {
    std::array<int, 64>& board = pos.board;
    int color = pos.sideToMove;
    int castleRights = pos.castleRights;
    
    moveList moves = {};

    for (const auto& [key, value] : pos.pieceLocations) {
        int pieceColor;

        if (value == 0) {
            pieceColor = -1;
        } else if (value >= 17) {
            pieceColor = 1;
        } else {
            pieceColor = 0;
        }

        if (pieceColor == color) {
            std::cout << "WE FOUND A PIECE BOIII\n";
            if (PIECES[value] == PAWN_NUMBER) {
                determine_pawn_moves(board, moves, key);
            }

            else if (PIECES[value] == ROOK_NUMBER) {
                determine_rook_moves(board, moves, key);
            }

            else if (PIECES[value] == KNIGHT_NUMBER) {
                std::cout << "WE FOUND A KNIGHT\n";
                determine_knight_moves(board, moves, key);
            }

            else if (PIECES[value] == BISHOP_NUMBER) {
                determine_bishop_moves(board, moves, key);
            }

            else if (PIECES[value] == QUEEN_NUMBER) {
                determine_queen_moves(board, moves, key);
            }

            else if (PIECES[value] == KING_NUMBER) {
                determine_king_moves(board, moves, key, castleRights);
            }
        }

    }

    return moves;
}
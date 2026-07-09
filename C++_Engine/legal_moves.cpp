#include <aliases.h>
#include <position.h>

moveList determine_legal_moves(Position pos, moveList allMoves) {
    moveList legalMoves{};
    Board board = pos.board;
    int movingColor = pos.sideToMove;

    for (AMove move : allMoves) {
        auto& [start, end, extra] = move;
    
        // Need to define make_move()
    }
}
#include <moves.h>
#include <aliases.h>
#include <position.h>

undoMove make_move(Position pos, AMove move) {
    auto&[start, end, extra] = move;
    int castleRights = pos.castleRights;
    int numPieces = pos.pieces;
    uint64_t hash = pos.hash;
    
}
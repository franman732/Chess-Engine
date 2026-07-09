#pragma once

#include "moves.h"
#include "validation.h"
#include "aliases.h"

#include <array>
#include <vector>

constexpr std::array<int, 64> create_square_row() {
    std::array<int, 64> tempArray {};
    for (int i = 0; i < 64; i++) {
        tempArray[i] = i >> 3;
    }

    return tempArray;
}

constexpr std::array<int, 64> create_square_column() {
    std::array<int, 64> tempArray {};
    for (int i = 0; i < 64; i++) {
        tempArray[i] = i & 7;
    }

    return tempArray;
}

inline constexpr std::array<int, 64> SQUARE_ROW = create_square_row(); 
inline constexpr std::array<int, 64> SQUARE_COLUMN = create_square_column();

constexpr Raytable create_diagonal_rays(){
    Raytable finalRay {};

    std::array<std::pair<int, int>, 4> directions = {{
        {-1, -1}, {-1, 1}, {1, -1}, {1, 1}
    }};

    for (int sq = 0; sq < 64; sq++) {
        std::array<std::array<int, 7>, 4> squareRay {{
            {{-1, -1, -1, -1, -1, -1, -1}},
            {{-1, -1, -1, -1, -1, -1, -1}},
            {{-1, -1, -1, -1, -1, -1, -1}},
            {{-1, -1, -1, -1, -1, -1, -1}}
        }};

        int row = sq >> 3; int col = sq & 7;

        for (int i = 0; i < directions.size(); ++i) {
            int r = row + directions[i].first;
            int c = col + directions[i].second;

            int counter = 0;
            while ((0 <= r && r < 8) && (0 <= c && c < 8)) {
                squareRay[i][counter] = (r * 8 + c);
                r += directions[i].first;
                c += directions[i].second;
                counter += 1;
            }
        }
        finalRay[sq] = squareRay; 
    }

    return finalRay;
}

constexpr Raytable create_straight_rays(){
    Raytable finalRay {};

    std::array<std::pair<int, int>, 4> directions = {{
        {0, -1}, {0, 1}, {-1, 0}, {1, 0}
    }};

    for (int sq = 0; sq < 64; sq++) {
        std::array<std::array<int, 7>, 4> squareRay {{
            {{-1, -1, -1, -1, -1, -1, -1}},
            {{-1, -1, -1, -1, -1, -1, -1}},
            {{-1, -1, -1, -1, -1, -1, -1}},
            {{-1, -1, -1, -1, -1, -1, -1}}
        }};

        int row = sq >> 3; int col = sq & 7;

        for (int i = 0; i < directions.size(); ++i) {
            int r = row + directions[i].first;
            int c = col + directions[i].second;

            int counter = 0;
            while ((0 <= r && r < 8) && (0 <= c && c < 8)) {
                squareRay[i][counter] = (r * 8 + c);
                r += directions[i].first;
                c += directions[i].second;
                counter += 1;
            }
        }
        finalRay[sq] = squareRay; 
    }

    return finalRay;
}

constexpr std::array<std::array<int, 8>, 64> create_knight_attacks() {
    std::array<std::array<int, 8>, 64> finalRay {};
    std::array<int, 8> change = {6, 10, 15, 17, -6, -10, -15, -17};

    for (int sq = 0; sq < 64; sq++) {
        std::array<int, 8> targets {-1, -1, -1, -1, -1, -1, -1, -1};

        int counter = 0;
        for (auto diff : change) {
            int target = sq + diff;
            if (valid_knight_move(sq, target)) {
                targets[counter] = target;
            }
            counter += 1;
        }
        finalRay[sq] = targets;
    }
    return finalRay;
}

constexpr std::array<std::array<int, 8>, 64> create_king_attacks() {
    std::array<std::array<int, 8>, 64> finalRay {};
    std::array<std::pair<int, int>, 8> directions = {{
        {-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}
    }};

    for (int sq = 0; sq < 64; sq++) {
        std::array<int, 8> targets {-1, -1, -1, -1, -1, -1, -1, -1};
        int row = sq >> 3; int col = sq & 7;

        for (int i = 0; i < directions.size(); ++i) {
            int r = row + directions[i].first;
            int c = col + directions[i].second;

            int target = (r * 8 + c);
            if (valid_pawn_move(sq, target)) {
                targets[i] = target;
            }
        }
        finalRay[sq] = targets;
    }
    return finalRay;
}

inline constexpr auto DIAGONAL_RAYS = create_diagonal_rays();
inline constexpr auto STRAIGHT_RAYS = create_straight_rays();
inline constexpr auto KNIGHT_ATTACKS = create_knight_attacks();
inline constexpr auto KING_ATTACKS = create_king_attacks();
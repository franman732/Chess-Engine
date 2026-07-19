#pragma once // This contains all the information necessary for dealing with transposition tables

#include "aliases.h"

#include <random>
#include <cstdint> 
#include <unordered_map>
#include <tuple>
#include <string>

struct TT_Info {
    int depth;
    float bestEval;
    std::string flag;
    AMove bestMove;
};

struct TT_tracker {
    int TT_Lookups;
    int TT_Hits;
    int numberOfRecursions;
};

std::unordered_map<uint64_t, TT_Info> TT;
std::mt19937_64 gen(std::random_device{}());  // Defines a random number generator that can be called to using gen()

inline std::array<std::array<uint64_t, 64>, 25> ZOBRIST = []{
    std::array<std::array<uint64_t, 64>, 25> table{};

    for (auto& piece : table) {
        for (auto& square : piece) {
            square = gen();
        }
    }

    return table;
}();

uint64_t ZOBRIST_SIDE = gen();
std::unordered_map<int, int> ZOBRIST_CASTLE;

inline std::array<std::array<uint64_t, 64>, 25> PAWN_ZOBRIST = [] {
    std::array<std::array<uint64_t, 64>, 25> table{};

    for (auto& piece : table) {
        for (auto& square : piece) {
            square = gen();
        }
    }

    return table;
}();

std::unordered_map<int, std::tuple<int, int>> PAWN_HASH_TABLE;

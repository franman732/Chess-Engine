#pragma once // This contains all the information necessary for dealing with transposition tables

#include <random>
#include <cstdint> 
#include <unordered_map>
#include <tuple>

std::unordered_map<int, int> TT;

std::mt19937_64 gen(std::random_device{}());  // Defines a random number generator that can be called to using gen()

std::array<std::array<uint64_t, 64>, 33> ZOBRIST;
uint64_t ZOBRIST_SIDE;
std::unordered_map<int, int> ZOBRIST_CASTLE;

std::array<std::array<uint64_t, 64>, 25> PAWN_ZOBRIST;
std::unordered_map<int, std::tuple<int, int>> PAWN_HASH;

int compute_hash(const std::array<int, 64>& board, int sideToMove, int castle);

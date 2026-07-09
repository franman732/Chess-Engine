#pragma once

#include <tuple>
#include <vector>
#include <array>

using AMove = std::tuple<int, int, int>;
using moveList = std::vector<AMove>;

using Board = std::array<int, 64>;

using Raytable = std::array<std::array<std::array<int, 7>, 4>, 64>;

using scoredMove = std::pair<int, AMove>;
using scoredMoves = std::vector<scoredMove>;
#pragma once

#include <array>

constexpr int abs_constexpr(int x) {
    return (x < 0) ? -x : x;
}

constexpr std::array<int, 8> make_filled_array() {
    std::array<int, 8> arr {};
    arr.fill(-1);
    return arr;
}
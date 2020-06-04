//! clang++ -Wall -std=c++17 multi-retval.cc
#include <iostream>
#include <stdexcept>
#include <tuple>
#include <vector>
using namespace std;

tuple<int, int> gcd_lcm(int a, int b) {
  if (a == b || a == 0 || b == 0) {
    throw logic_error("这还用问我？");
  }
  // 确保 x > y
  // 解包语法：C++ 17
  auto [x, y] = a < b ? make_tuple(b, a) : make_tuple(a, b);
  // 辗转相除法
  while (x % y != 0) {
    auto tmp = x % y;
    x = y;
    y = tmp;
  }
  return make_tuple(y, a * b / y);
}

int main() {
  int a = 0;
  int b = 0;
  cin >> a >> b;
  auto [max_factor, min_prod] = gcd_lcm(a, b);
  cout << max_factor << ", " << min_prod << endl;
  return 0;
}
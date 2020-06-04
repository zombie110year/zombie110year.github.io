#include <iostream>
using namespace std;

bool (*must_true(int a, int b))(const int &, const int &) {
  if (a > b) {
    return [](const int &a, const int &b) { return a > b; };
  } else {
    return [](const int &a, const int &b) { return a <= b; };
  }
}

auto must_false(int a, int b) -> bool (*)(const int &, const int &) {
  if (a > b) {
    return [](const int &a, const int &b) { return a <= b; };
  } else {
    return [](const int &a, const int &b) { return a > b; };
  }
}

int main() {
  int a = 10;
  int b = 20;
  auto ft = must_true(a, b);
  auto ff = must_false(a, b);
  cout << ft(a, b) << endl << ff(a, b) << endl;
  return 0;
}
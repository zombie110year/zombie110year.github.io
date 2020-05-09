#include <iostream>
#include <string>

int main() {
  int input;
  std::cin >> input;
  switch (input) {
  case 1: {
    double x = 0;
    std::cout << x << std::endl;
  }
  default:
    break;
  }
  return 0;
}
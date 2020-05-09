#include <iostream>

int main() {
  int input;
  std::cin >> input;
  switch (input) {
  case 1:
    // 未初始化
    double y;
  default:
    std::cin >> y;
    std::cout << y << std::endl;
    break;
  }
  return 0;
}
#include <iostream>
#include <string>

int main() {
  int input;
  std::cin >> input;
  switch (input) {
  case 1:
    // 初始化     jump bypasses variable initialization
    double x = 0;
    // 未初始化
    double y;
    // 显式初始化 jump bypasses variable initialization
    std::string s1("Hello World");
    // 隐式初始化 jump bypasses variable initialization
    std::string s2;
    // 初始化但未使用 jump bypasses variable initialization
    double z = 1;
  default:
    std::cout << x << std::endl
              << y << std::endl
              << s1 << std::endl
              << s2 << std::endl;
    break;
  }
  return 0;
}
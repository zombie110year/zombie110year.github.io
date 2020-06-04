#include "SalesItem.h"

int main() {
  SalesItem sum;
  std::cin >> sum;
  SalesItem cur;
  while (std::cin >> cur) {
    if (cur.isbn() == sum.isbn()) {
      sum += cur;
    } else {
      std::cerr << "期望相同的 ISBN：" << cur.isbn() << " != " << sum.isbn()
                << std::endl;
      return -1;
    }
  }
  std::cout << sum << std::endl;
  return 0;
}
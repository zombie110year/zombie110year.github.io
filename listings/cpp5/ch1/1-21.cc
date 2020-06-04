#include "SalesItem.h"

int main() {
  SalesItem a, b;
  std::cin >> a;
  std::cin >> b;
  if( a.isbn() == b.isbn()) {
    std::cout << a + b << std::endl;
  } else {
    std::cerr << "期望相同的 ISBN: " << a.isbn() << " != " << b.isbn() <<std::endl;
    return -1;
  }
  return 0;
}
#include <iostream>
int counter() {
    static int ctr = 0;
    return ++ctr;
}
int main() {
    for(int i = 0; i < 10; ++i) {
        std::cout << counter() << ", ";
    }
    std::cout << std::endl;
    return 0;
}

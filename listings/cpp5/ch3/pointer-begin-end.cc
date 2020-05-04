#include <iostream>
using std::begin;
using std::end;

int main() {
    int arr[10] = {1, 2, 3, 4, 5, 6, 7, 8 ,9, 0};
    auto b = begin(arr);
    auto c = end(arr) - 1;
    for(;b < c; ++b, --c) {
        auto tmp = *c;
        *c = *b;
        *b = tmp;
    }
    for(auto c: arr) {
        std::cout << c;
    }
    std::cout << std::endl;
    return 0;
}
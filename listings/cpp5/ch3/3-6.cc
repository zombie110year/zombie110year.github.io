#include <string>
#include <iostream>
#include <cctype>
using namespace std;

int main() {
    string s0("hello world, this is c++, namely c plus plus.");
    for(auto &c: s0) {
        if (isalpha(c)) {
            c = 'x';
        }
    }
    cout << s0 << endl;
}
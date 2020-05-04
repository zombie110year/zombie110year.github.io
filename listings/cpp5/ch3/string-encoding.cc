#include <string>
#include <iostream>

using std::cout;
using std::endl;
using std::string;

int main() {
    string s1("你好呀");
    string s2("Hello World");

    // 如果按字符存储，则应为 3 好
    cout << s1.size() << s1[2] << endl;
    // 11 e
    cout << s2.size() << s2[2] << endl;
    return 0;
}

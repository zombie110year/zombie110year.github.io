#include <iostream>
#include <string>
#include <vector>
using namespace std;

string join_str(vector<string> src, string sep);

int main() {
    vector<string> src = {
        "abc",
        "efg",
        "hij",
        "klm",
    };
    auto result = join_str(src, "XXX");
    cout << result << endl;
    return 0;
}

string join_str(vector<string> src, string sep) {
  string writer;
  switch (src.size()) {
  case 0:
    return writer;
  case 1:
    return src[0];
  default:
    writer.append(src[0]);
    for (size_t i = 1; i < src.size(); i++) {
      writer.append(sep);
      writer.append(src[i]);
    }
    return writer;
  }
}
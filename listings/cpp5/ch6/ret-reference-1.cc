#include <iostream>
using namespace std;

int &get_item(int arr[], size_t index) { return arr[index]; }

int main() {
  int arr[] = {1, 2, 3, 4};
  auto &x = get_item(arr, 2);
  x = 999;
  for (auto i : arr) {
    cout << i << endl;
  }
}
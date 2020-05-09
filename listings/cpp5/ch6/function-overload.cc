#include <iostream>
using namespace std;
void print(int x) { cout << x << endl; }
void print(const int arr[], size_t len) {
  for (size_t i = 0; i < len - 1; ++i) {
    cout << arr[i] << ", ";
  }
  cout << arr[len - 1] << endl;
}
int main() {
  print(1);
  int arr[] = {1, 2, 3, 4, 5};
  print(arr, 3);
}
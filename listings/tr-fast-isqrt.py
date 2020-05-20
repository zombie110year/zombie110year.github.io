def count(title: str):
    class Counter:
        def __init__(self, fn):
            self._fn = fn
            self._c = 0
            self.r = None

        def __call__(self, *args, **kwargs):
            self._c += 1
            self.r = self._fn(*args, **kwargs)
            return self.r

        def show(self):
            print(f"{title}[{self._c}]: {self.r}")

    return Counter


@count("isqrt1")
def isqrt1(x: int) -> int:
    if x == 0:
        return 0
    else:
        r2 = isqrt1(x - 1)
        r3 = r2 + 1
        if x < r3 * r3:
            return r2
        else:
            return r3


@count("isqrt2")
def isqrt2(x: int) -> int:
    if x == 0:
        return 0
    else:
        z = x // 4
        r2 = 2 * isqrt2(z)
        r3 = r2 + 1
        if x < r3 * r3:
            return r2
        else:
            return r3

def nroot(n: int):
    "Curring 化，以便携带 show 方法"
    b = 2**n

    @count("nroot")
    def nroot_(x: int):
        if x == 0:
            return x
        else:
            z = x // b
            r2 = 2* nroot_(z)
            r3 = r2 + 1
            if r3**n < x+1:
                return r3
            else:
                return r2

    return nroot_

if __name__ == "__main__":
    n = 156
    isqrt1(n)
    isqrt2(n)

    x, b = 128, 3
    nroot_ = nroot(b)
    nroot_(x)

    isqrt1.show()
    isqrt2.show()
    nroot_.show()
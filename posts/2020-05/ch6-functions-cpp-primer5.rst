---
title: '第六章：函数 | C++ Primer 5'
slug: 'ch6-functions-cpp-primer5'
date: 2020-05-09 16:05:07 UTC+08:00
tags:
- c++
category: note
description:
type: text
---

.. contents::

.. TEASER_END

############
局部静态变量
############

.. listing:: cpp5/ch6/local-static.cc cpp

``ctr`` 只会初始化一次，且其生命周期贯穿从开始调用到整个程序结束。

########
引用传参
########

默认的传参行为是拷贝，而当形式参数为引用时，则不会发生拷贝：

.. code:: cpp

    void reset0(int n) {
        // n 是一个被复制的新值
        n = 0;
    }
    void reset1(int* n) {
        // n 是一个指向一个 int 的指针
        *n = 1;
    }
    void reset2(int& n) {
        // n 是一个引用
        n = 2;
    }
    int main() {
        int x = 3;
        reset0(x);
        // x == 3
        reset1(&x);
        // x == 1
        reset2(x);
        // x == 2
    }

在旧的 C/C++ 编程风格中，可能会要求使用引用或指针参数使函数能够「返回」多个值：

.. code:: cpp

    int do_sth(int arg0, int arg1, int* ret1, int& ret2) {
        if (true) {
            return 0;
        } else {
            return -1;
        }
    }

这种用例下，返回值通常代表函数的执行状态，例如在 C 代码中，大量使用 -1 作为发生错误时的返回值，而真正的返回值则通过指针或引用赋值给外界的变量，
C 语言 Socket 编程中可以看到大量的例子。
在 C 语言中，由于语言本身的限制而不得不使用此种编程风格，但在 C++ 中，
错误处理应当使用 try-catch，而多返回值完全可以使用标准库的 ``tuple`` 类：

.. listing:: cpp5/ch6/multi-retval.cc cpp

##########
const 形参
##########

在形式参数上用 const 修饰，将在函数作用域中禁止对该参数的修改，无论传递的实参是普通变量还是常量。

########
数组形参
########

在形参表中可以声明数组：

.. code:: cpp

    void print(int[] arr);
    void print(int* arr);
    void print(int[100] arr);

以上三种定义是等价的：

* 数组类型将被转化为指针
* 指定数组的长度只有参考意义，实际调用时可以接受任何长度的数组

传递数组跳不开处理范围，通常有三种标识范围的风格：

.. code:: cpp

    // 1. 在数据中标识末尾，例如 C 字符串
    void print(const char str[]) {
        if (str) {
            while(*str != '\0') {
                cout << *str++;
            }
        }
    }

.. code:: cpp

    // 2. 使用 C++ 迭代器规范，所有 STL 容器都支持
    void print(const char* begin, const char* end) {
        while(begin != end) {
            cout << *begin++;
        }
    }

.. code:: cpp

    // 3. 显式指定长度，如果想要 FFI 通用性就选这个
    void print(const char str[], size_t len) {
        for(size_t i = 0; i < len; ++i) {
            cout << str[i];
        }
    }

注意，如果声明数组形式的变量，方括号要放在标识符后面，而不是紧跟着类型定义。

######
返回值
######

引用返回左值：

.. listing:: cpp5/ch6/ret-reference-1.cc

C++ 提供了标注返回类型的新方法：

尾置返回类型
    .. code:: cpp

        auto fn(/* parameters */) -> /* return type */;
decltype
    用于已知返回值的可选范围时，例如返回一个定义过的对象的指针：

    .. code:: cpp

        int A[] = {1, 2, 3, 4};

        decltype(A) *fn(/* param */);

########
函数重载
########

C++ 编译器用来确定函数的因素除了函数名之外，还有各个参数的类型。
对于同名的函数，如果声明了不同类型的形式参数，那么将编译生成不同的函数，
这种行为叫「函数重载」：

.. listing:: cpp5/ch6/function-overload.cc

形参的名字与重载无关
    重载只与形参的类型有关，如果类型相同，只有名字相同，那么将报错「重复定义」。
顶层或底层 const
    重载会忽略顶层常量（修饰在后）而考虑底层常量（修饰在前）。

    .. code:: cpp

        // 两者等价
        // const 修饰的是指针，指针本身不可变
        int fn(int* const);
        int fn(int*);

        // 两者不同
        // const 修饰的是指针指向的对象，指针本身可变，但对象不可变
        int fn(const int*);
        int fn(int*);

    原因是传参时指针本身就是副本，无论是否 const 都不会影响到主调函数方的变量，
    因此编译期会忽略这种 const。

当调用一个存在重载的函数时，将发生以下步骤：

函数匹配（重载确定）
    编译期检查是否存在与实际参数向匹配的重载函数。
    如果存在且唯一，那么生成相关代码，否则：
无匹配
    找不到匹配的重载函数，编译终止。
二义性
    存在多个可匹配的重载函数，编译终止。

在编译重载函数时，函数名的实际符号将被扩展为类似::

    name@type1@const_type2 ...

.. abbr:: ABI

    Application Binary Interface

样式的新符号，这也是重载的本质，这个过程通常称为 mangle，属于 :abbr:`ABI` 的一部分。
不同的编译器实现使用不同的重载样式，MSVC 和 GCC 的行为就不一致，所以双方编译的程序不可互相链接。

实参类型转换
============

转换存在优先级：

1. 精确匹配：
    -   实参类型和形参类型相同；
    -   数组转指针；
    -   增减 const；
2. const_cast 转换；
3. 类型提升；
4. 算术类型转换或指针转换；
5. 类类型转换。

########
默认参数
########

.. code:: cpp

    void hello(string name, string greed = "Hello") {
        cout << greed << ", " << name << endl;
    }

- 在形参定义时使用 ``= val`` 可以设定默认实参，当调用函数时没有在对应位置处传入实参，则将隐式传入默认实参。
- 如果要为参数设置默认值，则它后面的参数也必须有默认值。
- 默认实参要么是编译期就能确定的常量、字面量，要么就必须拥有大于函数的作用域。
- 当使用变量作为默认实参时，变量的解析发生在调用时。

########
函数指针
########

一个函数的声明::

    bool cmp(const int&, const int&);

对应的函数指针声明::

    bool (*cmp_ptr)(const int&, const int&);

该函数的类型表示::

    bool(const int&, const int&)

    using F = bool(const int&, const int&);
    using FP = bool(*)(const int&, const int&);

对于返回函数指针的函数定义，需要显式声明返回值为指针类型::

    FP fn();
    F *fn();

    // 错误，不会自动转换类型
    F fn() {
        // ...
    }
    FP x = fn();

如果不使用别名，而是直接定义函数指针返回值的话，建议使用尾缀方式::

    auto f(int a, int b) -> bool(*)(const int&, const int&) {
        // ...
    }

否则，要阅读起来就太费劲了::

    bool (*f(int a, int b))(const int&, const int&) {
        // ...
    }

.. listing:: cpp5/ch6/must-ret-tof.cc
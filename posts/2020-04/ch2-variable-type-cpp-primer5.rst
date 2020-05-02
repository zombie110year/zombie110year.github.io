---
title: '第二章：变量和基本类型 | C++ Primer 5'
slug: 'ch2-variable-type-cpp-primer5'
date: 2020-04-30 11:35:02 UTC+08:00
tags:
- c++
category: note
description:
type: text
---

.. contents::

.. TEASER_END

##############
指定字面量类型
##############

字符串
======

.. list-table::
    :header-rows: 1
    :widths: 5 10 20

    *   -   前缀
        -   类型
        -   含义
    *   -   u
        -   char16_t
        -   USC 16 编码的字符串
    *   -   U
        -   char32_t
        -   USC 32 编码的字符串
    *   -   L
        -   wchar_t
        -   宽字符
    *   -   u8
        -   char
        -   UTF 8 编码的字符串

整数
====

.. list-table::
    :header-rows: 1

    *   -   后缀
        -   类型
        -   含义
    *   -   u,U
        -   unsigned
        -   无符号
    *   -   l,L
        -   long
        -   加长
    *   -   ll,LL
        -   long long
        -   双倍加长

浮点数
======

.. list-table::
    :header-rows: 1

    *   -   后缀
        -   类型
        -   含义
    *   -   f,F
        -   float
        -   浮点数
    *   -   l,L
        -   long double
        -   加长浮点数

##########
列表初始化
##########

四种初始化形式：

.. code:: cpp

    int x = 0;
    int x = {0};
    int x {0};
    int x (0);

如果使用列表初始化，提供的初始值存在信息丢失的风险的话，那么编译器将报错。

使用花括号
    如果存在信息丢失风险则报错。
不使用花括号
    隐式信息截断。


##########
默认初始化
##########

定义在函数外的变量将被自动初始化为 0，
但定义在函数内的变量 **不会自动初始化**，在初始化它们之前访问它们的值是 :abbr:`UB`。

########
声明变量
########

.. code:: cpp

    extern int i;

将声明一个名为 ``i`` 的变量，不能初始化，否则将被理解为定义。

.. code:: cpp

    // 声明
    extern int x;
    // 声明并定义
    int y;
    // 声明并定义并初始化
    int z = 1;
    // 声明并定义并初始化
    extern int a = 0;

##############
引用：左值引用
##############

-   引用的类型表示法是 ``T&``，例如 ``int`` -> ``int&``，``&`` 在定义时是靠在标识符一侧的；
-   引用必须初始化；
-   引用的语义为「绑定」而非「拷贝」；
-   引用是创建了表示同一值的多个名字，对任何一个引用进行的操作都会影响到目标值。

.. code:: cpp

    int x = 123;
    int& y = x;

在初始化时，如果在同一条语句初始化多个引用，那么 ``&`` 在每个名字前都要出现一次（靠在标识符一侧）：

.. code:: cpp

    int x, y; // int, int
    int &a, &b; //int&, int&
    int s, &t; // int, int&

.. note:: 引用只在编译期存在？

####
指针
####

指针是一个存储了对象在内存中地址的值。和引用不一样，它可以在不同作用域之间传递、复制，它是一个值，而不是一个名字（符号）。

-   指针的类型表示法是 ``T*``，例如 ``int`` -> ``int *``，类似引用，``*`` 在定义时是靠在标识符一侧的；
-   指针可能空悬（指向一个未使用的地址）；
-   指针的语义是「指向」而非「存储」；
-   可以对右值使用 ``&`` 取地址运算符；
-   可以对指针使用 ``*`` 解引用运算符来访问目标地址。

.. code:: cpp

    int* a = nullptr; // 默认指向 0 指针，这个地址受操作系统保护，无法读写
    int x = 123;
    int* xx = &x; // 指向 x 的地址


.. code:: cpp

    int x = 0;
    int* p = &;

    cout << "指针： " <<  p << endl;
    cout << "数值： " << *p << endl;

给指针赋值，语义为修改指针存放的地址，从而指向新的对象。
给指针解引用后赋值，语义为修改指针所指向的对象。


.. note:: & * 的上下文相关性

    ``&`` 和 ``*`` 的含义与它们所处的位置有关：

    .. code:: cpp

        int x = 0;
        int &r = x;     // & 与类型一起，为声明的一部分，表示引用
        int *p;         // * 与类型一起，为声明的一部分，表示指针
        p = &x;         // & 在表达式中，为运算符，表示取地址
        *p = 42;        // * 在表达式中，为运算符，表示解引用


############
const 限定符
############

const 的作用是告诉编译器，让它禁止对某个变量的修改，
如果在程序中编写了修改被 `const` 修饰的变量，那么就无法通过编译。

这种限制只存在于编译期，如果编写了能在运行期获取对象指针并修改的方法，
那么就可能绕过此限制。不过这种设置都是为了避免一些安全问题，所以不要去卡 BUG。

const 必须初始化
    代码中存在未初始化的 const 变量会无法通过编译。
const 不限制读取，可以用来给其他变量赋值
    const 只是限制写入。
不同文件的同名 const 对象独立存储
    const 值默认在每个文件中独立定义，如果要在多个文件中共享，
    须在定义的同时进行 extern 声明：

    .. code:: cpp

        extern const int zero = 0;

##################
const 与引用和指针
##################

.. code:: cpp

    // const 修饰 int&
    const int& x;
    //* 和 const int & 表示相同语义
    int const& x;
    //! const 运算符不能修饰 int& 的实例 x
    int& const x;
    // const 修饰 int*
    const int* x;
    //* 与 const int* 语义相同
    int const* x;
    // const 修饰 x
    int *const x;

const 修饰 int&
    引用是一个常量，它指向一个确定的对象，但不能修改它。
const 修饰 int*（底层常量）
    指针 x 所指向的是一个常量，不能被修改，不过指针本身可以被修改：

    .. code:: cpp

        #include <iostream>
        using namespace std;
        int main() {
            int n = 0;
            int m = 1;
            const int* x = &n;
            cout << x << endl;
            x = &m;
            cout << x << endl;
            //! 无法通过编译
            // *x = m;
            // cout << x << endl;
            return 0;
        }
const 修饰 x（顶层常量）
    指针本身是一个常量，不可修改，但不限制它修改它所指向的对象（除非它的指向也用 const 修饰）

    .. code:: cpp

        #include <iostream>
        using namespace std;
        int main() {
            int n = 0;
            int m = 1;
            int* const x = &n;
            cout << x << endl;
            //x = &m;
            //cout << x << endl;
            *x = m;
            cout << x << endl;
            return 0;
        }

.. topic:: 顶层常量和底层常量

    顶层
        指针本身是一个常量
    底层
        指针指向的对象是一个常量

const 可以用多次，来同时表示顶层和底层常量：

.. code:: cpp

    const int* const x = 0;


######################
constexpr 和常量表达式
######################

常量表达式的值必须要能在编译期就计算得出，并使用 constexpr 修饰。
和 const 修饰的值相比，常量表达式的检查更严格，不允许使用没有用 const 或 constexpr 修饰，但能够在编译期计算得出的值。

.. code:: cpp

    // 无法编译
    constexpr int a = 1;
    const int b = 2;
    int c = 3;
    constexpr int x = a + b + c;

.. code:: cpp

    // 可以编译
    const int a = 1;
    int b = 2;
    const int x = a + b;

.. code:: cpp

    // 可以编译
    constexpr int a = 1;
    const int b = 2;
    constexpr x = a + b;

和 const 修饰符相比，constexpr 用在指针的声明时，只对指针有效，与指针所指的对象无关。


########
处理类型
########

typedef 与 using
================

C 语言中定义类型别名
    .. code:: c

        typedef { old } { new };
C++11 新标准
    .. code:: cpp

        using { new } = { old };

和旧用法相比，using 更加清晰，例如对数组和指针：

.. code:: cpp

    typedef char* pstr;
    using pstr = char*;

    typedef char* astr[];
    using astr = char*[];

以及对函数指针：

.. code:: cpp

    #include <iostream>
    // 将 (int, int) -> int 类型的函数指针命名为 iioi
    typedef int(*iioi)(int, int);

    int add(int a, int b) {
        return a + b;
    }

    int main() {
        using namespace std;
        iioi fn = &add;
        cout << (*fn)(1, 3) << endl;
        return 0;
    }

传统的 typedef 基本上是::

    typedef { 返回值类型 }(* { 新定义的类型名 })({ 形式参数的类型 });

.. code:: cpp

    #include <iostream>

    using iioi = int(*)(int, int);

    int add(int a, int b) {
        return a + b;
    }

    int main() {
        using namespace std;
        iioi fn = &add;
        cout << (*fn)(1, 3) << endl;
        return 0;
    }

把新的类型名后旧的声明放到等号两边，能增加可读性。


auto 类型自动推导
=================

auto 声明能根据初始化值自动推导变量类型，存在以下规则：

1. 若初始化值为一个引用，那么 auto 将推导为解引用后的类型，`int& -> int`，除非使用 & 修饰 auto，`auto & r = x;`；
#. auto 会忽略顶层 const 而保留底层 const，除非用 const 修饰 auto，`const auto x`；


decltype 计算表达式的类型
=========================

auto 用于变量定义，而 decltype 用于计算表达式的类型。
这一个过程发生在编译期：

.. code:: cpp

    #include <iostream>
    int add(int a, int b) {
        return a + b;
    }
    using iioi = decltype( &add );

    int main() {
        using namespace std;
        iioi fn = &add;
        cout << (*fn)(1, 3) << endl;
        return 0;
    }

和 auto 相比， decltype 不会自动解引用。
而且，它处理带括号的表达式时，如果有多余的括号，会将括号处理为引用。
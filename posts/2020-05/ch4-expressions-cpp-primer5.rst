---
title: '第四章：表达式 | C++ Primer 5'
slug: 'ch4-expressions-cpp-primer5'
date: 2020-05-08 15:31:52 UTC+08:00
tags:
-   c++
category: note
description:
type: text
---

这一章内容比较简单，大多数编程语言在此拥有一致的性质，触类旁通。

.. contents::

.. TEASER_END

.. default-role:: code

##########
左值与右值
##########

.. list-table::
    :header-rows: 1

    -   *   角度
        *   左值
        *   右值
    -   *   从位置上看
        *   能放在赋值号（=）左侧的值（有特例：常量）
        *   不能放在赋值号（=）左侧的值
    -   *   身份
        *   表示位置（可写的变量、指针等）
        *   值（内容）
    -   *   变换
        *   左可当右（通过位置获取内容）
        *   右不可左（无法通过内容确定位置）

##############
++--表达式的值
##############

当使用 `++` `--` 运算符时，根据其位置的不同会构成不同的表达式。
例如::

    a++
    ++a

是两个不同的表达式：后缀和前缀自增表达式。

两个表达式都会使 `a += 1`，但它们会返回不同的右值，下面的 `a` 都表示其原始值：

前缀式
    得到自增后的值。
后缀式
    得到自增前的值。

    由于需要保存临时变量，因此效率低于前缀式；除非必要，不建议使用。

::

    ++a     ->      (a + 1)
    a++     ->      (a)

######
位运算
######

右移运算符
    对于无符号类型，在边缘填零；对于有符号类型，右移运算符在左侧填充符号位副本。

############
显式类型转换
############

英文称为（cast），又名强制类型转换，通常在语法上具有以下形式::

    { cast_name }<{ type }>({ expression })

cast_name 代表了不同的转换方式，一共有四种：

static_cast
    具有明确定义的静态类型可以使用此转换。例如::

        void* -> int*:
            int x = 0;
            void* p = &x;
            int* ip = static_cast<int*>(p);

        int -> double:
            int x = 5;
            double s = static_cast<double>(x) / 3.0;

    对于指针，在转换时不会修改它的指向，只是变换解读方式，因此需要保证转换目标就是指针所指向内容的类型，否则产生 :abbr:`UB`。
const_cast
    用来去掉 const 修饰变量的写限制，将常量转换为非常量。
reinterpret_cast
    仅仅用于重新解释，而不会修改被转换目标的值。
    这个操作非常危险，一般只用于底层 Hack，例如那个著名的平方根算法 [#Q_rsqrt]_ ，
    由于其在 bit 层 Hack 了 float 和 long ，因此可以使用此转换。
dynamic_cast
    用于运行时类型识别，见原书 730 页。

########
参考链接
########

.. [#Q_rsqrt] https://en.wikipedia.org/wiki/Fast_inverse_square_root#Overview_of_the_code
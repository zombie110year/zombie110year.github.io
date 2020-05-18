---
title: '第一章：开始 | C++ Primer 5'
slug: 'ch1-start-cpp-primer5'
date: 2020-04-29 21:38:59 UTC+08:00
tags:
- c++
category: code
description: |
    《C++ Primer 第五版》 第一章节读书笔记
type: text
---

.. contents::

.. TEASER_END

.. default-role:: code

#########
main 函数
#########

操作系统运行一个程序需要找到一个入口，`main` 函数就是 C++ 程序的入口。

.. code:: cpp

    int main(int argc, char* argv[]) {
        return 0;
    }

:param int argc: 从命令行传入参数的数目；
:param (char*)[] argv: 从命令行传入的参数组成的数组，C-style 字符串；
:return int: 返回值作为程序的退出状态，约定 0 表示正常，其他值表示出现错误。

########
iostream
########

`iostream` 库提供了输入输出能力，包含两个类 `istream`, `ostream`。
其中， `i` 表示 in，所以是读；`o` 表示 out, 是写。

iostream 提供的读写功能以 **流** 的形式提供，「流」表示读写是顺序生成或消耗的。

提供了四个标准读写对象：

cin
    标准输入
cout
    标准输出
cerr
    标准错误输出
clog
    标准日志输出

从 C++ 程序到操作系统，c* 等标准输入输出可能会映射为不同的文件、缓冲区等，
通常来说，默认配置下的程序，其标准输入输出都连接至控制台。

c* 使用 `<<` 和 `>>` 两个运算符，前者表示将某个东西送入 c*，后者表示从 c* 抽出：

.. code:: cpp

    // 导入符号，这样编译器才能在标准库中找到对应的对象
    #include<iostream>
    int main() { // 不需要命令行参数，可以省略掉 main 的形式参数
        // 标准库中的符号在 std 命名空间下，这里的声明让编译器知道后面的符号到 std:: 下去找
        using namespace std;
        int a = 0;
        int b = 0;
        // 从 stdin 读取一个数到 a
        cin >> a;
        // 从 stdin 读取一个数到 b
        cin >> b;
        // 向 stdout 输出
        cout << a << " + " << b << " = " << a + b << endl;
        return 0;
    }

`endl` 是 `end line` 的缩写，其作用就是终止当前行并且刷新缓冲区，根据输入模式的不同，可能会插入换行符。

测试 cout, cerr, clog 的关系：

.. code:: cpp

    #include <iostream>
    int main() {
        using namespace std;
        cout << "cout" << endl;
        cerr << "cerr" << endl;
        clog << "clog" << endl;
    }

利用操作系统文件描述符重定向的功能，将输入划分到不同的文件::

    ./a.out 1>cout.txt 2>cerr.txt 3>clog.txt

cout 的文件描述符是 1，cerr 和 clog 的文件描述符都是 2 。

.. note:: 形式参数和实际参数

    形式参数指在函数定义时写在后面的参数，其作用是表示一个符号、一个名字。
    实际参数则是传递给函数的实际的值。

`::` 是作用域运算符，作用是解开一层命名空间。C++ 中的命名空间设定是为了避免名字冲突。
如果没有命名空间则为了编译链接时，不将错误的代码链接到重复的符号上，就必须写很长的，不重复的名字。像 C 和 Object-C 一样。

######
控制流
######

while
=====

先判定，再执行。

.. code:: cpp

    while(x < 100) {
        x += 1;
    }

for
====

.. code:: cpp

    for(int i = 0; i < 100; i++) {
        x += i;
    }

############
cin 的布尔值
############

.. code:: cpp

    int sum = 0;
    int val = 0;
    while(cin >> val) {
        sum += val;
    }
    cout << "= " << sum << endl;

cin 读取时会自动根据变量的类型解析输入，当能够成功解析时（在本例为字符串），其布尔值相当于 true；否则为 false。空白字符（空格、制表符、换行符等）将被忽略。

因此上面这个程序在遇到非整数字面量形式的输入时，循环将会结束，输出结果。

if
====

::

    if( cond ) {

    } else if ( cond ) {

    } else {

    }


#################
类简介：SalesItem
#################

书店程序，SalesItem 代表一个出版物的销售情况。

对于类，在设计时思考它有哪些性质，能执行哪些行为：

记录ISBN 书号
    添加一个 isbn_id 的字段；
记录销售额、销量
    添加对应字段来存储数据；
通过 iostream 读写
    重载 `<<` 和 `>>` 运算符；
复制 SalesItem 实例
    使用 `=` 赋值号；
合并两条销售记录
    重载 `+` 和 `+=` 运算符；
    并且，需要保证只有相同的商品（ISBN相同）的销售记录可以合并。

######
练习题
######

练习 1.6
========

下面这段程序不合法：

.. code:: cpp

    std::cout << "Hello World" << v1;
        << " and " << v2;
        << " is " << v1 + v2 << std::end;

因为分号结束语句，上面后两行的 `<<` 运算符没有操作数。

更正：

.. code:: diff

    - std::cout << "Hello World" << v1;
    + std::cout << "Hello World" << v1
    -     << " and " << v2;
    +     << " and " << v2

练习 1.20
=========

.. listing:: cpp5/ch1/1-20.cc cpp

练习 1.21
=========

.. listing:: cpp5/ch1/1-21.cc cpp

练习 1.22
=========

.. listing:: cpp5/ch1/1-22.cc cpp

####
参考
####

.. listing:: cpp5/ch1/SalesItem.h cpp
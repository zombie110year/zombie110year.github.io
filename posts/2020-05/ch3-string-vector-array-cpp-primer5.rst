---
title: '第三章：字符串、向量和数组 | C++ Primer 5'
slug: 'ch3-string-vector-array-cpp-primer5'
date: 2020-05-04 10:57:40 UTC+08:00
tags:
- c++
category: note
description:
type: text
---

.. contents::

.. TEASER_END

######
using
######


using 语句的作用是将某个名字导入到当前作用域。

使用 using 应用默认命名空间
    假设要让之后的作用域中的符号默认在 std 命名空间中获取，则::

        using namespace std;

    :弊端:  可能引起命名空间混淆，因此尽可能少的使用：

        1.  在尽可能小的作用域中使用，例如一个函数内部
        2.  尽可能避免同时 using 两个或以上的命名空间

使用 using 提取特定成员
    假设要使用 std::cout 成员，但不希望将整个命名空间引入，则::

        using std::cout;

    这样，就可以将 std::cout 引入为 cout，而 std 命名空间中的其他成员仍然需要完整的路径。

在使用 using 时，建议遵守以下规范：

头文件中不包含 using 声明
    由于头文件会被包含到其他文件中，因此避免使用 using ，以避免名字冲突和混淆。


###########
string 类型
###########

string 类型
    :头文件: string
    :名字: std::string

注意， string 由于没有字符编码设置，因此实际上是「字节串」！

.. listing:: cpp5/ch3/string-encoding.cc cpp

初始化方法
==========

.. code:: cpp

    // 空字符串
    string s1;

    // s2 拷贝 s1
    string s2 = s1;
    string s2(s1);

    // 从字面量拷贝
    string s3 = "hello";
    string s4("hello");

    // 重复字节
    string s5(10, 'x');

==========  ==========  ========    ========    ================================
初始化方法  使用花括号  使用等号    使用括号    含义
----------  ----------  --------    --------    --------------------------------
直接初始化  否          否          是          调用对象与实参对应的构造方法
拷贝初始化  否          是          否          将右值拷贝到新创建的对象，
                                                调用复制构造方法
==========  ==========  ========    ========    ================================

常用方法
========

operator<<
    将内容写入 string（类似 ostream）。读取过程会忽略开头空白，在之后的空白处停止。

    .. listing:: cpp5/ch3/string-read.cc cpp

    ::

            Hello World
        Hello
operator>>
    从 string 读取内容（类似 istream）
getline(src, dst)
    从 src 从读取一行，写入给 dst，同时返回 src 本身
empty()
    检查是否为空字节串
size()
    检查字节的个数
s[n]
    取第 n 个字节
s1+s2
    连接 s1+s2，返回新的字符串对象
s1 == s2
    检查两个字符串内的字节是否完全一致
<, <=, >, >=
    按字节序比较大小

##########
Range For
##########

range for 可以遍历给定序列的每一个元素：

.. code:: cpp

    for(auto a: r)

默认情况下是拷贝，对 a 的修改无法影响到 r；
`auto &a` 是引用，对 a 的修改会影响到 r。

.. listing:: cpp5/ch3/3-6.cc cpp


######
Vector
######

vector 是一个模板类而非类型，可以定义其中包含的元素类型。

vector
    :头文件: vector
    :名字: std::vector
    :模板参数: T, 容器内元素的类型

vector 内部提供了容量、长度两个限定大小的字段。前者表示实际分配的内存大小，后者表示当前所有的元素数目。

初始化方法
==========

.. code:: cpp

    // 默认初始化
    vector<T> v1;

    // 拷贝初始化
    vector<T> v2(v1);
    vector<T> v2 = v1;

    // val 重复 n 个
    vector<T> v3(n, val);
    // 默认值重复 n 个
    vector<T> v4(n);

    // 列初始化
    vector<T> v5{a, b, c};
    vector<T> v6 = {a, b, c};

常用操作
========

push_back
    将一个元素添加到末尾
empty
    检查是否为空
size
    获取当前长度
其他同 string
    实际上，string 可以理解为 vector<char>

######
迭代器
######

用迭代器访问容器元素。

begin
    容器的第一个元素
end
    容器的最后一个元素的下一位。
    （尾后迭代器）

如果容器为空，则 begin 迭代器得到的也是尾后迭代器。

常用操作：

`*iter`
    解引用
`iter->member`
    访问成员
`++iter`
    指向下一个元素
`--iter`
    指向上一个元素
`iter += n`
    指向下 n 位
`iter -= n`
    指向上 n 位
`it1 - it2`
    两个迭代器之间的距离，向后为正。
`>, <, >=, <=`
    两个迭代器之间的位置关系，靠后更大。

迭代器不能随容器的更新而更新，因此在迭代器使用完毕之前不要修改容器。

####
数组
####

数组，内置功能。

在函数内声明的数组会保存在栈上，因此，需要在声明时指定容量，且容量可以在编译期计算出来。

初始化
======

.. code:: cpp

    // 容量为 10，默认初始化
    int arr[10];

    // 列表初始化，容量可以自动推断
    int arr[3] = {1, 2, 3};
    int arr[] = {1, 2, 3};

    // 字符数组需要考虑 0 字节
    char str[6] = "abcdef"; // 错
    char str[7] = "abcdef";
    char str[7] = {'a', 'b', 'c', 'd', 'e', 'f', '\0'};

    // 不能拷贝初始化
    int a[] = {1, 2, 3};
    int b[] = a;        // 错
    b = a;              // 错

修饰符从右向左绑定：

.. code:: cpp

    // 数组->int*：包含 10 个 int* 指针
    int *arr[10];

    // 数组->int->*：指向包含 10 个 int 的数组的指针
    int (*arr)[10];
    // 数组->int->&：指向包含 10 个 int 的数组的引用
    int (&arr)[10];

指针拥有和迭代器相同的性质，对其进行 +, - 运算时将使指针发生指定容量的位移。

标准库提供了 begin 和 end 函数，可以获取首元素地址和尾后地址。

.. listing:: cpp5/ch3/pointer-begin-end.cc cpp

######
C 接口
######

C++ 类型与 C 类型的交互。

string 和 C 风格字符串（字符数组）互转
======================================

.. code:: cpp

    char *str0 = "abc";
    string str1("efg");

    string str2(str0);
    char *str3 = str1.c_str();

使用数组初始化 vector
=====================

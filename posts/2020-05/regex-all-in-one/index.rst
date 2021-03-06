---
title: '正则表达式的教程'
slug: 'regex-all-in-one'
date: 2020-05-10 12:59:28 UTC+08:00
tags:
-   regex
-   python
category: tutorial
description:
type: text
---

.. contents::

.. TEASER_END

.. default-role:: code

##########
正则表达式
##########

**正则表达式** 中的字符， 可以划分为 *普通字符* 和 *元字符*， 其中，
元字符起到控制作用或者代表一个字符集等， 普通字符则表示其字面本义。
我们姑且将一个正则表达式的最小表意单元称为 「正则构造」。

元字符可以分四个大部分进行介绍:

`字符集`_
    用简短的正则构造来表示字符的集合
`量词`_
    限定一个正则构造的重复次数
`子表达式`_
    在一个表达式内部具有完整正则特性的子表达式
`断言`_
    断定正则表达式外部情况的正则构造

由于编程语言在源代码中定义字符串时， 会将反斜杠 ``\`` 转义。
而正则表达式中又多用反斜杠表示正则表达式的转义行为。 因此，
在编程语言的源代码中定义正则表达式， 大多需要使用 `\\`
来表示一个在正则表达式中可用的转义符。

.. code:: python

    # 表示一串数字
    pat = re.compile("\\d+")

如果是通过输入输出机制将字符串传递给程序进行正则表达式的设置，
那么就不需要用双反斜杠来表示转义符。 因为在这个过程中没有发生
编译器/解释器的转义行为。

.. code:: python

    pat_str = input(">>> ").strip();
    pat = re.compile(pat_str)

######
字符集
######

一个字符集，将使用较简短的写法来表示一系列字符组成的集合。
例如，对于一个字符来说，要求此表达式匹配 `*&,.` 其中之一，
就可以将这些字符放在一个字符集中：`[*&,\.]`。

自定义字符集
============

自定义字符集使用方括号 `[]` 作为边界字符， 用方括号包含的字符，
将被定义到一个字符集中：

    :code:`r""` 是 Python 中原始字符串的写法， 表示此字符串中的特殊字符不会被
    Python 转义。 由于正则表达式中也需要转义字符， 所以采用这样的写法能避免
    `\\` 这样的表达方式出现。

.. code:: python

    # []
    r"[*&，\。]"

上面这个字符集， 可以匹配 `*`， `&`， `，`， `。` 四个字符。

在自定义字符集中，元字符会表示其字面含义，例如：`[.]` `[*]` `[+]` 分别会匹配
`.`, `*`, `+` 三个字符。

也可以使用字符编码来代替字符，例如 `\x20` 代表空格，
在 ASCII 范围内的字符都可如此表示。 如果表示 Unicode，
那么不同的语言也许存在不同的表示方法， 但绝大多数语言采用 `\u编码` 的形式。

区间
----

在自定义字符集中， 可以使用 `-` 表示一个连续的字符序列区间， 例如:

.. code:: python

    r"[1-9]"
    # 表示 [123456789]

这个序列的顺序是按照字符编码顺序来排序的。 支持 Unicode 的语言都遵守
Unicode 码点顺序。

也可以将两个区间合并起来：

.. code:: python

    r"[0-9A-Za-z]"
    # 表示所有数字以及大小写字母

补集
----

自定义字符集中， 也可以使用 **非** 条件来创建一个
**不在其中的字符所组成的集合** ，只需要在字符集的第一位使用脱字符 `^` 就好：

.. code:: python

    # [^]
    r"[^0-9]"

这样的字符将表示 『不在方括号中的其他字符所组成的集合』。

预定义字符集
============

在大多数正则表达式实现中， 都预先定义了一系列常用的字符集:

+--------------+------------------------------------------------------+
| 字符集表示法 | 含义                                                 |
+==============+======================================================+
| `\d`         | `[0-9]`， 数字                                       |
+--------------+------------------------------------------------------+
| `\D`         | `[^0-9]`， 非数字                                    |
+--------------+------------------------------------------------------+
| `\w`         | 数字或字母                                           |
+--------------+------------------------------------------------------+
| `\W`         | 非数字或字母                                         |
+--------------+------------------------------------------------------+
| `\s`         | 空白字符， 例如 ` `， `\t`， `\v` 等                 |
|              | ( `\n` 一般不包括在内， 除非进行了特殊设置)。        |
+--------------+------------------------------------------------------+
| `\S`         | 非空白字符                                           |
+--------------+------------------------------------------------------+
| `。`         | 任意字符                                             |
+--------------+------------------------------------------------------+

一般都是 `\小写字母` 表示一个字符集， 而对应的 `\大写字母` 表示它的补集。

####
量词
####

量词， 用于限制一个正则构造的重复次数。 例如， 如果要表示一个 11
位的手机号码（不考虑区号、编码等规则）， 可以如何编写?

.. code:: python

    # 不使用量词
    r"\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d"
    # 使用量词
    r"\d{11}"

量词使用花括号 `{}` 来进行表示。 量词可以是一个确定的数字，
也可以是一个区间。

    m， n 表示正整数且 m < n

=========== =============
量词        含义
=========== =============
`{m}`       重复 m 次
`{m， n}`   重复 m~n 次
`{m，}`     重复至少 m 次
=========== =============

量词可以对字符， 字符集， 子表达式使用。

预定义量词
==========

========== =========
预定义量词 含义
========== =========
``*``      ``{0，}``
``+``      ``{1，}``
``?``      ``{0，1}``
========== =========

量词的贪心性
============

用于决定量词的匹配方式：

贪婪
    对于一个被量词修饰的正则构造，在 **整个表达式可以被匹配** 的前提下，为当前构造尽可能 **多** 地匹配字符。依次读取字符，当字符满足当前正则构造时就将其匹配为此构造的内容；当不满足时，就将回溯，进入下一个正则构造开始匹配。重复以上过程，直到表达式结束或字符串耗尽（匹配失败）。
懒惰
    对于一个被量词修饰的正则构造，在 **整个表达式可以被匹配** 的前提下，为当前正则构造尽可能 **少** 地匹配字符。依次读取字符，每次尝试不读入字符就匹配当前构造，如果失败，则读入一个字符进行匹配。重复以上过程，直到表达式结束或字符串耗尽（匹配失败）。

正则表达式默认以贪婪模式进行匹配， 如果要将一个正则构造设置为懒惰，
则在对应的量词后 **再** 多加一个 ``?`` 问号。

.. code:: python

    import re
    regp = re.compile(r"\d{1，5}")
    regp_l = re.compile(r"\d{1，5}?")
    # 这两个正则表达式都匹配 1 ~ 5 个数字， 一个是贪婪的， 另一个是非贪婪的

两者分别进行匹配:

.. code:: python

    >>> string = "abc0123456efg"
    >>> regp.search(string)
    <re.Match object; span=(3, 8), match='01234'>
    >>> regp_l.search(string)
    <re.Match object; span=(3, 4), match='0'>

可以看到， ``regp`` 匹配满了 5 个， 才结束了匹配， 而 ``regp_l``
只匹配了一个， 就结束了匹配。

当多个贪婪或懒惰的正则构造配合使用时， 满足以下规律
（在整个表达式可成功匹配的前提下）：

1.  每个构造都能满足最低需求
#.  优先满足贪婪构造的最高需求
#.  同为贪婪构造， 优先满足左侧(头部)构造的需求
#.  若为懒惰构造， 则多余的部分被抛弃

########
子表达式
########

正则表达式中可以使用 ``()`` 圆括号来表示一个子表达式。
子表达式和完整的正则表达式具有相同的特性：可以使用一切正则语法，
包括内嵌子表达式。

子捕获组
========

子表达式和正则表达式一样， 都是捕获的。 捕获的意思就是说，
对于一个成功匹配的正则匹配结果， 可以将表达式所匹配到的内容提取出来。

.. code:: python

    >>> import re
    >>> string = "zombie110year@outlook.com"
    >>> regp = re.compile(r"(\S+)@outlook.com")
    >>> match = regp.match(string)
    >>> match.group(0)
    zombie110year@outlook.com
    >>> match.group(1)
    zombie110year

所有的捕获组都有对应的索引值。 完整的正则表达式具有索引值 0，
内部的子捕获组索引则按照 1，2，3，4… 这样的顺序依次递增。
如果存在内嵌的子表达式， 则索引值对应的顺序为:

1.  从外向内
2.  如果属于同一层， 则从左到右

非捕获组
========

非捕获组使用 ``(?:)``， 用于表示那些需要在正则表达式中匹配，
但是不计入捕获组计数中的子表达式:

.. code:: python

    >>> import re
    >>> string = "zombie110year@outlook.com"
    >>> regp = re.compile(r"(\S+)(?:@)([\w\.]+)")
    >>> match = regp.match(string)
    >>> match.group(0)
    zombie110year@outlook.com
    >>> match.group(1)
    zombie110year
    >>> match.group(2)
    outlook.com

命名捕获组
==========

可以为捕获组取一个名字， 以便通过其名称以字符串作为索引取出该捕获组内容。
命名捕获组采用 ``(?<name>pattern)`` 的语法。 ``pattern`` 是要匹配的模式，
``name`` 是这个捕获组的命名。

.. code:: python

    >>> import re
    >>> regp = re.compile(r"(?P<username>\S+)@(?P<domain>[\w\.]+)")
    # Python 中的命名捕获组使用  (?P<name>pattern) 语法
    >>> regp.match("zombie110year@outlook.com")
    <re.Match object; span=(0, 25), match='zombie110year@outlook.com'>
    >>> _.group('username'), _.group('domain')
    ('zombie110year', 'outlook.com')
    >>> regp.match("zombie110year@gmail.com")
    <re.Match object; span=(0, 23), match='zombie110year@gmail.com'>
    >>> _.group('username'), _.group('domain')
    ('zombie110year', 'gmail.com')

条件或
======

条件或使用 ``|`` 管道符。 它表示 『在当前表达式层级匹配竖线左侧或右侧的结构』。

条件或可用在最外层表达式中: ``"cat|dog"`` 既可以匹配 ``"cat"``，
又可以匹配 ``"dog"``。

也可以用在子表达式中: ``"gr(e|a)y"`` 可以匹配 ``"grey"`` 或 ``"gray"``。

如果多个条件或连用， 则表示在当前表达式层级下，
竖线所分割的不同区块的或关系: ``"tom|jerry|spike"`` 可以匹配 ``"tom"``
或 ``"jerry"`` 或 ``"spike"``。

捕获组的引用
============

捕获组可以通过继续的程序调用， 以编号或命名方式引用（提取）。
也可以在正则表达式内部进行引用（反向引用）。

正向引用
--------

就是通过程序调用进行引用，使用方法与编程语言的实现强相关，在对应编程语言的话题下再阐述。建议网上搜索各编程语言正则表达式模块的文件。

反向引用
--------

在同一个正则表达式中引用匹配的部分。

通过索引值引用
    使用 `\n` 或 `$n` 的语法，例如 `\1`, `\2`, `$1`, `$2`。与正则引擎的实现相关。
    特别的是，子表达式从 1 开始编号，而 0 表示整个正则表达式。
    如果在反向引用中使用了 0，大多数正则引擎会报错，拒绝执行，因为它会引发无限递归。
通过名字引用
    可以引用设置了名字的命名捕获组，使用 `\k<name>` 或 `${name}` 等语法，不同正则引擎使用的语法不一定相同。

    反向引用用于表达连续出现的相同字符串。 例如，
    从一个字符串中找到连续重复出现三次的相同结构:

    .. code:: python

        >>> import re
        >>> string = "akdfjaskdfak k kfjakdslfj"
        >>> pat = re.compile(r"(\w) \1 \1")
        >>> pat.search(string)
        <re.Match object; span=(11, 16), match='k k k'>

对于 Python，其 re 模块使用 ``\n`` 和 ``(?P=name)`` 的语法。

####
断言
####

断言用于在整个字符串中限定正则表达式的匹配部分。
在匹配过程中，断言不会被计入正则构造中，不会引起读写指针的变化。
通常用于表示在某某字符串一侧的正则表达式。

断言又被称作「零宽断言」， 就是表达了 **断言不计算在匹配结果之内，
而且不会引起读写指针的变化** 这个含义。

一般都用在正则表达式的首尾两端。

预定义断言
==========

`^`
    字符串（或行）的首部
`$`
    字符串（或行）的尾部
`\b`（或 `\<`, `\>` 在 GNU Regex 中）
    单词的首尾。`\b` 更通用一些。
`\B`
    单词的内部

自定义断言
==========

正前瞻断言〔`(?={{ 模式 }})`〕
    在正则表达式的末尾使用，限定正则表达式在 **模式** 之前。
正后顾断言〔`(?<={{ 模式 }})`〕
    在正则表达式的开头使用，限定正则表达是在 **模式** 之后。
负前瞻断言〔`(?!{{ 模式 }})`〕
    类似「正前瞻断言」，但此断言内的模式表示『非』含义，限定正则不在此模式之前。
负后顾断言〔`(?<!{{ 模式 }})`〕
    类似「正后顾断言」，但此断言内的模式表示『非』含义，限定正则不在此模式之后。

##############################
各种编程语言中的正则表达式实现
##############################

Python
    可用标准库中的 re 或第三方实现的功能更强的 regex 库。
JavaScript
    由 JS 引擎内置，并且提供了 `/{{ 模式 }}/{{ 选项 }}` 样式的字面量表示法，但在这种字面量表示中需要将 `/` 符号转义，否则将会被识别为正则字面量的边缘，因此在处理路径、URL时非常麻烦。在 ES5 之后，可以调用标准对象 `RegExp` 的构造函数来创建正则表达式，通过传入一个满足正则语法的字符串来构造。
Rust
    已从标准库分离，现维护在 crate `regex` 中。
Java
    `java.util.regex` 模块。
Go
    `regexp` 模块。
C
    GNU C 提供了 regex.h 头文件，且相关函数定义在 glibc 中，不需要额外链接。
    由于 C 这种底层语言处理字符串非常麻烦，未过多研究。
C++
    在 C++ 11 后，STL 提供了 regex 模块，`#include <regex>` 即可引入其符号。
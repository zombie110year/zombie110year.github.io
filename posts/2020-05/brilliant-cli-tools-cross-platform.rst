---
title: '优秀的跨平台命令行工具'
slug: 'brilliant-cli-tools-cross-platform'
date: 2020-05-14 17:17:43 UTC+08:00
tags:
-   cli
-   unix
-   windows
category: life
description: 在 Unix，Windows NT 系统上通用的命令行程序。
type: text
---

.. contents::
    :depth: 2

.. TEASER_END

#######
NuShell
#######

NuShell [#site-nushell]_ 是使用 Rust 语言编写的跨 Unix, Windows, macOS 系统的现代 Shell 程序，目前在 GitHub 上有 7k 星。
NuShell 的首个 Commit 在 2019 年提交，且截至 2020 年 5 月 14 日仍在活跃更新，目前的最新版本为 0.14.0 。

在 Windows 上，可以使用 scoop 方便地安装 NuShell：

.. code:: powershell

    scoop install nu

可以在内部调用 ``help`` 命令查询内置的帮助文档。

NuShell 的特色在于结构化数据以及类似 SQL 的二维表操作，
在处理大量结构化数据时具有一定优势，几乎相当于一个针对本地文件、数据的 SQL 解析器。

不过其缺少流程控制语句的特点，让它难以胜任逻辑化的系统管理工作。

NuShell 哲学
============

.. abbr:: OS

    Operation System

NuShell 不像传统的 Unix Shell，它从 PowerShell 汲取灵感，将每个命令产生的结果视作具有结构的对象，而不是传统的原始字节。但和 PowerShell 相比，它的速度要快得多。

数据类型
========

NuShell 具有以下几种数据类型：

简单数据
--------

整数（Integers）
    字面量满足正则表达式 `\d+` 形式。
实数（Decimals）
    字面量满足 `\d+.\d+` 形式。
字符串（Strings）
    在 NuShell 中，字符串都是 UTF8 编码的。
行（Lines）
    行是由 :abbr:`OS` 默认换行符结尾的字符串。
列路径（Column Paths）
    用来表达从一个表到子表、列、行直到单元格的路径::

        sys | get host.sessions

    上面例子中的 ``host.sessions`` 就是一个列路径的实例。
模式（Patterns）
    通常也叫做通配符模式。可以使用 ``*`` 和 ``?`` 通配符。
布尔数（Booleans）
    ``$true`` 与 ``$false``。
时刻（Dates）
    默认使用 UTC 时区。
时间（Durations）
    用来表示一段持续的时间，例如 ``1s`` 代表一秒。字面量为 数字+后缀单位 的形式。单位有：

    .. list-table::
        :header-rows: 1

        *   -   单位
            -   含义
        *   -   s
            -   秒
        *   -   m
            -   分
        *   -   h
            -   时
        *   -   d
            -   日
        *   -   w
            -   周
        *   -   M
            -   月
        *   -   y
            -   年
范围（Ranges）
    类似于 Rust 中的范围，但是个闭区间，且从 0 开始::

        ls | range 0..1
        # 取流的前 2 项
路径（Paths）
    这里的路径指文件系统路径，表示法和 OS 有关::

        C:\Program Files
        /usr/bin
文件尺寸（Bytes）
    特指文件有多大，后缀的单位可以是 b, kb, mb, gb 等。
二进制数据（Binary Data）
    现在这个类型才表示二进制的数据，如一段原始字节。

结构化数据
----------

二维表（Rows）
    一组拥有多个字段的数据组成的二维表。
列表（Lists）
    一列数据，不在乎其字段是否相同，如果有不同的字段，会影响它们的打印样式。
    如果要从字面量来构造列表，可以使用 ``[]`` 做界定符，空格 `` `` 做分隔符::

        echo [α β θ]
块（Blocks）
    用来表示一段 NuShell 的代码块。

加载数据
========

NuShell 使用 ``open`` 命令来从文件系统加载数据。特别的是， open 会自动识别一些存储数据的文件格式的后缀名，然后以结构化数据的方式加载它们，例如::

    open data.json
    open data.yaml
    open data.toml
    open data.xml
    open data.csv
    open data.ini

等。

对于太长的文本文件，如果没有使用管道传输数据而是直接打印到终端的话，则会自动打开一个分页器，可以通过 ESC 退出。
不过对于存在中文的文本文件，其换行时会出现一些偏差：每一个全角字符都会导致下一行多显示一个前缀的空格 [#issue-nushell-1784]_ 。

open 也可以附加参数 ``--raw`` 来以原始模式读取一个文件。

fetch 命令则可以读取网络数据::

    fetch https://cn.bing.com/search?q=nushell

管道
====

与 NuShell 的管道相互配合的命令可以有以下三种类别：

*   处理一个流（例如 ls）
*   过滤一个流（例如 where）
*   消费管道的输出（例如 autoview）

在每个命令的结束，除非显式调用其他消费命令，否则 autoview 都将被自动调用。

在一个流中传递的数据是结构化的，每个对象都有不同的字段，在使用 where 过滤时，可以通过布尔表达式进行运算::

    ls | where type == 'Dir'
    # 筛选出当前目录下的所有子目录

常用的对管道进行处理的命令有：

where
    通过一个布尔表达式对管道内容进行筛选。
sort-by
    以某个字段为依据进行排序。
get
    获取管道内容的某个字段，如果该字段有嵌套的子字段，那么可以用 ``.`` 进行访问::

        sys | get host.name
save
    将管道内容保存到文件。

内置命令与外部程序冲突
======================

因为 NuShell 拥有众多内置命令，如果有与外部命令命名冲突的，可以在命令前添加脱字符 ``^`` 来调用外部程序::

    ^echo Hello World

环境变量
========

NuShell 创建的环境变量都会保存在 ``$nu.env`` 对象的对应命令字段下。

对于单个临时变量，可以使用 Bash 语法::

    FOO=bar echo $nu.env.FOO

也可以使用 with-env 命令::

    with-env [FOO bar] { echo $nu.env.FOO }

二维表操作
==========

见官方文档 https://www.nushell.sh/book/en/working_with_tables.html

########
starship
########

StarShip [#site-starship]_ 是一个命令提示符增强工具，其着眼于

兼容
    支持 Unix、Windows、macOS 上的 Bash、Fish、Zsh、PowerShell 以及 Ion 等 OS 和 Shell 程序。
速度
    使用 Rust 编写，确保速度与内存安全。
扩展
    拥有极强的可扩展性。

由于 StarShip 使用 Powerline 字体进行美化，请在安装前确保设备上已经安装 Powerline 字体 [#site-powerline-font]_ 并在终端程序中启用。

在 Windows 上，通过 scoop 安装：

    scoop install starship

在 PowerShell 的配置文件中写入：

.. code:: powershell

    Invoke-Expression (&starship init powershell)

个人配置
========

详细的配置手册可以阅读其文档，有中文版本 [#doc-starship]_ 。
个人的 starship 配置文件位于 ``~/.config/starship.toml``。

.. code:: toml

    prompt_order = [
        "python",
        "rust",
        "username",
        "hostname",
        "directory",
        "git_branch",
        "git_commit",
        "git_state",
        "git_status",
        "jobs",
        "time",
        "cmd_duration",
        "line_break",
        "character"
    ]

    [character]
    use_symbol_for_status = true

    [directory]
    prefix = ":"

    [git_branch]
    symbol = "|"

    [time]
    disabled = false


########
参考链接
########

.. [#site-nushell] https://github.com/nushell/nushell
.. [#issue-nushell-1784] https://github.com/nushell/nushell/issues/1784
.. [#site-starship] https://starship.rs/zh-CN/
.. [#site-powerline-font] https://github.com/powerline/fonts
.. [#doc-starship] https://starship.rs/zh-CN/config/
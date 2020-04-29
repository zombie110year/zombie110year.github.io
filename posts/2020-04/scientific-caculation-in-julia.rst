---
title: '用 Julia 搞科学计算'
slug: 'scientific-caculation-in-julia'
date: 2020-04-28 22:12:37 UTC+08:00
tags:
- julia
- 科学计算
- 数值计算
category: 科学计算
description:
type: text
status: draft
---

.. default-role:: code

前几年就听说过 Julia 了，这下来试试它的功能。
由于 Windows 上各种编程语言的配置都很麻烦，这次就在 :abbr:`WSL` 中搞。

.. contents::

.. TEASER_END

安装 Julia 不必多说，对 julia 语言的一些配置通常在 julia 的 :abbr:`REPL`
（交互式解释器）中进行。

##################
配置国内软件包镜像
##################

根据 [#fn-jl-mirror]_ 的讨论得知，目前 Julia 1.4 没有国内镜像，而且尝试 ping 给出的两个国外镜像的地址，都 timeout 了。
而访问 HTTPS 链接时，延迟又高，速度又慢，所以还是先使用默认仓库吧。

根据一些消息，包仓库中存储的其实是目录，实际的数据通常是从代码仓库下载源码而来。
通常这些代码都托管在 GitHub 上，所以想办法提高 HTTPS on GitHub 的链接速度即可::

    (@v1.4) pkg> add IJulia
        Cloning default registries into `~/.julia`
        Cloning registry from "https://github.com/JuliaRegistries/General.git"

例如，配置一个 GitHub 的 HTTPS 代理（在 ~/.gitconfig） 中::

    [proxy]
        https = http://localhost:8080
        http = http://localhost:8080

记得自己配置绑定的端口和链接协议。

################
配置 Jupyter Lab
################

Jupyter Lab [#fn-site-jupyter]_ 是一个非常方便的交互式文学编程工具，
可以在 Code 胞中写代码并交互式运行，也可以在 Markdown 胞中写文档，
还可以在 Raw 胞中粘贴原始文本（一般用来记录程序的输出）。

可以输入 `]` （无需输入换行）就可进入包管理模式。
虽然 Julia 自己拥有下载安装 Conda + Jupyter 的能力，
不过由于默认源位于国外，下载速度和稳定性都不怎么样，因此建议配置 Conda 镜像源之后，主动下载 JupyterLab，然后在 Julia 中配置已有的 Jupyter。

1. 到清华大学镜像站下载 Miniconda3 安装包
2. 安装 Miniconda 后配置 conda 源为国内镜像

一些教程可能会教你先在 Jupyter 的 REPL 模式下，配置环境变量 `JUPYTER`，设定为 jupyter 可执行文件的路径，如::

    ENV["JUPYTER"] = "~/miniconda3/envs/jupyter/bin/jupyter"

之后再安装 IJulia。

但这个版本过时了，现在的 IJulia 安装在默认目录即可，它会被 Jupyter 自动发现。[#fn-pre-conda-ijulia]_

########
语法入门
########

网络上学习 Julia 通常都是阅读官方文档
https://docs.julialang.org/en/v1/manual/documentation/index.html ，
其中的 Manual 章节提供了入门指南。

其他好用的中文资源还有：

《Julia 编程指南》
    https://github.com/Roger-luo/Brochure.jl

运行 Julia 程序，可以在 REPL 中逐行输入，也可以保存在脚本文件中（约定以 `.jl` 为后缀名），然后通过命令行调用::

    julia script.jl args...

在安装好 Julia 之后，执行这句代码发出第一声 Hello World 吧！

.. code:: julia

    println("Hello World")

基本语法要素
============

Julia 使用 `#` 作为注释开始的符号。

.. contents::
    :local:

变量和类型
----------

变量标识符
    几乎是任意 Unicode 符号，只要不与内置符号冲突即可。
    特别地， Julia 可以输入一些希腊、罗马字符，可以通过类似于 LaTeX 的语法进行输入。
    在 REPL 中，按下 TAB 键即可转化::

        julia> \varepsilon<TAB>
        julia> ε
        julia> ε = 1e-6

变量初始化
    变量初始化其实就是对一个新的变量赋值，其类型可以通过字面量或其他变量自动推导。

获取类型
    通过 `typeof` 函数获取一个变量的类型信息：

    .. code:: julia

        In[1]:  typeof(A)
        Out[1]: Array{Int64,2}

变量类型标注
    通过 `var::Type` 来进行标注，使用 `::` 符号。
    但是不支持对全局变量进行类型标注，这个通常在函数的形参表中使用。

类型的相关信息
    对一些数值类型，Julia 提供了 `typemax` `typemin` 和 `eps` 函数，用来取得类型的最小值、最大值和 0 附近的间隔值（eps 只能应用在浮点数上）。

向量和矩阵
    Julia 内置了向量和矩阵类型，并且可以通过统一的字面量形式表达。
    使用 `[]` 作为界定符，使用空格 ` ` 或分号 `;` 做分隔符，前者分隔列，后者分隔行。例如：

    .. code:: julia

        # x. 是 x.0 的简写，表示这是浮点数
        A = [1. 2.; 3. 4.]
        b = [5; 6]

    那么，A 是一个 2x2 的矩阵::

        2×2 Array{Float64,2}:
         1.0  2.0
         3.0  4.0

    b 是一个 2 维列向量::

        2-element Array{Float64,1}:
         5.0
         6.0

常用运算符
----------

四则运算
    `+-*/%` 等与其他编程语言一样，不再赘述。
    值得注意的是，如果是 n * x 形式的乘法，其 `*` 可以省略::

        x = 3
        2x == 2 * x
赋值运算符
    四则运算符和 `=` 符组合::

        x += 1

运算符基本上和其他编程语言一样，不再赘述。

特别地是，Julia 内置了向量、矩阵运算支持，默认的四则运算符遵守线性代数计算法则。
如果要把向量和矩阵当作普通的数组处理，需要对运算符前加一 `.`，代表广播运算（对数组中的每一元素进行对应处理）。

例如，定义了 A，B，C 三个向量：

.. code:: julia

    A = [1 2 3]
    B = [4 5 6]
    C = [4; 5; 6]

如果你学过的线性代数知识还没忘的话，应该还记得必须是两个列向量和行向量相乘::

    A * C == [32]
    C * A == [4 8 12; 5 10 15; 6 12 18]
    # A * B 报错

如果加上点，那么就变成了数组相乘，相当于每一个元素对应相乘，而不是矩阵乘法规则::

    A .* B

从向量来看不明显，这里弄两个矩阵：

.. code:: julia

    D = [1 2 3; 4 5 6; 7 8 9]
    E = [1 4 7; 2 5 8; 3 6 9]

    D * E == [14 32 50; 32 77 122; 50 122 194]
    D .* E == [1 8 21; 8 25 48; 21 48 81]

控制语句
--------

for-in
    .. code:: julia

        result = 0
        for i in 1:100
            @show i
            result += i
        end
        result == 5050

while
    .. code:: julia

        result = 1
        while result < 10000
            result *= 2
        end
        result == 16384

if-elseif-else
    .. code:: julia

        x = 0
        if x < 0
            @show -x
        elseif x == 0
            @show 0
        else
            @show x
        end

表达式和语句块
--------------

Julia 以 begin .. end 来表示一个语句块，其作用类似于 Rust 的 `{}`， Lisp 的 `()`，
这种基于表达式的表示风格，对于方便编写程序还是很有利的。
比如在 Julia 中写一个匿名函数::

    fnx = x -> begin

函数
----

命名约定
    如果会修改传入的参数，那么函数名以 `!` 结尾。

函数定义的传统语法形式::

    function {{ name }} ({{ parameters }})
        {{ function body }}
    end

需要以 end 来表示语句块的结尾。

另外， Julia 还提供了类似于数学表达式的表示方式：

.. code:: julia

    f(x) = x * x

这和数学上写：

.. math:: f(x) = x \times x

形式上是很相近的。

######
结构体
######

.. code:: julia

    struct {{ Name }}
        {{ member name }}::{{ member Type }}
    end

####################
站在前人的肩膀：模块
####################

########
参考链接
########

.. [#fn-site-jupyter] https://jupyter.org
.. [#fn-jl-mirror] https://discourse.juliacn.com/t/topic/2969
.. [#fn-pre-conda-ijulia] https://github.com/JuliaLang/IJulia.jl/issues/802
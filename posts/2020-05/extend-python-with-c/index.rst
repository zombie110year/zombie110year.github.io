---
title: '用 C 语言扩展 Python'
slug: 'extend-python-with-c'
date: 2020-05-30 15:00:48 UTC+08:00
tags:
-   python
-   c
category: tutorial
type: text
---

Python 官方给出教程如下 [#doc-ext]_，本文总结几个要点，并介绍与 Python Poetry [#site-poetry]_ 工具相结合的方法。

.. contents::

.. TEASER_END

######################
文件安排与开发前的准备
######################

对于一个包含 C 扩展的 Python 模块，我们期望它如同一个标准的纯 Python 包那样使用，
可以将文件系统如下布置，``/`` 表示当前工作目录，假设我们的包叫做 spam::

    /
        pyproject.toml          poetry 创建的项目元数据文件
        build.py                构建脚本
        spam                    包
            __init__.py         封装 Python 接口
            spam_.c             一般在扩展模块名后加 _，而通过同名 Python 模块向外导出接口
            <spam_.pyd>         编译后，期望二进制模块位于此处

如果使用 Linux 系统，那么在安装 Python 时，其必要的库文件与头文件已经在编译器的检索路径中了；
如果使用 Windows 系统，那么在开发时，还需要设置开发工具的头文件检索路径，将 Python.h 所在的路径添加到其中，
例如 Vscode 的 C++ 设置：

.. code:: json

    "${env:USERPROFILE}/scoop/apps/python/3.8.2/include/**"

这里笔者在 Windows 上使用了 *scoop* [#site-scoop]_ 来安装 Python，因此安装路径如上。
不过不需要另外配置，这里只是让语言服务器能够找到符号而已，在编译时，通过 Python 提供的 disutils 模块，
它可以自己找到自己。

注意，由于 MSVC 和 GCC ABI 不同，在 Windows 上编译 Python C 扩展需要 Visual Studio C++ 开发负载安装。
（因为 Windows 上的 Python 发行版是 MSVC 编译的）
记得勾选 Windows 10 SDK，尽管它体积庞大，令人生厌，但它是在 Windows 10 上编译 Python C 扩展的必要组件。

##############
自顶向下的教程
##############

Python 官方教程选择了从细节到整体的讲解路线，本文则先说明如何创建一个模块，然后添加另外的成分。

注意，由于 Python.h 通过宏来对跨平台代码进行一些设置，因此这个头文件应当第一个被包含。并且在它之前用 ``#define PY_SSIZE_T_CLEAN`` 设置 Python 相关方法使用 ``Py_ssize_t`` 来代替 int 作为尺寸类型。

.. code:: c

    #define PY_SSIZE_T_CLEAN
    #include <Python.h>

初始化模块
==========

.. default-role:: code

一个 Python 模块是一个 **模块定义结构体** ，这个结构体有一个重要成员名为 **模块方法表** ，
所有模块中提供的方法都必须在模块方法表中导出。
而模块定义结构体也必须被模块初始化函数导出。

模块方法表是一个数组，定义了该模块所导出的方法（函数），其元素为一个结构体，具有四个字段，按顺序分别为：

方法名（const char*）
    该方法在 Python 中使用的命名；
函数指针
    该方法在 C 中的实例；
传参机制
    传入在 Python.h 中预定义的 bitflag，可选值有：

    `METH_VARARGS`
        表示接受一个 tuple 为参数
    `METH_VARARGS | METH_KEYWORDS`
        表示既接受元组，也接受关键字参数，这种情况下，一个导出给 Python 使用的函数需要接受第三个 PyObject* 作为参数，
        传入一个字典。
文档字符串（const char*）
    该方法的文档字符串。
    一般留 NULL，而在对应的 pyi 文件中编写文档字符串，因为这种东西一般由开发工具使用，运行时不会管它。
    除非该模块需要利用 docstring 实现特殊功能。

例如：

.. code:: c

    /// 将所有传入参数加到一起
    PyObject *add(PyObject *self, PyObject *args);

    /// 模块方法表
    static PyMethodDef SPAM_METHODS[] = {
        {"add", add, METH_VARARGS, NULL},
    };

模块定义结构和模块方法表中的元素其实是同一种类型，只不过多一个初始化字段：

.. code:: c

    static PyModuleDef SPAM_MOD = {
        /// 模块初始化基对象
        PyModuleDef_HEAD_INIT,
        /// 模块在 Python 中的命名
        "spam_",
        /// 模块文档，一般留 NULL，而在 pyi 中编写
        NULL,
        /// 每个解释器使用该模块的状态尺寸，留 -1 让模块将状态保存在全局变量中
        -1,
        /// 模块方法表
        SPAM_METHODS};

将模块定义结构由初始化函数处理，创建一个 Python 的模块对象：

.. code:: c

    /// 模块初始化函数
    PyMODINIT_FUNC PyInit_spam_(void) { return PyModule_Create(&SPAM_MOD); }

模块初始化函数的返回值为 `PyMODINIT_FUNC` ，不接受参数，并且，命名必须为::

    PyInit_<模块名>

.. warning::

    注意，模块名与以下三个名称相关，需要确保它们相同：

    -   在 Python 中 import 的名称（对应模块方法表第二个字段）
    -   编译产物（动态库）的名称（对应模块方法表第二个字段，编译后不应当修改）
    -   模块初始化函数的名称（`PyInit_<模块名>` 模式）

    如果改变了动态库的名称，那么在加载模块时，会寻找另一个名为 `PyInit_*` 的初始化函数，例如原本名为 `spam_.*.pyd` ，
    之后重命名为 `abc.*.pyd` 后，导入模块时将会寻找 `PyInit_abc` 初始化函数。

现在，补一个 add 函数的定义在下面（功能未实现），先定义为返回 `int(0)` 以便通过编译，看看效果。

.. code:: c

    // spam_.c
    #define PY_SSIZE_T_CLEAN
    #include <Python.h>

    /// 将所有传入参数加到一起
    PyObject *add(PyObject *self, PyObject *args);

    /// 模块方法表
    static PyMethodDef SPAM_METHODS[] = {
        /// add 方法
        {"add", add, METH_VARARGS, NULL},
        /// 哨兵，必须以它收尾，作用和字符串中的 \0 类似
        {NULL, NULL, NULL, NULL}
    };

    /// 模块定义结构
    static PyModuleDef SPAM_MOD = {
        /// 模块初始化基对象
        PyModuleDef_HEAD_INIT,
        /// 模块在 Python 中的命名
        "spam_",
        /// 模块文档，一般留 NULL，而在 pyi 中编写
        NULL,
        /// 每个解释器使用该模块的状态尺寸，留 -1 让模块将状态保存在全局变量中
        -1,
        /// 模块方法表
        SPAM_METHODS};

    /// 模块初始化函数
    PyMODINIT_FUNC PyInit_spam_(void) { return PyModule_Create(&SPAM_MOD); }

    PyObject *add(PyObject *self, PyObject *args) {
        return PyLong_FromLong(0);
    }

在 `spam/__init__.py` 中，通过 `from .spam_ import *` 来导出内容。

试运行
======

.. code:: python

    from spam import add
    assert add() == 0

解析位置参数
============

Python C API 通过 `PyArg_ParseTuple` 来解析一个元组对象，它接受一个 PyObject* 为第一个参数，
然后是格式化字符串，再之后是一组可写的变量地址，例如：

.. code:: c

    PyObject *add(PyObject *self, PyObject *args) {
        long a = 0;
        long b = 0;
        PyArg_ParseTuple(args, "ll", &a, &b);
        long sum = a + b;
        return PyLong_FromLong(sum);
    }

这里，Python 与 C 方法参数传递的对应关系为::

    # Python
    def add(a, b) -> int:

    // C
    PyObject *add(PyObject *self, PyObject *args);

所有位置形参都以 tuple 的形式传递给 args。

这里，列出一些常用的格式字符串 [#doc-fmtstr]_ ：

.. csv-table::
    :header-rows: 1

    格式字符串,Python 类型,C 类型
    `s#`,str,const char* + Py_ssize_t
    `y#`,bytes,const char* + Py_ssize_t
    `b`,int,unsigned char
    `i`,int,int
    `I`,int,unsigned int
    `l`,int,long int
    `k`,int,unsigned long int
    `L`,int,long long int
    `K`,int,unsigned long long int
    `f`,float,float
    `d`,float,double
    `D`,complex,Py_complex
    `O`,object,PyObject*
    `p`,bool,int
    `(items)`,tuple,...

另外，有一些特殊字符：

`|`
    剩下的参数是可选参数，在 C 中，这些参数需要初始化一个默认值。
`$`
    剩下的参数是只能通过命名参数传递的参数。与 `|` 类似。

解析 tuple 对象，需要在 `()` 内填写另外的类型格式字符串::

    # python
    test( (1, "a") )

    // c
    PyArg_ParseTuple(args, "(is)", &num, &str);

通过 Iterator Protocol 解析不定参数
===================================

在 Python 中，等同于：

.. code:: python

    def func(*args):

在 C 中的等效写法为：

.. code:: c

    PyObject *isum(PyObject *self, PyObject *args) {
        long sum = 0;
        PyObject *iter = PyObject_GetIter(args);
        PyObject *item = NULL;
        while ((item = PyIter_Next(iter))) {
            long x = PyLong_AsLong(item);
            sum += x;
            /// 释放 item
            Py_DECREF(item);
        }
        Py_DECREF(iter);
        return PyLong_FromLong(sum);
    }

解析关键字参数
==============

.. code:: c

    /// 在模块方法表中
    {"named_join", named_join, METH_VARARGS | METH_KEYWORDS, NULL},

    /**
    * def named_join(a=0, b=1, c=2) -> str:
    */
    PyObject *named_join(PyObject *self, PyObject *args, PyObject *kwargs) {
        static char *kw[] = {"a", "b", "c", NULL};
        unsigned int a = 0;
        unsigned int b = 1;
        unsigned int c = 2;
        PyArg_ParseTupleAndKeywords(args, kwargs, "|$III", kw, &a, &b, &c);
        char *const buffer = (char *const)calloc(a + b + c, sizeof(char));
        memset(buffer, 'a', a);
        memset(buffer + a, 'b', b);
        memset(buffer + a + b, 'c', c);
        /// 构造时复制
        const PyObject *join = Py_BuildValue("s#", buffer, a + b + c);
        free(buffer);
        return (PyObject *)join;
    }

##########################
Python 与 C 对象的互相转化
##########################

Python 提供了一系列命名规律为 `Py<Python Type>_From<C Type>` 的函数，以便由 C 类型构造 Python 对象。
当然，也有对应的 `*As*` 函数，将 Python 对象转换成 C 类型。

也可以通过 `Py_BuildValue` + 格式字符串来由 C 类型转换 Python 对象。

为了 FFI 接口的简洁性，推荐只传递基本类型。

#################################
将扩展编译过程集成到 poetry build
#################################

根据 StackOverflow 上的这个讨论 [#so-poetry-c-ext]_。
需要编写一个 build.py 脚本，在其中定义名为 build 的函数，在其中修改 setup 函数的参数即可：

.. code:: python

    from setuptools import Extension
    def build(setup_kwargs: dict):
        setup_kwargs.update(
            {
                "ext_modules": [
                    Extension("spam.spam_", sources=["spam/spam_.c"])
                ]
            }
        )

为了保持目录结构， Extension 的模块名可以按照 Python 模块导入语法进行命名。
如上， `spam.spam_` 模块将在 `spam/__init__.py` 文件中以 `from .spam_ import *` 的形式将方法暴露出来。

然后，修改 pyproject.toml 中的 bulid 字段：

.. code:: toml

    [tool.poetry]
    # ... 其他配置
    build = "build.py"

############
添加类型定义
############

Python 的开发工具，例如 pyls，mypy 等，可以将与模块同级的同名 `.pyi` 结尾的文件作为类型声明文件，
可以在其中编写类型定义、文档字符串等。

.. code:: python

    # spam/__init__.pyi
    def add(a: int, b: int) -> int:
        """a + b

        >>> add(3, 5)
        8
        """
        pass
    def isum(*args: int) -> int:
        """传入整数类型的不定参数，将它们加在一起返回

        >>> isum(1, 2, 3)
        6
        """
        pass
    def named_join(a: int = 0, b: int = 1, c: int = 2) -> str:
        """将 abc 三个字母按传入的数字重复对应次数，组成字符串返回

        >>> named_join(a=1, b=2, c=3)
        "abbccc"
        """
        pass

########
参考链接
########

.. [#doc-ext] https://docs.python.org/zh-cn/3/extending/index.html
.. [#site-poetry] https://python-poetry.org/
.. [#site-scoop] https://scoop.sh
.. [#so-poetry-c-ext] https://stackoverflow.com/questions/60073711/how-to-build-c-extensions-via-poetry
.. [#doc-fmtstr] https://docs.python.org/zh-cn/3/c-api/arg.html
---
title: 'HTML + CSS + JavaScript 技巧收集'
slug: html+css+javascript-skill-collection
date: 2020-05-08 16:14:58 UTC+08:00
tags:
- html
- css
- javascript
category: collection
type: text
---

.. contents::

.. TEASER_END

##############
让表格相间着色
##############

例如，奇数行背景色设为淡灰色，偶数行则为纯白色。

可以利用 nth-child 选择器，可以接受一个名为 ``n`` 的变量用于表示
在当前元素的父元素下的兄弟元素中当前子元素的序号，这个序号从 1 开始，
而 ``n`` 的值则从 0 开始。[#nth-child]_

.. code:: css

    /* 从 2 开始，为了略过表头 */
    table#table1 tr:nth-child(2n+2) {
        background: white;
    }
    table#table1 tr:nth-child(2n+3) {
        background: lightgrey;
    }


.. raw:: html

    <style>
    table#table1 tr:nth-child(2n+2) {
        background: white;
    }
    table#table1 tr:nth-child(2n+3) {
        background: lightgrey;
    }
    </style>

.. table::
    :name: table1

    ======= ======= ======= =======
    Example ColumnA ColumnB ColumnC
    ------- ------- ------- -------
    a       a1      a2      a3
    b       b1      b2      b3
    c       c1      c2      c3
    d       d1      d2      d3
    e       e1      e2      e3
    ======= ======= ======= =======

----

你可能会在一些资料里看到 CSS expression 表达式，但那个是 IE8 之前才提供的功能，
不在现代 CSS 标准里。

########
参考链接
########

.. [#nth-child] https://developer.mozilla.org/zh-CN/docs/Web/CSS/:nth-child
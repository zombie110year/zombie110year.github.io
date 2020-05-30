---
title: '使用 Python 对静态站点进行整站重建'
slug: 'static-site-full-reconstraction-by-python'
date: 2020-05-18 15:54:14 UTC+08:00
tags:
-   python
-   spider
category: tutorial
description: 将一个静态站点完整地扒拉下来。
type: text
status: draft
---

玩玩爬虫。

.. contents::

.. TEASER_END

##################
一个全站爬虫的要素
##################

一个静态站点的所有资源都处于 HTML + CSS + JavaScript + Media Resource 的范畴之内，在爬取时忽略所有动态因素，如 AJAX、HTML 表单等。

在爬取的过程中，可能会遇到以下困难：

重复爬取
    当多个页面拥有相同的资源引用时，为了避免重复爬取，可以通过记录每一份成功下载资源的绝对链接，在开始下载前检测此资源是否已经被爬取来达成。
    这个功能可以通过 Python 标准库的 ``urllib.parse`` 模块来实现。
循环跳转
    若存在一个「页面环」：A->B->C->A... 等等，将形成循环跳转的情况，如果爬虫一头栽进去，就可能进入死循环。
    如果网站没有通过符号链接来刻意制作陷阱的话，这个问题也可以通过绝对链接来解决；否则，需要为爬虫加上一个最大路径深度的设置。

为了搞整站重建，我们需要爬取这些目标：

从起点出发，所有可以通过超链接访问到的资源
    在这个步骤中，需要在爬取并下载文件的同时，在本地文件系统建立与远程同步的文件结构。打个比方，如果有个 URL 为 ``https://example.com/a/b/c/hello.html`` 的文件，那么在本地文件系统，从工作目录开始，将它保存为 ``./example.com/a/b/c/hello.html``。
爬取所有存储在外站的资源
    有些静态站点将媒体文件、CSS 或 JS 资源存储在 CDN 中，为了完成重建，需要把它们也爬取过来。并同样构造等价的文件结构。
    为了让这些资源能够被一个 HTTP 服务包全，打算建立在该站点对应的存储目录下的 ``.ssc-external`` 文件夹里（ssc 是 static site copy 的缩写）。
解析已爬取的 HTML 文件，将外站资源重定向至本地
    解析出 HTML 中的外站链接，将它们一律解析成::

        /.ssc-external/{scheme}-{domain}/{path}

##############
开发环境的准备
##############

打算直接上 aiohttp 模块、使用 lxml 解析 HTML。

lxml 库的基本用法
=================

.. code:: python

    from lxml.etree import HTML, HTMLParser

    et = HTML("<span>Hello</span", base_url=url)

- 一般通过 xpath 来选择元素
- base_url 用来解析内部的相对链接。

partially initialized module
============================

在运行时，由于划分了几个文件，而且为了提供类型标注而产生了循环导入，
为此，使用参考自 StackOverflow 的方法 [#so-1]_：

1. 在 ``if typing.TYPE_CHECKING`` 块下导入起类型标注作用的模块
2. ``from __future__ import annotations`` 以添加向前类型引用的支持（Python 3.7 以上可用，Python 3.9 正式支持）

.. [#so-1] https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports

########
程序设计
########

当我们完成 `一个全站爬虫的要素`_ 章节中所确定的任务时，需要这些角色：

发送网络请求（RequestSender）
    从 URL 池中读取一个链接，发送请求，获取响应。
响应解析任务分配（ResponseManager）
    从 RequestSender 获取一个响应，根据 MIMEType 决定下一步的策略。
解析 HTML （HTMLSolver）
    从 ResponseManager 获取一个 HTML 响应，解析出该网页引用的资源链接；
    然后放入 URL 池调度系统。而此 HTML 响应的完整内容，也放入文件调度系统进行保存作业。
保存静态资源（StaticFileSolver）
    从 ResponseManager 获取一个 非 HTML 响应。直接转交给文件调度系统。
文件调度系统（DiskManager）
    从各 Solver 获取响应，然后将其按照一定规则保存到本地文件系统。
URL 调度系统（URLManager）
    管理 URL 池。分 to_visit 和 visited 两个池，前者用一个队列，后者用一个集合。
    如果一个 URL 已经存在于 visited，那么就不会将其放入 to_visit。

以上各角色的关系如下图：

.. figure:: /images/static-site-full-reconstraction-by-python-uml.drawio.svg
    :height: 400px

    UML 图

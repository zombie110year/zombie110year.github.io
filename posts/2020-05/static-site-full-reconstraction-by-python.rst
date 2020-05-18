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

打算直接上 aiohttp 模块。
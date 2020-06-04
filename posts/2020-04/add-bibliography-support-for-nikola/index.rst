---
title: '为 Nikola 添加 Bibliography 支持'
slug: 'add-bibliography-support-for-nikola'
date: 2020-04-30 15:26:02 UTC+08:00
tags:
- python
- bibtex
- nikola
- restructuredtext
category: blog
description: |
    通过 bibtexparser 库为 Nikola 博客添加解析并显示 bibliography 引用的功能。
type: text
status: draft
---

.. default-role:: code

预期：添加 `bibliography` 指令和 `bibcite` 角色，前者引入一个 .bib 数据库，
后者则在段落中添加引用::

    .. bibliography:: path/to/example.bib

    这里引用了 :bibcite:`key`。

.. contents::

.. TEASER_END

#####################
Nikola 插件的加载方式
#####################

一个 Nikola 插件，是处于 `plugins` 目录下的一个子目录，
子目录名应当是插件的名字。

在子目录中，至少存在一个 `{{ name }}.plugin` 的文件和一个 Python 模块（一个脚本文件，或者包含 `__init__.py` 文件的包）。
在 .plugin 文件中，至少需要定义以下字段：

[Core] 表
    name 字段
        插件的名称
    module 字段
        插件所加载的 Python 模块的名称（无需后缀名）
[Nikola] 表
    compiler 字段
        编译器，如果是 reStructuredText 插件的话，此字段设为 rest。
    PluginCategory 字段
        插件的分类。本例设为 CompilerExtension。
[Documentation] 表
    author 字段
        作者名称
    version 字段
        版本号
    website
        插件的主页， https://github.com/zombie110year/nikola-plugin-bibcite
    description 字段
        描述

在运行时，如果会发生文件的读取，那么需要注意，当前工作目录是 `conf.py` 所在的目录。

.. [#fn-nikola-handbook] https://getnikola.com/handbook.html

###############################
Python 解析 bibliography 的方式
###############################

.. bibliography:: files/sample.bib

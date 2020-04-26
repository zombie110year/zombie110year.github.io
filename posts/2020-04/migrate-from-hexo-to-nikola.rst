---
title: 关于博客从 Hexo 迁移到 Nikola 这件事
slug: migrate-from-hexo-to-nikola
date: 2020-04-25 21:15:50 UTC+08:00
tags:
- nikola
- restructuredtext
category: blog
description: |
    Nikola 的优势、主题和插件。
type: text
---

.. default-role:: code
.. include:: _refs/abbr.rst
    :encoding: utf-8

由于在编写内容的时候受够了 Markdown 那有限的表达力，因此一直在寻找能够支持 reStructuredText 的博客生成器，
在经过多篇文章 [#fn-macplay]_ [#fn-lengyueyang]_ 的安利，加上对自身 Python 编程能力的自信，跳入了 `Nikola`_ 的阵营。

.. TEASER_END

.. contents::

################
使用体验上的更新
################

nikola 使用 :code:`nikola new_post` 创建的博文脚手架会带有 reST 注释风格 [#fn-rest-style-comments]_ 的元数据，但是我一般都换成 YAML 风格，Nikola 能直接识别。
一共有这些字段，在 Nikola Handbook 的 Metadate Fields 中有解释 [#fn-metadata-fields]_ ：

title
    文章的标题，这是方便人类阅读的，因此推荐使用任何 Unicode 符号。

slug
    文章的 slug 名，这是方便 URL 和文件系统解析的，因此推荐使用 ASCII 符号，
    在文章创建时， nikola 会强行将 title 中的非 ASCII 符号替换掉。对于中文，会替换成无音调的拼音字母。

    这个词语在此语境下的表意在词典里查不到，不过 MDN 上有一个词条 [#fn-slug-translate]_ 解释了它的含义。目前没有汉语翻译。

    认真处理这个字段，有利于 URL 的语义性，也有助于 |a_seo|。
date
    文章的创建日期。
tags
    文章的标签，是一对多的关系，在 YAML 风格下可以传入一个列表。如果仍使用 reST 注释风格的话，就传入用逗号分隔的列表。
category
    文章的分类，是一对一的关系，要么不分类，要么只能分一个。
link
    源文件的链接，在一些主题下可能渲染。对于我来说，没有设置它的需求。
description
    文章的描述，用在 HTML 头的 `<meta>` 元素中，有助于 |a_seo|。
type
    文章的类型，如果设置，将会在 `<article>` 元素中加上一个 CSS 类。
    需要主题配合以呈现不同样式。

其他还有一些有用的元数据：

previewimage
    设定一个地址，用于充当预览图（需要主题支持）。
template
    单独设置该篇文档的渲染模板。
status
    文章状态，可选值 published (default), featured, draft, or private。
    分别表示发布、未来发布、草稿和私有。

    published
        文章被渲染到 index 中，任何人都可以访问
    featured
        表示正在写作，但没有完成，在不同主题会有不同的渲染样式。
    draft
        不会渲染到输出中。
    private
        渲染到输出，但是不渲染到 index，只能通过完整链接访问。

在 Hexo 中，可以使用 `<!-- more -->` 来将内容分成两部分，前半部分在 Index（时间线） 中呈现。在 Nikola，可以用 reST 注释 `..TEASER_END` 来实现 [#fn-teasers]_ 。

同时，在 conf.py 需要将 `INDEX_TEASERS` 设置为 True。

############
对主题的处理
############

和 Hexo 丰富的主题生态相比， Nikola 的确有些贫瘠。
对于 Nikola 而言，它的衍生主题都必须继承自 `base` 或 `bootstrap` 之一。
默认的模板引擎是 mako，但也可以换成 Jinja2。

其对主题的继承关系非常傻瓜式：现用主题有的文件，就从现用主题读取，没有的，从父主题读取。

自带的默认主题满足不了我的需求，一个是需要加 `has_math` 字段才渲染公式，
我们希望这是个默认行为；另一个是要从谷歌 API 加载字体，这导致我们的网页渲染异常的慢，最好取消掉，就用每台机器都有的默认字体好了。

首先，找到默认使用的主题 bootblog4 模板所在的文件夹，然后整个复制过来，确保所有的文件都可以被我们改写掉。

Nikola 的内置主题文件位于 nikola 包的 `data/themes` 目录下，例如 `.venv/Lib/site-packages/nikola/data/themes/bootblog4/templates`

Nikola 将在站点根目录的 `themes/<theme name>` 目录下加载主题。
我将在主题修改完成后发布在 https://github.com/zombie110year/nikola-theme-zomhub 上。

测试一下语法高亮和 :math:`\KaTeX` 数学公式渲染：

.. code:: python

    def get_nikola(url: str = "https://getnikola.org/):
        """下载 Nikola 主页的 HTML"""
        resp = requests.get(url)
        if resp.status_code == 200:
            print(resp.text)

.. math::

    E = mc^2

############
对插件的处理
############

Nikola 相比文档生成工具 Sphinx_ 还是有一些不足，比如缺少一些 Directive 和 Role。
基于 docutils 提供的 Directive 和 Role 可以在 https://docutils.sourceforge.io/docs/ 查看。

构建 Nikola 插件的内容可以在 https://learn-rst.zombie110year.top 查看。

这里急需补充的 Directive 有两个：highlight 和 literalinclude，前者设置默认代码块的词法高亮，后者则拥有相比 include 更强的导入表现能力。

这些我用到的插件，会发布在 https://github.com/zombie110year/nikola-plugin-zomhub 上。

########
参考链接
########


.. _Nikola: https://getnikola.org/
.. _Sphinx: https://sphinx-doc.org/
.. [#fn-macplay] https://macplay.github.io/categories/rest/
.. [#fn-lengyueyang] https://www.lengyueyang.com/post/tools/org_mode/%E5%8D%9A%E5%AE%A2%E8%BF%81%E7%A7%BB%E6%9D%82%E8%AE%B0-%E4%BB%8E-hexo-%E5%88%B0-nikola
.. [#fn-rest-style-comments] https://www.getnikola.com/handbook.html#rest-style-comments
.. [#fn-slug-translate] https://developer.mozilla.org/zh-CN/docs/Glossary/Slug
.. [#fn-metadata-fields] https://www.getnikola.com/handbook.html#metadata-fields
.. [#fn-teasers] https://www.getnikola.com/handbook.html#teasers
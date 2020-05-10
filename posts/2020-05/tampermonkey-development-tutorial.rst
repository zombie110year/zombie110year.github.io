---
title: 'TamperMonkey 脚本开发教程'
slug: 'tampermonkey-development-tutorial'
date: 2020-05-03 09:08:32 UTC+08:00
tags:
-   tampermonkey
-   javascript
-   browser
category: tutorial
description:
type: text
---

.. abbr:: TM

    TamperMonkey

.. abbr:: AJAX

    Asynchronous JavaScript and XML

:abbr:`TM` 用户脚本，用来增强网页功能。
现在网络上很多关于安装、使用的教程，但却没有开发教程，有点令人失望。

.. contents::

.. TEASER_END

###########
TM 的文件头
###########

.. default-role:: code

:abbr:`TM` 使用 JavaScript 作为开发语言，虽然有可以选择 CoffeScript，不过这个技术好像没人用了，为了未来的可维护性，建议直接使用 JavaScript ES6 。

在 JS 文件的头部，TM 使用 `// ==UserScript==` 和 `// ==/UserScript==` 两个注释包括的特殊注释区域来标注脚本的元数据，例如通过 TM 创建的脚本默认带有以下注释：

.. code:: js

    // ==UserScript==
    // @name         New Userscript
    // @namespace    http://tampermonkey.net/
    // @version      0.1
    // @description  try to take over the world!
    // @author       You
    // @match        http://*/*
    // @grant        none
    // ==/UserScript==

所有可用的注释字段见官方文档 [#tmdoc-headers]_ ，其中经常用到的有

name
    脚本的名称，会在 Geasyfork 等发布网站和 TamperMonkey 等脚本管理器的控制面板上显示。
namespace
    命名空间，用来区分不同但 name 字段相同的脚本。如果作者并没有一个受控的域名，也可以填写邮箱等其他任何格式的 URL。它仅仅起名称区分作用，与业务逻辑无关。

version
    版本号，推荐采用语义化版本 [#semver]_。
description
    简短的描述。如果要编写长篇大论的文档，需要发布网站支持，在网站上撰写文档。
author
    你的名字、网名、笔名等。
match
    允许此脚本运行的地址，可用通配符。
grant
    启用一些额外的命令、权限，出于安全考虑，这些功能是默认禁用的。
require
    请求外部 JS 脚本，相当于将两个脚本合并，顶层作用域合并到一起，可以调用其中的函数、变量。此字段可以多次使用以导入多个资源。
    同时，可以以注释的形式附加安全性检查::

        // @require https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.js#sha384=y23I5Q6l+B6vatafAwxRu/0oK/79VlbSz7Q9aiSZUvyWYIYsd+qj+o24G5ZU2zJz
resource
    预请求外部资源，通常用来引入 CSS 样式表、图标等，可以为请求的资源命名，之后需要通过 `GM_getResourceURL` 或 `GM_getResourceText` 来导入::

        // @resource custom_style https://example.com/css/style.css
        let style = GM_getResourceText(custom_style);
        console.log(style)

    通常可以以注释的形式附加安全检查，以及多次使用导入多个资源。
connect
    定义了可以被 `GM_xmlhttpRequest` 访问的域，用来进行 :abbr:`AJAX` 。
run-at
    定义了脚本运行的时机。

    =============== ============================================================
    时机            含义
    --------------- ------------------------------------------------------------
    document-start  尽可能的早
    document-body   发现 document.body 存在时
    document-end    在 DOMContentLoaded 事件同时或之后
    document-idle   在 DOMContentLoaded 事件之后，这是默认行为
    context-menu    右键点击菜单栏手动运行（仅支持 Chromium）
    =============== ============================================================

还有三个对于脚本维护、升级很重要的字段：

updateURL
    获取升级的 URL。
downloadURL
    当检测到更新时，下载脚本的 URL。
supportURL
    用户可以提出 Issue 或寻求帮助的网址。

######
TM API
######

查阅官方文档 [#tmdoc-functions]_ ，常用的 API 有：

unsafeWindow
    提供完全访问页面的全局变量、函数的功能。
GM_addStyle
    向页面添加 CSS。
GM_getResourceText
    获取在脚本头信息中预加载的资源内容。
GM_getResourceURL
    获取在脚本头信息中预加载的资源链接，被 Base64 编码。
GM_xmlhttpRequest
    进行 AJAX。
GM_download
    将资源下载到本地。
GM_notification
    发送 HTML 5 通知。
GM_setClipboard
    将内容发送到剪贴板。

.. warning:: 请使用 WebAPI

    上面的既然写了，那就不删了，但不要用。

########
开发技巧
########

使用 debugger 语句显式调用调试器
================================

浏览器功能，如果开发者工具被打开的情况下执行到 debugger 语句，那么将会作为断点进入调试器。

##################################
实例1：利用 KaTeX 渲染网页上的公式
##################################

一些网站没有提供 MathJax 或 KaTeX 支持，但我们可以自己加上！
参考 KaTeX 官方文档 [#katexdoc-install]_ ，需要用到以下三个资源::

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css" integrity="sha384-zB1R0rpPzHqg7Kpt0Aljp8JPLqbXI3bhnPWROx27a9N0Ll6ZP/+DiW/UqRcLbRjq" crossorigin="anonymous">

    <!-- The loading of KaTeX is deferred to speed up page rendering -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.js" integrity="sha384-y23I5Q6l+B6vatafAwxRu/0oK/79VlbSz7Q9aiSZUvyWYIYsd+qj+o24G5ZU2zJz" crossorigin="anonymous"></script>

    <!-- To automatically render math in text elements, include the auto-render extension: -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/contrib/auto-render.min.js" integrity="sha384-kWPLUVMOks5AQFrykwIup5lo0m3iMkkHrD0uJ4H5cjeGihAutqP0yW0J6dpFiVkI" crossorigin="anonymous"
        onload="renderMathInElement(document.body);"></script>

当然，得载入 KaTeX CSS 样式才能正常显示。那么请看代码：

.. gist:: zombie110year/4e6e33890de8880d99bd8cfb7ff03a6c

########
参考链接
########

.. [#tmdoc-headers] https://www.tampermonkey.net/documentation.php
.. [#tmdoc-functions] https://www.tampermonkey.net/documentation.php
.. [#semver] https://semver.org/lang/zh-CN/
.. [#katexdoc-install] https://katex.org/docs/browser.html
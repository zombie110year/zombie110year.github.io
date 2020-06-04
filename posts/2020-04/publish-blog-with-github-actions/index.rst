---
title: 使用 GitHub Actions 发布博客
slug: publish-blog-with-github-actions
date: 2020-04-26 19:43:53 UTC+08:00
tags:
-   github
-   github actions
category: blog
description: GitHub 使用简单教程。
type: text
---

.. default-role:: code

GitHub 出品了官方 CI 系统：GitHub Actions，可以通过阅读其文档 [#fn-gadoc]_ 获取相关信息。
本文介绍如何通过 GitHub Actions 配置 Python 构建环境，并且将本文的输出发布到 GitHub Pages 仓库里去。

另外，也可以参考阮一峰的这两篇文章：

GitHub Actions 入门教程
    https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html
GitHub Actions 教程：定时发送天气邮件
    https://www.ruanyifeng.com/blog/2019/12/github_actions.html

.. TEASER_END

#############################
GitHub Actions 配置的基本组成
#############################

一个 Action 配置是一个存储在项目的 ./github/workflows/ 目录下的一个 YAML 格式的文件，
其文件名可以随意取名。
在 YAML 文件中，至少需要配置 `name`, `on`, `jobs` 三个字段，
分别表示

name
    工作流的名字
on
    工作流的触发条件
jobs
    工作流的具体流程

对于本博客来说，当 push 到 publish 分支时，执行工作流；
工作流的内容则是：

1. 安装依赖
2. 构建站点
3. 发布

在这个过程中，还希望能缓存安装的依赖，能加快速度。

运行条件
========

打算在将源码推送到 release 分支时触发构建，那么触发条件写作：

.. code:: yaml

    on:
      push:
        branches:
          - release

工作流内容
==========

博客的生成、发布工作连续性很强，因此只用一条工作流即可。
第一步，当然得从仓库切出源码啦，在这里可以使用 GitHub 提供的 Action 脚本
`actions/checkout@v2`，由于需要切出 release 分支内容，因此需要使用参数::

    -   name: checkout source
        uses: actions/checkout@v2
        with:
            ref: release
            lfs: true
            fetch-depth: 1

ref
    指定分支、标签等。
lfs
    启用 LFS，因为一些图片打算用 LFS 存储。
fetch-depth
    只切出最后一次 commit 的内容，减少体积。

然后，安装 Python 环境，也可以使用::

    -   name: Setup Python 38
        uses: actions/setup-python@v1
        with:
            python-version: 3.8

当一个 step 使用了 Action 脚本时，可以通过 `with` 字段来传入命名参数。

之后，安装依赖::

    -   name: install dep
        run: |
            python -m pip install -r requirements.txt

构建::

    -   name: gen site
        run: |
            nikola build

发布::

    -   name: upload to github pages
        run: |
            cd output
            echo "blog.zombie110year.top" >> CNAME
            git init
            git config user.name zombie110year
            git config user.email zombie110year
            git add -A
            git commit -m "upload"
            git push --force --quiet https://${{ secrets.UPLOAD_TOKEN }}@${{ secrets.UPLOAD_URL }} master

##########
完整的配置
##########

.. include:: .github/workflows/publish.yml
    :code: yaml
    :encoding: utf-8

########
参考链接
########

.. [#fn-gadoc] https://help.github.com/en/actions
---
title: '在 Windows 上配置 Haskell 开发环境'
slug: 'haskell-setup'
date: 2020-05-18 10:30:59 UTC+08:00
tags:
- windows
- haskell
category: code
type: text
status: draft
---

.. contents::

.. TEASER_END

##################
安装 Haskell Stack
##################

Haskell Stack [#doc-hs-stack]_ 是一个 Haskell 的工具链管理器，在 Windows 平台上可以通过 scoop 下载::

    scoop install stack

在 ``scoop info haskell`` 时，也会给出提示，将用户引导至 stack 工具。

.. abbr:: THU

    清华大学

安装好 stack 后，配置 :abbr:`THU` 的镜像 [#mirror-thu]_，不过 Windows 系统上的 stack 配置文件不在 ``~/.stack/config.yaml``，而是 ``%APPDATA%\stack\config.yaml``。

然后，通过 ``stack setup`` 安装本机适应的工具链。

.. math::

    \begin{aligned}
    \text{GHC}          &   \approx 200 \mathrm{MB} \\
    \text{MSYS2}        &   \approx 60  \mathrm{MB} \\
    \end{aligned}

之后，安装 Haskell 的包管理器 Cabal [#site-hs-cabal]_ ， 并配置镜像 [#mirror-thu]_。

########
参考链接
########

.. [#doc-hs-stack] https://docs.haskellstack.org/en/stable/README/
.. [#mirror-thu] https://mirrors.tuna.tsinghua.edu.cn/help/hackage/
.. [#site-hs-cabal] https://www.haskell.org/cabal/
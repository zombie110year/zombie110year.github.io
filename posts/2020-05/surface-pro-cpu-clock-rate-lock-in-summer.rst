---
title: 'Surface Pro 在夏天CPU锁频'
slug: 'surface-pro-cpu-clock-rate-lock-in-summer'
date: 2020-05-02 18:14:49 UTC+08:00
tags:
- surface pro
- microsoft
category: living
description:
type: text
status: draft
---

夏天到了，不知道你们有没有发现购买的 Surface Pro 设备的频率莫名其妙地降低到 0.4 甚至 0.2 GHz？

.. contents::

.. TEASER_END

#########################
检查是否为 CPU 温度的问题
#########################

提到锁频，第一时间反映的就是「过热」，所以先尝试获取 CPU 的温度数据，
检查是否为此原因。

在 GitHub 上有个叫 「OpenHardwareMonitor」[#fn-site-gh-ohm]_ 的项目提供了硬件监控功能，这是用 C# 编写的。其有一个官方网站 [#fn-site-ohm]_ ，提供了预编译包的下载。但你也可以通过 scoop 下载，其 manifest 位于 extras 仓库中::

    scoop install openhardwaremonitor

它可以挂在后台运行，甚至提供了一个 Web 服务用来展示数据：

.. figure:: /images/ohm-web-ui-shown.webp

    OpenHardwareMonitor 的 Web UI

OpenHardwareMonitor 可以通过 CPU 的 ring0 获取温度数据，相对比较准确。

##############################
Surface Pro CPU 降频的可能原因
##############################

.. abbr:: SAM

    Surface System Aggregator

.. abbr:: EC

    Embedded Controller

见知乎上的这个讨论 [#fn-zhihu-sp-article]_，可能是 :abbr:`SAM` 运行错误，
导致 CPU 在安全阈值之下被降频。

:abbr:`SAM` 是 Surface 上 :abbr:`EC` 的实现，用于管理设备的各组件，是高于操作系统甚至 BIOS/UEFI 的固件 [#fn-zhihu-what-is-ec]_ 。


#######################
利用 Intel XTU 调试 CPU
#######################

参考 [#fn-zhihu-xtu]_ 。Intel XTU 工具的下载链接为
https://downloadcenter.intel.com/zh-cn/download/24075/-XTU



########
参考链接
########

.. [#fn-site-gh-ohm] https://github.com/openhardwaremonitor/openhardwaremonitor
.. [#fn-site-ohm] https://openhardwaremonitor.org/
.. [#fn-zhihu-xtu] https://zhuanlan.zhihu.com/p/25537264
.. [#fn-zhihu-sp-article] https://zhuanlan.zhihu.com/p/59289369
.. [#fn-zhihu-what-is-ec] https://zhuanlan.zhihu.com/p/80568996

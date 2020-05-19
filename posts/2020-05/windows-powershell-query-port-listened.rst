---
title: 'Windows PowerShell 查看端口占用'
slug: 'windows-powershell-query-port-listened'
date: 2020-05-19 08:15:24 UTC+08:00
tags:
-   windows
-   powershell
-   network
category: life
description: 使用 PowerShell Cmd-Let 查询端口占用
type: text
---

TCP 链接和 UDP 链接的查询指令是分别的两个：

Get-NetTCPConnection
    查询 TCP 链接
Get-NetUDPEndPoint
    查询 UDP 链接

要查询 8000 被哪个进程占用，查询 TCP 链接情况::

    Get-NetTCPConnection -LocalPort 8000

返回结果具有 ``OwningProcess`` 字段，存储了对应的 PID，然后通过 ``Get-Process`` 查询::

    Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

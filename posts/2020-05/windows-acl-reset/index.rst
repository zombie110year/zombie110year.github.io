---
title: 'Windows 文件访问权限重置'
slug: 'windows-acl-reset'
date: 2020-05-19 07:53:20 UTC+08:00
tags:
-   windows
-   acl
category: life
description: 重装系统后重置文件权限。
type: text
---

当重装系统后，即便名称和邮箱完全相同，新创建账户的 GUID 也与之前的账户不一样，因此，硬盘上的文件的 「所有者」将会成为一个已经不存在的用户。而在读写时，会遇到 PermissionError。
因此，需要将文件的所有者修改为新的账户，如果通过图形界面来修改，则非常的麻烦。Windows 提供了名为 ``icacls`` 的命令行程序用来管理 ACL 表，这个程序使用 DOS 风格的命令行参数。
递归地重置一批文件的 ACL 可使用命令::

    icacls * /reset /T /C

``*``
    路径通配符
``/reset``
    重置指令
``/T``
    递归选项
``/C``
    遇到错误也继续

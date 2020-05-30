---
title: '文件隐写术'
slug: 'file-steganography'
date: 2020-04-27 11:44:30 UTC+08:00
tags:
- powershell
- steganography
- security
category: tutorial
description: |
    利用文件读写特性和 NTFS 系统的交换数据流来隐藏数据。
type: text
---

谁不想在自己的电脑上藏一些东西呢？
要隐藏一些内容，设置隐藏文件夹太 LOW，可以将硬盘主动分一个区，在不用的时候取消挂载，这样别人就算勾选了 『显示隐藏文件和文件夹』也看不到，因为内容根本没进入文件系统。

.. thumbnail:: /images/windows10-diskmgr-unmount.webp
    :width: 400px

    在 Windows 10 的磁盘管理器中取消分配盘符

不过，这种方法只适用于本地环境，如果通过网络传输，就没有意义了。
因此，我们可以尝试使用文件级的 Hack 来达成目的。

.. contents::

.. TEASER_END

.. default-role:: code

##############################
一个老办法：将文件追加到图片后
##############################

相信很多人都看过这样的一个技巧::

    copy /b a.png+b.txt c.png

这样就能把一个文件文件隐藏在图片中，并且 c.png 可以正常打开，从图像上也读不出任何信息。
但在这个文件的末尾，却能够看到出现文本文件中的内容。

这是因为，图片等文件在文件头处存储了内容的长度，超过这个长度的部分将被忽略，不会被图片浏览器读取。
因此，在二进制层面上看，虽然文件的末尾已经添加了一部分字节，但是图像本身是不知道的。

`copy` 是 cmd.exe 的指令，它的作用是复制文件。
懂得了上面处理的原理，应该就能写出在其他各平台上的处理办法::

    # Linux
    cat a.png b.txt > c.png
    # cmd.exe
    type a.png b.txt > c.png
    # PowerShell
    # 不建议用 PowerShell，读取字节时卡爆了


除了文本文件，还可以加 ZIP 压缩包等。

其他图片隐写需要一定的专业知识， 这篇文章 [#zh-pic-ste]_ 进行了简单的介绍。

###############
NTFS 交换数据流
###############

.. abbr:: ADS

    Alternate Data Stream

对于 Windows 使用的 NTFS 文件系统，它提供了名为 :abbr:`ADS` 的特性，可以让我们将一些数据附加（也称「寄生」）在一个文件上。
为了接下来表达上不出现歧义，我们将一个能通过文件系统直接访问的对象称为「文件入口」、
将一个文件在磁盘上的实际数据称为「文件内容」。

ADS 所寄生的数据拥有实际的文件内容，但没有文件入口，除非创建一个符号链接。

创建 ADS
========

cmd.exe 可以通过管道重定向的方式创建 ADS::

    # 创建宿主文件
    echo Hello > a.txt
    # 将内容写入 ADS
    echo World > a.txt:b.txt

如上，便创建了一个名为 b.txt 的寄生在 a.txt 上的 ADS。
这个 ADS 不会在图形界面上显示，也不会在 a.txt 的尺寸上统计、甚至不会统计到文件夹的尺寸大小上。

可以用 more 读取文本内容的 ADS::

    more < a.txt:b.txt

一些二进制编辑器，例如 HxD [#site-hxd]_ 也可以通过命令行参数读取 ADS::

    hxd a.txt:b.txt

交换流的发现::

    # 可以通过 dir /r 来查看交换流
    dir /r

创建符号链接以便访问（需要管理员权限）::

    mklink b.txt a.txt:b.txt

通过二进制读写，将交换流的文件内容复制到另一个文件::

    more <a.txt:b.txt >bb.txt

交换流的删除::

    # 删除宿主，则 ADS 也被删除
    del a.txt

复制宿主也会复制 ADS::

    copy a.txt aa.txt
    dir /r

########
参考链接
########

.. [#zh-pic-ste] https://zhuanlan.zhihu.com/p/62895080
.. [#site-hxd] https://mh-nexus.de/en/hxd/
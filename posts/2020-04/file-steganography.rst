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
status: draft
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
    # PowerShell
    # 不建议用 PowerShell，读取字节时卡爆了

除了文本文件，还可以加 ZIP

.. TODO

########
参考链接
########

https://zhuanlan.zhihu.com/p/62895080
https://zhuanlan.zhihu.com/p/30539398
https://3gstudent.github.io/3gstudent.github.io/%E9%9A%90%E5%86%99%E6%8A%80%E5%B7%A7-%E5%88%A9%E7%94%A8JPEG%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F%E9%9A%90%E8%97%8Fpayload/
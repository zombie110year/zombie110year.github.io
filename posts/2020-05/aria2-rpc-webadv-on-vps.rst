---
title: '在 VPS 上配置 Aria2 RPC 服务并将文件同步至坚果云 webdav'
slug: 'aria2-rpc-webdav-on-vps'
date: 2020-05-15 12:51:02 UTC+08:00
tags:
-   vps
-   aria2
-   webdav
-   坚果云
category: life
description:
type: text
---

.. contents::

.. TEASER_END

.. todo

    OneDrive
    奶牛快传
    FireFox Send

##############
Aria2 RPC 配置
##############

.. listing:: aria2-rpc.conf ini

###########
WebDav hook
###########

Rclone [#site-rclone]_ 是个好软件，除了 WebDav 以外，还支持一大票网盘和对象存储服务。如果不出意外的话，之后会介绍的挂载 OneDrive 也会用它。

例如，配置坚果云的 WebDav，我们先在坚果云的网盘上创建一个单独的文件夹，例如命名为 ``vps-download`` 好了，然后创建一个新的 WebDav 角色，也命名为 ``vps-download``， 将会得到一个应用密码，之后用 passwd 表示它。这一配置位于网页端的 『账户信息』『安全选项』里面。

那么，连接坚果云的三个要素就确定了：

URL 地址：
    ``https://dav.jianguoyun.com/dav/vps-download``
用户账户
    登录坚果云的用户账户，不是应用账户。
应用密码
    上述步骤所创建的应用密码 passwd。

可以通过 ``rclone config`` 命令来进行交互式的配置，也可以直接编辑位于 ``~/.config/rclone/rclone.conf`` 的配置文件。
每一个表对应一个 remote，推荐在创建新 remote 时不要在名字中加空格，因为在后期还需要在命令行中使用：

.. code:: ini

    [JianGuoDav]
    type = webdav
    url = https://dav.jianguoyun.com/dav/vps-download
    vendor = other
    user = 用户账户
    pass = 散列后的应用密码

推荐在本地配置好后将 rclone 配置文件上传到 VPS。

在配置好后，就可以使用命令::

    rclone copy example.txt JianGuoDav:/

将本地的 example.txt 上传到远程了，远程的根目录是从 /vps-download 开始计算的，如果没有指定文件名，则使用与源文件相同的文件名。
由于 BT 的多文件下载比较复杂，因此后续再处理，这里只处理普通下载文件和 Bt 单文件的上传：

.. code:: sh

    # on download complete
    gid=$1
    fnum=$2
    fpath=$3
    now=$(date '+%Y-%m-%d %H:%M:%S')
    log=/data/log/aria2-webdav.log
    # 通过 rclone 上传
    rclone copy "$fpath" "JianGuoDav:/"
    if [[ $? -ne 0 ]]; then
        echo "[$now] WARNING rclone copy $fpath failed" >> $log
    else
        echo "[$now] INFO save $fpath, numbers: $fnum" >> $log
    fi

########
参考链接
########

.. [#site-rclone] https://github.com/rclone/rclone
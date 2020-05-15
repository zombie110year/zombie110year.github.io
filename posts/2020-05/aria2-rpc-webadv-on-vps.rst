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

#############
OneDrive Hook
#############

首先，你得在 **安装了浏览器** 的日常使用主机上安装
rclone，这样才能弹出一个页面进入 OneDrive 网站上获取授权。

在 Windows 系统上用 ``scoop install rclone`` 安装了 rclone 后，运行
``rclone authorize onedrive`` ，然后会弹出浏览器窗口，进入微软登录页面用
OAuth2 验证。

输入你的微软帐号密码登录后，rclone 就取得了微软授权，在终端中显示授权码。这个授权码可以保存下来给其他 rclone 程序使用（例如我们要作为下载服务器的主机）。

::

    # rclone authorize onedrive
    2020/02/02 00:22:07 NOTICE: Config file "C:\\Users\\zom\\.config\\rclone\\rclone.conf" not found - using defaults
    If your browser doesn't open automatically go to the following link: http://127.0.0.1:53682/auth?state=_yOQ6xvaun9P7FSOIj-2aw
    Log in and authorize rclone for access
    Waiting for code...
    Got code
    Paste the following into your remote machine --->
    {"access_token":"EwCAA8l6BAAUO9**************************************************************防止泄漏************************************************************************DAs$","expiry":"2020-02-02T01:27:49.2021085+08:00"}
    <---End paste

可以看到， rclone 用 JSON 配置它自己，并且从 ``expiry`` 字段读取到，这个授权码存在一个有效期，过期后不可用。上面的 paste 部分保存下来，命名为 onedrive.json。

执行 ``rclone config`` 进入配置流程，下面会先介绍输入，然后展示当时的终端情况。

1. rclone 询问你的意图

我们选择 ``n``\ ，新建一个 remote。

::

    e) Edit existing remote
    n) New remote
    d) Delete remote
    r) Rename remote
    c) Copy remote
    s) Set configuration password
    q) Quit config
    e/n/d/r/c/s/q> n

2. 设置新 remote 的名字

随便起一个就好，例如，因为 OneDrive 是微软家的，就取名叫 ``ms`` 了。

::

    name> ms

3. 选择服务提供方

选择 ``22`` ，微软 OneDrive。

**注意，如果 rclone 版本不同，编号可能不一样，记得看准了选**，
其他用不到的部分已被略去。

::

    Type of storage to configure.
    Enter a string value. Press Enter for the default ("").
    Choose a number from below, or type in your own value
    21 / Microsoft Azure Blob Storage
       \ "azureblob"
    22 / Microsoft OneDrive
       \ "onedrive"
    23 / OpenDrive
       \ "opendrive"
    storage> 22

特别说明一下， ``drive_id`` 是微软给你的 OneDrive 帐号分配的
ID，可以在网页登录 OneDrive 时从 URL 中获取.

4. 询问 Microsoft App Clinet ID，由于没有，所以留空。

::

    ** See help for onedrive backend at: https://rclone.org/onedrive/ **

    Microsoft App Client Id
    Leave blank normally.
    Enter a string value. Press Enter for the default ("").
    client_id>

5. Microsoft App Client Secret，同样留空。

::

    Microsoft App Client Secret
    Leave blank normally.
    Enter a string value. Press Enter for the default ("").
    client_secret>

6. 询问是否进阶编辑，选择是。

::

    Edit advanced config? (y/n)
    y) Yes
    n) No
    y/n> y

7. Chunk Size，保持默认即可。

::

    Chunk size to upload files with - must be multiple of 320k (327,680 bytes).

    Above this size files will be chunked - must be multiple of 320k (327,680 bytes). Note
    that the chunks will be buffered into memory.
    Enter a size with suffix k,M,G,T. Press Enter for the default ("10M").
    chunk_size>

8. 是否自动配置 remote，选择 ``n``\ ，因为远程服务器没有浏览器。

::

    Remote config
    Use auto config?
     * Say Y if not sure
     * Say N if you are working on a remote or headless machine
    y) Yes
    n) No
    y/n> n

9. 输入我们之前获取的 onedrive.json 文件内容。

::

    For this to work, you will need rclone available on a machine that has a web browser available.
    Execute the following on your machine (same rclone version recommended) :
           rclone authorize "onedrive"
    Then paste the result below:
    result> {******* 敏感信息，已隐藏 ********}

10. 选择 OneDrive 服务类型，个人版就选 1，persional 或 bussiness
    这一类。

::

    Choose a number from below, or type in an existing value
     1 / OneDrive Personal or Business
       \ "onedrive"
     2 / Root Sharepoint site
       \ "sharepoint"
     3 / Type in driveID
       \ "driveid"
     4 / Type in SiteID
       \ "siteid"
     5 / Search a Sharepoint site
       \ "search"
    Your choice> 1

11. rclone 通过之前的配置，查询到微软服务器上你的 OneDrive 帐号对应的 ID，让你选择

如果买了多个 OneDrive 计划的话，可能有多种选择，选其中一个方便的就好。

::

    Found 1 drives, please select the one you want to use:
    0:  (personal) id=c***********0
    Chose drive to use:> 0

12. 配置基本完成，接下来一路 ``y``
    过去就好了，问的问题都是「你的配置是不是这样？」、「还要继续配置其他
    remote 吗？」这样的问题。

然后将生成的 ``~/.config/rclone/rclone.conf`` 中 ``[ms]`` 表下的内容上传到 VPS 即可使用。

事件钩子和 `WebDav hook`_ 一样，只不过将远程修改一下即可。

########
参考链接
########

.. [#site-rclone] https://github.com/rclone/rclone
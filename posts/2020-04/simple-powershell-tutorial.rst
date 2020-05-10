---
title: 简单的 PowerShell 教程
slug: simple-powershell-tutorial
date: 2020-04-25 20:04:38 UTC+08:00
tags:
- powershell
category: tutorial
link:
description: |
    基于日常使用的 PowerShell 教程。
type: text
---

.. default-role:: code

介绍了 PowerShell 的控制语句、函数定义和管道操作中常用的方法。

.. contents::

.. TEASER_END

#####################
PowerShell 字符串操作
#####################

在任何 Shell 中字符串操作都是最常用的，在处理 stdio 内容、拼接命令行参数等情形下都需要操作字符串。
PowerShell 提供了字符串的以下功能：

拼接
    使用运算符 `+` 即可::

        ("hello" + " " + "world") -eq ("hello world")

重复
    使用运算符 `*` 即可::

        ("abc" * 3) -eq ("abcabcabc")

模板字符串
    在用 `"` 双引号包裹的字符串中，可以插入变量或表达式的值::

        $name = "Zombie110year"
        "hello $name"

        "1 + 3 = $( 1 + 3 )"

    表达式内的空白不是必须的，出于美观和个人喜好而加上。

    对于一些变量，我们希望在字符串中插入它的某个属性，例如一个文件的大小::

        $file = (ls conf.py)

    但如果按照下面的方式 『使用点运算符』 的话，实际上只是将 `$file` 插入到目标位置::

        "file is $file.Length bytes."
        # file is C:\Users\*\.local\blog\conf.py.Length bytes.

    要取出某个属性，需要按照嵌入表达式的值的方法::

        "file is $( $file.Length ) bytes."

    而对于单引号包裹的字符串，则不会应用为模板字符串，可以把它当作纯字面量::

        '1 + 3 = $( 1 + 3 )'

PowerShell 中的字符串可以换行，直到遇见下一个分界符 `"` 或 `'` 为止，
在 PowerShell 中，由于 `\\` 符号被用作路径分隔符，因此使用反引号来作为转义符号。

搜索替换
    可以使用 `-contains` 运算符来检测一个容器中是否包含某个元素，对于字符串，可以用::

        "abc" -contains "a"

    来检测字符串中是否包含某个子串。
    如果要得到子串在字符串中的索引值，需要调用 String 类型的方法 `IndexOf`::

        "abc".IndexOf("b") -eq 1

    要替换字符串中的某个模式，可以使用 `-replace` 运算符，它接受一个二元组作为参数，前者表示模式，后者表示替换内容::

        ("C:\Users\hello\Desktop" -replace "\\","/") -eq "C:/Users/hello/Desktop"

    值得注意的是，模式其实是正则表达式，而不是一个简单字符串。在正则表达式中，反斜杠代表转义。

正则表达式
    对字符串进行正则表达式操作，可以使用 `-match` 或 `-replace` 运算符，前者检查一个正则是否匹配，后者则是搜索替换。
    注意，正则匹配的捕获组将会存储在一个名为 `$Matches` 的变量中，而 `-match` 表达式的返回值是一个布尔值::

        ("ann 18 student" -match "(\S+) (\d+) (\S+)") -eq $true
        ($Matches[0]) -eq "ann 18 student"
        ($Matches[1]) -eq "ann"
        # ...

#######################
PowerShell 中的控制语句
#######################

条件分支
========

PowerShell 提供了 if-else 语句与 switch 语句::

    if ($cond) {
        # true
    } else {
        # false
    }

PowerShell 的 Switch 非常 Powerful，它的基本使用形式是::

    switch [-option] ($var) {
        {<# 条件表达式 #>} { <# 执行体 #>}
    }

对于一般的用法，可以用来匹配离散值，所有剩余情况可以将转到 `Default` 分支执行::

    switch ($var) {
        1 { echo "H" }
        2 { echo "e" }
        3 { echo "y" }
        Default { echo "EOF" }
    }

还可以用来匹配一个区间，在条件表达式里可以用 `$_` 来表示传入的数值（这个值在管道中也表示相同含义）::

    switch ($var) {
        { $_ -lt 0 } { echo "$_ < 0" }
        { $_ -lt 100 } { echo "$_ < 100" }
        Default { echo "?" }
    }

值得一提的是，每条匹配的分支都会执行一次（Default 除外），如果希望只处理第一条匹配的分支，那么可以在每条分支后加 `Break` 关键字::

    switch ($var) {
        { $_ -lt 0 } {
            echo "$_ < 0"
            Break
        }
        { $_ -lt 100 } {
            echo "$_ < 100"
            Break
        }
        Default { echo "?" }
    }

在匹配字符串上， Switch 也提供了易用的功能::

    # 默认的匹配是大小写不敏感的
    switch ("abc") {
        "ABC" { "OK" }
        "abc" { "ok" }
    }

    # 加上 -case 选项，使大小写敏感
    switch -case ("abc") {
        "ABC" { "OK" }
        "abc" { "ok" }
    }

    # 加上 -wildcard 或 -regex 以支持通配符/正则表达式
    switch -wildcard ("readme.txt") {
        "*.md" { echo "Markdown" }
        "*.txt" { echo "Plain Text" }
    }
    switch -regex ("readme.txt") {
        "\S+.md$" { "Markdown" }
        "\S+.txt$" { "Plain Text" }
    }

Switch 还可以同时处理多个值，例如，下面这段代码将打印出各数位和等于 9 的三位数::

    switch(100..999) {
        {
            $a0 = [Math]::Truncate($_ / 100);
            $a1 = [Math]::Truncate($_ % 100 / 10);
            $a2 = [Math]::Truncate($_ % 10);
            ($a0 + $a1 + $a2) -eq 9
        } { echo "$_" }
    }

循环迭代
========

还提供了 while 循环::

    while($cond) {
        # ...
    }

还提供了 C 风格的 for 循环::

    # 1 + 2 + ... + 100
    $sum = 0;
    for($i = 0; $i -le 100; $i++) {
        $sum += $i;
    }
    $sum -eq 5050

以及 foreach-in 循环::

    foreach($i in (ls)) {
        echo "$($i.Length) Bytes file: $($i.Name);
    }

###################
PowerShell 容器类型
###################

PowerShell 提供数组与表::

    # 字面量用 , 分隔，没有空格
    $arr = 1,2,3,4
    # 对于连续数字，可以用区间表示法，这是闭区间
    $arr = 1..4
    # 也可以加上界定符 @()
    $arr = @('a', 2, 'three')
    # 表用 @{} 界定符
    $tab = @{
        Name = "小明";
        Age = 24;
        Job = "待业";
    }

都通过 `[index]` 进行 访问::

    # 数组索引从 0 开始
    $arr[0]
    # 如果为负数，则逆序访问，类似 Python
    $arr[-1]
    # 用一个范围做切片
    $arr[1..3]
    # 逆序切片
    $arr[3..1]
    # 表可以通过点运算符访问，如果键的命名满足标识符格式的话
    $tab["Name"] -eq $tab.Name

数组的大小是固定的，因此不能插入或删除值，要做到这点，必须创建新的数组::

    $arr += "abc"

    $arr = $arr[0..($arr.Count - 1)]

默认的数组是弱类型的，但是在声明数组时使用类型标注可以让其生成强类型数组::

    [int[]] $arr = 1,2,3,4,5
    $arr += "string"

    无法将值“string”转换为类型“System.Int32”。错误:“输入字符串的格式不正确。”
    所在位置 行:1 字符: 5
    +     $arr += "string"
    +     ~~~~~~~~~~~~~~~~
        + CategoryInfo          : MetadataError: (:) [], ArgumentTransformationMetadataException
        + FullyQualifiedErrorId : RuntimeException

###############
PowerShell 函数
###############

PowerShell 中的函数通过 `function` 关键字来定义::

    function func {
        echo Hello
    }

当调用时，通过 `函数名 参数0 参数1 ...` 的方式调用。
函数可以用 `$args` 访问所有传入的参数，不过由于这些参数需要手动解析，很不易用。
因此，通常在一个 `param` 块中定义函数的参数，例如，为开启 aria2c 的 RPC 服务而定义一个函数::

    function aria2c-rpc {
        param([switch] $hidden)
        if ($hidden) {
            Start-Process -FilePath aria2c.exe -WindowStyle Hidden
        } else {
            aria2c.exe
        }
    }

在 `param` 块中定义的参数可以设定类型，也可以设定默认值；参数之间用逗号分隔::

    function gitignoreapi {
        param(
            [string] $language = "python",
            [string] $output   = ".gitignore"
        )
        curl.exe -o $output "https://gitignore.io/api/$language"
    }

这样定义的函数，可以通过 `-参数名 参数值` 的方式传递参数。
特别的是 `[switch]` 类型的参数，它不接受值，当参数中存在此选项时，其值为 `$true` 否则为 `$false`。

函数的最后一个表达式的值就是它的返回值，也可以用 return 指定。

############################
基于管道的 PowerShell 工作流
############################

在管道传递中，无法使用 if-else foreach 等控制语句，PowerShell 提供了 `ForEach-Object` 和 `Where-Object` 来完成它们的任务。

ForEach-Object
    对每一个对象执行一定的命令，命令通过 `-Process` 参数传入，例如::

        1..10 | ForEach-Object -Process { echo $($_ * 2) }

    将会输出传入数字的两倍。

Where-Object
    过滤对象，只有判断条件为 `$true` 的对象才会进入管道的下一级，条件表达式通过 `-FileterScript` 传入::

        1..10 | Where-Object -FilterScript { $_ % 2 -eq 1 }

使用管道时必须要小心，它消耗的资源特别大。
不过根据 [#fn-anonymous-block]_ 的说法，使用匿名脚本块代替 ForEach-Object 可以提高 200 倍的速度::

    1..10 | & { process { $_ * $_ } }

代码块里的 `process` 是 PowerShell 高级方法的内容，参考 [#fn-advanced-methods]_。

##################
调用 .Net 静态方法
##################

一些模块已经封装在 PowerShell 中了，可以通过 `[模块名]` 来访问。
例如::

    [Math]::Pow(2, 8) -eq

########
必知必会
########

Get-Command
===========

一个帮助使用 PowerShell 的指令，可以接受一个通配符，查询所有相关的可用命令::

    Get-Command *-Process

::

    CommandType Name          Version Source
    ----------- ----          ------- ------
    Cmdlet      Debug-Process 3.1.0.0 Microsoft.PowerShell.Management
    Cmdlet      Get-Process   3.1.0.0 Microsoft.PowerShell.Management
    Cmdlet      Start-Process 3.1.0.0 Microsoft.PowerShell.Management
    Cmdlet      Stop-Process  3.1.0.0 Microsoft.PowerShell.Management
    Cmdlet      Wait-Process  3.1.0.0 Microsoft.PowerShell.Management

Start-Process
=============

Start-Process 用来启动一个进程，重要的参数有三个：

-FilePath       可执行文件的路径，如果在 $env:Path 下，则只需要文件名
-ArgumentList   可执行文件接受的命令行参数，用字符串形式传递，
                各参数用逗号分隔（PowerShell 的字符串数组）
-WindowStyle    窗口模式，如果设置为 Hidden 则没有窗口，否则弹出 cmd 窗口。

Get-Process 与 Stop-Process
===========================

用来查找进程与终止进程的。
一般对前者用 `-Name` 参数查找一组匹配通配符的进程，获取其 PID，
然后调用后者 `-Id` 参数精确终止进程::

    Get-Process -Name *brook*
    Stop-Process -Id 8123

Start-Job
=========

启动一个后台任务，任务需要执行的命令通过 `-ScriptBlock` 传入::

    Start-Job -ScriptBlock {
        # ...
    }

任务创建后即开始运行。可以通过 Get-Job 查看状态。其他相关的指令自行用 `Get-Command *-Job` 查询。

Read-Host
=========

Read-Host 从 stdin 读取输入，返回给一个变量。
注意，可能会有人用 `$input = Read-Host` 来接受输入，
但是 `$INPUT` 是一个自动变量，有特殊含义，不能被赋值。
因此最好采用其他变量名。

Read-Host 的输出格式是 string，常用的参数有

-Prompt             提示符
-AsSecureString     是否以安全模式读取，如果设置，则回显将被替换为星号，且
                    输出类型为 SecureString [#fn-secure-string]_ 。

Out-File
========

Out-File 用于将内容输出到文件，常用的参数有

-FilePath           被写文件的路径
-Encoding           设置字符编码，为了通用性，最好都显式设置为 utf-8
-InputObject        内容，应当为字符串类型，否则会被转换为字符串
-Append             switch 类型的参数，是否以追加模式写入，默认是截断模式

Get-Content
===========

Get-Content 用来获取文件的内容，Set-Content 用来向文件写入内容。

Get-Content 的输出是按行分隔的 `string[]`，常用的参数有

-Delimiter          分隔符，默认是换行符
-Encoding           字符编码
-Exclude            排除一些文件，支持通配符；筛选的最后一步
-Filter             只接受一些文件，支持通配符；在获取对象时就被应用
-Path               文件路径，支持通配符
-Raw                switch 类型，不分行，以原始模式读取
-ReadCount          限制读取行数
-Tail               读取文件末尾的行

####
例子
####

用 PowerShell 代替 Nikola 的 new_post 指令
==========================================

.. listing:: userfunc-nikola-new.ps1 powershell

用 PowerShell 起一个 HTTP 服务器
================================

########
推荐链接
########

学习 PowerShell 的几个好网站：

PowerShell 中文博客
    https://www.pstips.net/

    人数挺多，挺活跃的。
叹为观止
    https://blog.vichamp.com/

    一个更新非常活跃的个人博客，大部分内容是 PowerShell 技巧。

########
参考链接
########

.. [#fn-secure-string] SecureString 的加密是单向的，无法还原。
.. [#fn-anonymous-block] https://blog.vichamp.com/2019/07/15/increasing-pipeline-speed/
.. [#fn-advanced-methods] https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_methods?view=powershell-7
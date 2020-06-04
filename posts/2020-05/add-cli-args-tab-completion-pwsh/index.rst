---
title: '向 PowerShell 添加命令行工具的参数自动补全'
slug: 'add-cli-args-tab-completion-pwsh'
date: 2020-05-11 16:34:02 UTC+08:00
tags:
category:
description: 使用 Register-ArgumentCompleter 命令注册补全函数。
type: text
---

PowerShell 提供了 Register-ArgumentCompleter 命令 [#cmd-rac]_ 用于注册自定义命令的参数补全函数。
以如下语法进行注册：

.. code:: powershell

    Register-ArgumentCompleter -Native -CommandName <String[]> -ScriptBlock <ScriptBlock>

-Native         一个 ``[switch]`` 类型的选项，表明此补全代码用于非 PowerShell
                提供的原生命令。由于本教程主要介绍为 Unix 迁移过来的命令行工具
                添加补全，因此这个选项将会一直使用。
-CommandName    指定要添加补全的命令名称。
-ScriptBlock    指定用于提供补全的代码块，至少接受三个参数。

.. contents::

.. TEASER_END

#############################
ArgumentCompleter ScriptBlock
#############################

.. default-role:: code

此脚本块至少需要接受三个参数，按顺序分别是 `$wordToComplete` 、 `$commandAst` 、`$cursorPosition`。

wordToComplete
    当按下 Tab 键时，若光标紧邻一个单词，那么从光标所在位置直到上一个空白字符之间的内容将会作为此变量提供。常用于补全某个不完整的参数组件。
commandAst
    整个命令行的 Ast 结构。
cursorPosition
    光标在整个命令行中的位置，一个命令行的开头是从 0 开始的。
    不会忽略首个命令之前的空白字符，因此最好当成相对量来使用，只用于决定移动光标的起点。

通过研究 rustup 提供的补全脚本（使用 `rustup completions powershell` 获取），可以发现编写一个补全脚本通常需要完成以下步骤：

分析 Ast，构造补全条件分支
    rustup 的做法是将目前所有的命令元素通过特定编码组合成一个字符串，
    然后在后续的步骤中通过一个 swtich 语句提供对应命令+子命令的参数补全。
为各个分支编写补全项
    使用 `[CompletionResult]::new` 静态函数创建一个补全项，其完整的签名为：

    .. code:: csharp

        System.Management.Automation.CompletionResult new(string completionText, string listItemText, System.Management.Automation.CompletionResultType resultType, string toolTip)
匹配 wordToComplete 提供补全
    通过命令::

        $completions.Where{ $_.CompletionText -like "$wordToComplete*" } |
            Sort-Object -Property ListItemText

    最后返回的是一个由 CompletionResultType 组成的列表。

#########################
练习：为 WSL 提供命令补全
#########################

.. listing:: tab-completion-for-wsl.ps1 powershell

通过命令行描述创建补全项的正则表达式::

    ^(-{1,2})(\S+)\s+(\S+(?:[\s\S]+)?)$

    [CompletionResult]::new('$1$2', '$2', [CompletionResultType]::ParameterName, '$3')

这个正则可以将 `--ParameterName ParameterDescription` 形式的字符串转成上述命令。

########
参考链接
########

.. [#cmd-rac] https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/register-argumentcompleter
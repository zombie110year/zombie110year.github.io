---
title: '在 PowerShell 中并行执行任务'
slug: 'parallel-job-in-powershell'
date: 2020-06-01 13:10:14 UTC+08:00
tags:
-   powershell
category: code
description: 在 PowerShell 中运行后台任务
type: text
---

在 Bash 等 Shell 中，可以通过 ``bin >stdout.txt 2>stderr.txt &`` 来运行后台任务，并将输出收集到对应文件，
在 PowerShell 中，则使用一套 *-Job Cmdlet 来进行后台任务的处理。

Job 是一个新的 PowerShell 进程，而不是线程。

.. TEASER_END

创建 Job
========

通过 ``Start-Job`` 来创建一个 Job，在创建后会立刻执行，并返回一个标记，用来联系到后台任务实例：

.. code:: powershell

    $job = Start-Job -ScriptBlock { echo Hello }

创建 Job 时，如果要调用外部程序，如果可执行文件在 Path 中，那么一切正常；
如果可执行文件在某个非 Path 目录里，那么需要考虑当前工作目录的问题，最好采用绝对路径指定要运行的程序，在默认情况下，Job 将会把用户的 「文档」 文件夹作为当前工作目录。

收集 Job 输出
=============

Job 的输出会被自动收集，不在控制台显示，要得到输出，需要等待任务完成后，用：

.. code:: powershell

    Receive-Job $job

来得到输出。该任务的 ScriptBlock 中代码在 stdout 的输出可以通过此方法获取。
如果有多个程序会向 stdout 写入，那么它们的输出会被合成到一起。

多 Job 管理
===========

当创建 Job 时，它们会自动开始运行，可以通过 ``Get-Job`` 来查询当前所有 Job 的运行状态。
并可以对同样的 Cmdlet 传入参数，如 Job 的 ID 来获取其实例，以便下一步处理。
对于 State 为 Completed 的 Job，可以用 ``Receive-Job`` 获取其输出。

Job 的输出在结束后会一直保留到退出当前 PowerShell 会话为止，如果要提前清除，可以使用 ``Remove-Job``。

可以使用 ``Suspend-Job`` 来暂停一个 Job，用 ``Resume-Job`` 来恢复。

可以使用 ``Wait-Job`` 并传入一个 Job 实例组成的数组，当运行到此时，当前进程会挂起，直到其中所有 Job 都完成才会恢复。

实例
====

同时更新多个 git 仓库
---------------------

.. code:: powershell

    $repos = (ls)

    echo "开始"
    foreach($i in $repos) {
        $path = Resolve-Path $i
        Start-Job -ScriptBlock {
            cd $path;
            git fetch;
        }
    }
    $jobs = Wait-Job (Get-Job)
    echo "结束"

进阶：runspace
==============

.. todo

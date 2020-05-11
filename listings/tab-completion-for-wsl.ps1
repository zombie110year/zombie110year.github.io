<#
wsl 没有子命令
#>
Register-ArgumentCompleter -Native -CommandName wsl -ScriptBlock {
    param(
        $wordToComplete,
        $commandAst,
        $cursorPosition
    )

    $completions = @(
        [CompletionResult]::new('--exec', 'exec', [CompletionResultType]::ParameterName, "执行指定的命令而不使用默认的 Linux Shell")
        [CompletionResult]::new('--distribution', 'distribution', [CompletionResultType]::ParameterName, "运行指定的发行版")
        [CompletionResult]::new('--user', 'user', [CompletionResultType]::ParameterName, "指定用户")
        [CompletionResult]::new('--export', 'export', [CompletionResultType]::ParameterName, '导出发行版文件系统')
        [CompletionResult]::new('--import', 'import', [CompletionResultType]::ParameterName, '通过 tar 包导入发行版文件系统')
        [CompletionResult]::new('--list', 'list', [CompletionResultType]::ParameterName, '列出发行版')
        [CompletionResult]::new('--set-default', 'set-default', [CompletionResultType]::ParameterName, '设置默认发行版')
        [CompletionResult]::new('--set-default-version', 'set-default-version', [CompletionResultType]::ParameterName, '设置新发行版的安装版本（WSL 1 或 WSL 2）')
        [CompletionResult]::new('--set-version', 'set-version', [CompletionResultType]::ParameterName, '设置发行版的版本')
        [CompletionResult]::new('--shutdown', 'shutdown', [CompletionResultType]::ParameterName, '终止所有正在运行的发行版和 WSL 2 虚拟机')
        [CompletionResult]::new('--terminate', 'terminate', [CompletionResultType]::ParameterName, '终止指定的发行版')
        [CompletionResult]::new('--unregister', 'unregister', [CompletionResultType]::ParameterName, '注销发行版')
        [CompletionResult]::new('--help', 'help', [CompletionResultType]::ParameterName, '显示帮助')
    )

    $completions
}
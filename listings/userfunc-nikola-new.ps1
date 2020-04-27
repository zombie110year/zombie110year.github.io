function Nikola-New {
    param(
        [string] $slug = $(Read-Host -Prompt "slug> "),
        [string] $title = $slug,
        [string] $invalid_replace = ""
    )
    $invalid_chars = [System.IO.Path]::GetInvalidFileNameChars();
    foreach ($ic in $invalid_chars) {
        $slug = $slug.Replace($ic, ' ');
    }
    $basename = ($slug -replace " +", "-").ToLower();

    # 在控制台输入文章标题
    $titleread = (Read-Host -Prompt "title: $title> ").Trim();
    if ($titleread -ne "") {
        $title = $titleread;
    }
    $date = Get-Date -Format "yyyy-MM-dd HH:mm:ss UTCzzzz";
    # 生成头内容
    $content = @("---",
        "title: '$title'",
        "slug: '$basename'",
        "date: $date",
        "tags:",
        "category:",
        "description:",
        "type: text",
        "---",
        "",
        "文章内容",
        "",
        ".. TEASER_END");
    $content = [string]::Join("`n", $content);

    # 生成目录
    # 按 yyyy-MM 划分
    $ym = Get-Date -Format "yyyy-MM";
    if (-not (Test-Path "posts/$ym")) {
        New-Item -ItemType Directory -Path "posts/$ym";
    }
    $filename = "posts/$ym/$basename.rst";
    Out-File -Encoding utf8 -FilePath $filename -Append -InputObject $content;
}

"""提供名词缩写，可以使用 ``abbr`` 角色在单篇文档定义缩写，用 ``abbr`` 角色解析缩写。
也可以在 conf.py 配置中定义全局缩写。
"""
from typing import *

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.states import Inliner

__all__ = ("DefineAbbr", "parse_abbr")
print("WARNING: abbr module only supports HTML output.")


def singleton(fn: Callable[[], Dict[str, str]]):
    inst: Dict[str, str] = {}

    def inside():
        return inst

    return inside


@singleton
def global_abbr():
    pass


@singleton
def local_abbr():
    pass


class DefineAbbr(Directive):
    """定义一个页面有效的缩写::

        .. abbr:: abbr description

    will be rendered as :code:`<ruby><rb>abbr/rb><rt>description</rt></ruby>` by :meth:`parse_abbr`.
    """
    # 缩写
    required_arguments = 1
    # 缩写的解释
    has_content = True
    options_arguments = 0
    option_spec: Dict[str, Any] = {}

    def run(self):
        args: List[str] = self.arguments
        if len(args) < 1:
            raise ValueError("没有定义缩写")
        abbr = args[0]
        if len(self.content) < 1:
            raise ValueError("没有定义缩写的展开")
        desc = self.content[0]
        local_abbr().update({abbr: desc})
        return [nodes.raw("", "")]

def parse_abbr(
    name: str,
    rawtext: str,
    text: str,
    lineno: str,
    inliner: Inliner,
    options: dict = {},
    content: List[str] = [],
):
    abbr = text
    desc = local_abbr().get(abbr, None)
    desc = global_abbr().get(abbr, None) if desc is None else desc
    if desc is None:
        return [], [nodes.error(rawtext, nodes.paragraph(rawtext, f"没有定义的缩写 {abbr!r}"))]
    else:

        return [
            nodes.raw(rawtext, f"<ruby><rb>{abbr}</rb><rt>{desc}</rt></ruby>", format="html")
            # nodes.abbreviation(rawtext, abbr, title=desc)
        ], []

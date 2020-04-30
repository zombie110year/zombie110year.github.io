"""添加 bibliography 指令和 bibcite 角色，
提供类似于 bibtex 的参考文献解析与显示功能::

    .. bibliography:: path/to/example.bib

    在这个段落中引用 :bibtex:`example` 文献。
"""
from docutils.parsers.rst import directives, roles
from nikola.nikola import Nikola
from nikola.plugin_categories import RestExtension


class Plugin(RestExtension):
    name = "bibcite"

    def set_site(self, site: Nikola):
        self.site = site
        roles.register_canonical_role("bibcite", lambda : 0)
        directives.register_directive("bibliography", type)
        return super(Plugin, self).set_site(site)
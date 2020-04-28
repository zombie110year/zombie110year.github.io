# -*- coding: utf-8 -*-
"""便捷地引用外部链接的方式，提供角色 ``extlink`` 和指令 ``extlink``::

    .. extlink:: {{ url }}
        :title: 自定义标题

    :extlink:`{{ url }}`
"""

from typing import *

from docutils.parsers.rst import directives, roles
from nikola.nikola import Nikola
from nikola.plugin_categories import RestExtension

from .abbreviation import global_abbr, DefineAbbr, parse_abbr
from .github import GitHubGist, github_repository


class Plugin(RestExtension):
    """Plugins for zombie110year's blog"""

    name = "zomhub"

    def set_site(self, site):
        """Set Nikola site."""
        self.site: Nikola = site
        # 读取配置中的 SITE_ABBR 项
        abbr_preset = self.site.config.get("SITE_ABBR", {})
        global_abbr().update(abbr_preset)
        # 注册
        roles.register_canonical_role('github', github_repository)
        roles.register_canonical_role('abbr', parse_abbr)
        directives.register_directive('gist', GitHubGist)
        directives.register_directive('abbr', DefineAbbr)

        return super(Plugin, self).set_site(site)

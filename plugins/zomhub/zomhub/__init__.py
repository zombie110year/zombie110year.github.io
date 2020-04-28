# -*- coding: utf-8 -*-
"""便捷地引用外部链接的方式，提供角色 ``extlink`` 和指令 ``extlink``::

    .. extlink:: {{ url }}
        :title: 自定义标题

    :extlink:`{{ url }}`
"""

from typing import *

from docutils.parsers.rst import directives, roles
from nikola.plugin_categories import RestExtension

from .github import GitHubGist, github_repository


class Plugin(RestExtension):
    """Plugins for zombie110year's blog"""

    name = "zomhub"

    def set_site(self, site):
        """Set Nikola site."""
        self.site = site
        # 注册
        roles.register_canonical_role('github', github_repository)
        directives.register_directive('gist', GitHubGist)

        return super(Plugin, self).set_site(site)

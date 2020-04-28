# -*- coding: utf-8 -*-
"""github role for reStructuredText."""

from nikola.plugin_categories import RestExtension
from typing import *

from extlink import *

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

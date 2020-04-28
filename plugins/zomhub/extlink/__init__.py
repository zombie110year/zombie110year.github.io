"""便捷地引用外部链接的方式，提供角色 ``extlink`` 和指令 ``extlink``::

    .. extlink:: {{ url }}
        :title: 自定义标题

    :extlink:`{{ url }}`
"""

from .github import GitHubGist
from .github import github_repository
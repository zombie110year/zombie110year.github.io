"""提供指定为 GitHub 的链接脚本
"""

import re
from dataclasses import dataclass
from functools import lru_cache

import requests as r
from docutils import nodes
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.states import Inliner
from typing import *

__all__ = ("GitHubGist", "github_repository")

class GitHubGist(Directive):
    """Embed GitHub Gist

    Usage::

        .. gist:: ID
    """
    required_arguments = 0
    optional_arguments = 0
    option_spec: Dict[str, Any] = {}
    has_content = True

    def run(self):
        gist_id: str = self.content[0].strip()
        if gist_id.startswith("https://"):
            # 网页链接
            script_url = f"{gist_id}.js"
        elif m := re.search(r"(\S+)/([\dabcdef]+)", gist_id):
            # owner/id
            owner = m[1]
            id = m[2]
            script_url = f"https://gist.github.com/{owner}/{id}.js"
        else:
            raise self.error(f"Error: Cannot parse gist id: {gist_id!r}")

        script_el = f"<script src={script_url!r}></script>"
        return [nodes.raw("", script_el, format='html')]

def github_repository(name: str,
                      rawtext: str,
                      text: str,
                      lineno: int,
                      inliner: Inliner,
                      options: dict = {},
                      content: List[str] = []):
    """reST extension for replace :github:`zombie110year/blog-source` to
    <a href="https://github.com/zombie110year/blog-source">zombie110year/blog-source | GitHub</a>

    Usage::

        :github:`owner/repo`
    """
    owner_repo = re.search(r"(?P<owner>\S+)/(?P<repo>\S+)", text)
    if owner_repo is not None:
        owner = owner_repo["owner"]
        repo = owner_repo["repo"]
        info = check_github_repo(owner, repo)
        return [nodes.reference(rawtext, info.title, refuri=info.url, **options)], []
    else:
        return [], [f"Error: input cannot be refered to a GitHub repository."]


@dataclass
class GithubInfo:
    owner: str
    repo: str

    @property
    def url(self):
        return f"https://github.com/{self.owner}/{self.repo}"

    @property
    def title(self):
        return f"GitHub - {self.owner}/{self.repo}"


@lru_cache
def check_github_repo(owner: str, repo: str) -> GithubInfo:
    # todo: get description
    info = GithubInfo(owner=owner, repo=repo)
    return info

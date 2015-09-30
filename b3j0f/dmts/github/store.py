# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014 Jonathan Labéjof <jonathan.labejof@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------

"""Github store module in charge of storing data."""

from b3j0f.conf import Configurable
from b3j0f.dmts.rpc.store import RpcStore

from b3j0f.dmts.model import (
    Account, Label, Milestone, Project, Issue, Comment, Attachment, Group,
    Member
)

from github3 import GitHubEnterprise, GitHub


class GitHubStore(RpcStore):
    """Github store."""

    def __init__(self, repo, *args, **kwargs):
        """
        :param str repo: repository name.
        """

        super(GitHubStore, self).__init__(*args, **kwargs)

        self.repo = repo

    def connect(self):
        """Connect to the remote element with self attributes."""

        kwargs = {'url': self.url}

        if self.login is not None:
            kwargs['username'] = self.login
            kwargs['password'] = self.pwd

        if self.oauth is not None:
            kwargs['token'] = self.oauth

        self.conn = GitHubEnterprise(**kwargs)

    def get(self, _id, pids=None):

        result = None

        if issubclass(_type, Account):


        else:
            raise self.Error('Wrong type {0}.'.format(_type))

        return result

    def find(
            self,
            names=None, descs=None, created=None, updated=None, _type=None,
            **kwargs
    ):

        result = []

        if _type is None:
            _type = (
                Account, Label, Milestone, Project, Issue, Comment, Group,
                Member
            )

        for typ in _type:

            if issubclass(typ, Label):

            else:
                raise JiraStore.Error('Unknown type {0}'.format(typ))

        return result

    def _addelt(self, elt):

        result = elt

        if isinstance(elt, Issue):
            self.conn.create_issue(
                owner=elt.owner, repository=self.repo, title=elt.name,
                assignee=elt.assignee, body=elt.content,
                milestone=elt.milestone, labels=elt.labels
            )

        else:
            raise self.Error('Wrong type {0}.'.format(elt))

        return result

    def _updateelt(self, elt, old, upsert):

        result = elt

        if isinstance(elt, Account):


        else:
            raise self.Error('Wrong type {0}'.format(elt))

        return result

    def _delelt(self, elt):

        result = elt

        if isinstance(elt, Account):


        else:
            raise self.Error('Wrong type {0}'.format(elt))

        return result

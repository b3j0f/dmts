# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2015 Jonathan Labéjof <jonathan.labejof@gmail.com>
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

"""GitLab comment accessor module."""

__all__ = ['CommentAccessor']

from .base import GitLabAccessor

from ...model.comment import Comment


class CommentAccessor(GitLabAccessor):
    """Comment accessor."""

    __datatype__ = Comment
    __scopes__ = ['projects', 'issues', 'comments']

    def sdata2data(self, sdata):
        """Convert a sdata to a comment."""

        result = self.create(
            project=self.store.get(  # comment fields
                accessor='projects', _id=sdata['project_id']
            ),
            issue=self.store.get(
                accessor='issues', _id=sdata['issue_id']
            ),
            content=sdata['body'],
            attachment=sdata['attachment'],
            owner=self.store.sdata2data(  # element fields
                accessor='accounts', sdata=sdata['author']
            ),
            _id=sdata['id'],  # Data fields
            created=sdata['created_at'],  # TODO: format to a datetime
            updated=sdata.get('updated_at')  # TODO: format to a datetime
        )

        return result

    def find(self, pids=None, **kwargs):

        result = []

        if pids is None:
            projects = self.store._processquery(scopes='projects')
            for project in projects:
                comments = self.find(pids=[project['id']], **kwargs)
                result += comments

        elif len(pids) == 1:
            issues = self.store._processquery(
                scopes=['projects', 'issues'], pids=[pids[0]]
            )
            for issue in issues:
                comments = self.find(pids=[pids[0], issue['id']], **kwargs)
                result += comments

        else:
            comments = self.store._processquery(
                scopes=['projects', 'issues', 'notes'], pids=pids
            )
            if comments:
                result = map(self.sdata2data, result)

        # TODO : check kwargs

        return result

    def _filladdkwargs(self, data, kwargs):

        kwargs['body'] = data.content

    def _fillupdatekwargs(self, data, old, kwargs):

        self._filladdkwargs(data=data, kwargs=kwargs)

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

from b3j0f.sync import Accessor
from b3j0f.dmts.model.comment import Comment


class CommentAccessor(Accessor):
    """Comment accessor."""

    __datatype__ = Comment

    def _responsetodata(self, response):
        """Convert a response to a comment."""

        result = self.create(
            project=self.store.get(  # comment fields
                accessor='projects', _id=response['project_id']
            ),
            issue=self.store.get(
                accessor='issues', _id=response['issue_id']
            ),
            content=response['body'],
            attachment=response['attachment'],
            owner=self.store.get(  # element fields
                accessor='accounts', _id=response['author']['id']
            ),
            _id=response['id'],  # Data fields
            created=response['created_at'],  # TODO: format to a datetime
            updated=response.get('updated_at')  # TODO: format to a datetime
        )

        return result

    def get(self, _id, pids, globalid=None):

        response = self.store._processquery(
            scopes=['projects', 'issues', 'notes'], _id=_id, pids=pids
        )

        result = self._responsetodata(response=response)

        return result

    def find(self, pids=None, **kwargs):

        result = []

        if pids is None:
            projects = self._processquery(scopes='projects')
            for project in projects:
                issues = self._processquery(
                    scopes=['projects', 'issues'], pids=project['id']
                )
                comments = self.find(pids=project['id'], **kwargs)
                result += comments

        elif len(pids) == 1:
            issues = self._processquery(
                scopes=['projects', 'issues'], pids=pids[0]
            )
            for issue in issues:
                comments = self.find(pids=[pids[0], issue['id']], **kwargs)
                result += comments

        else:
            comments = self._processquery(
                scopes=['projects', 'issues', 'notes'], pids=pids
            )
            result = map(self._responsetodata, result)

        # TODO : check kwargs

        return result

    def _add(self, data):

        response = self.store._processquery(
            verb='post', scopes=['projects', 'issues', 'notes'],
            pids=data.pids, body=data.content
        )

        result = self._responsetodata(response)

        return result

    def _update(self, data, old):

        response = self.store._processquery(
            verb='put', scopes=['projects', 'issues', 'notes'],
            pids=data.pids, _id=data._id, body=data.content
        )

        result = self.store._responsetodata(response=response)

        return result

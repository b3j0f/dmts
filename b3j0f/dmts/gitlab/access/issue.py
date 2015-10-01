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

"""GitLab issue accessor module."""

__all__ = ['IssueAccessor']

from b3j0f.sync import Accessor

from ...model.issue import Issue


class IssueAccessor(Accessor):
    """Issue accessor."""

    __datatype__ = Issue

    def _responsetodata(self, response):
        """Convert a response to a issue."""

        result = self.create(
            project=response['project_id'],  # issue fields
            labels=response['labels'],
            assignee=response['assignee'],
            milestone=response['milestone'],
            state=response['state'],
            owner=response['author']['username'],
            _id=response['id'],  # Data fields
            name=response['title'],  # element fields
            pnames=self.store.get(
                accessor='projects', _id=response['project']
            ),
            description=response['description'],
            created=response['created_at'],  # TODO: format to a datetime
            updated=response.get('updated_at')  # TODO: format to a datetime
        )

        return result

    def get(self, _id, pids=None, globalid=None):

        response = None

        if pids is None:  # find globaly an issue
            issues = self.store._processquery(scopes='issues')
            for issue in issues:
                if issue['id'] == _id:
                    response = issue
                    break

        else:
            response = self.store._processquery(
                scopes=['projects', 'issues'], _id=_id, pids=pids
            )

        result = self._responsetodata(response=response)

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        result = None

        issues = self.store._processquery(scopes='issues')
        for issue in issues:
            if issue['title'] == name and pnames == issue.pnames:
                result = issue
                break

        return result

    def find(self, name=None, pids=None, **kwargs):

        result = []

        if pids:
            if name:
                kwargs['title'] = name
            response = self.store._processquery(
                scopes=['projects', 'issues'], pids=pids, **kwargs
            )
            result = map(self._responsetodata, response)

        else:
            issues = map(
                self._responsetodata, self._processquery(scopes='issues')
            )
            kwargs['name'] = name
            for issue in issues:
                for key in kwargs:
                    value = kwargs[key]
                    if value is not None and getattr(issue, key) == value:
                        result.append(issue)

        return result

    def _add(self, data):

        response = self.store._processquery(
            verb='post', scopes=['projects', 'issues'], pids=data.pids,
            title=data.name,
            description=data.description, assignee_id=data.assignee,
            milestone_id=data.milestone, labels=data.labels
        )

        result = self._responsetodata(response)

        return result

    def _update(self, data, old):

        response = self.store._processquery(
            verb='put', scopes=['projects', 'issues'], pids=data.pids,
            _id=data._id, title=data.name, description=data.description,
            assignee_id=data.assignee, milestone_id=data.milestone,
            labels=data.labels, state_event=data.state
        )

        result = self._responsetodata(response=response)

        return result

    def _remove(self, data):

        # close issue instead of deleting it (deprecated)
        data.state = 'close'
        self._update(data)

        return data

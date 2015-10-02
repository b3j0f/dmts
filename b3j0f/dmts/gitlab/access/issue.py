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

from .base import GitLabAccessor

from ...model.issue import Issue


class IssueAccessor(GitLabAccessor):
    """Issue accessor."""

    __datatype__ = Issue
    __scopes__ = 'projects'

    def sdata2data(self, sdata):
        """Convert a sdata to a issue."""

        result = self.create(  # issue fields
            project=self.store.get(
                accessor='projects', _id=sdata['project_id']
            ),
            labels=map(
                lambda _id:
                self.store.sdata2data(accessor='labels', sdata=_id),
                sdata['labels']
            ) if sdata.get('labels') else [],
            assignee=self.store.get(
                accessor='accounts', _id=sdata['assignee']
            ),
            milestone=self.store.get(
                accessor='accounts', _id=sdata['milestone']
            ),
            state=sdata['state'],
            owner=self.store.get(
                accessor='accounts', _id=sdata['author']
            ),
            _id=sdata['id'],  # Data fields
            name=sdata['title'],  # element fields
            description=sdata['description'],
            created=sdata['created_at'],  # TODO: format to a datetime
            updated=sdata.get('updated_at')  # TODO: format to a datetime
        )

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        result = None

        issues = self.store._processquery(scopes='issues')
        for issue in issues:
            if issue['title'] == name and pnames == issue.pnames:
                result = self.sdata2data(sdata=issue)
                break

        return result

    def find(self, name=None, pids=None, **kwargs):

        result = []

        if pids:
            if name:
                kwargs['title'] = name
            response = self.store._processquery(
                scopes=self.__scopes__, pids=pids, **kwargs
            )
            if response:
                result = map(self.sdata2data, response)

        else:
            issues = map(
                self.sdata2data, self.store._processquery(scopes='issues')
            )
            kwargs['name'] = name
            for issue in issues:
                for key in kwargs:
                    value = kwargs[key]
                    if value is not None and getattr(issue, key) == value:
                        result.append(issue)

        return result

    def _filladdkwargs(self, data, kwargs):

        kwargs.update({
            'title': data.name,
            'description': data.description,
            'assignee_id': data.assignee._id,
            'milestone_id': data.milestone._id,
            'labels':
                map(lambda data: data._id, data.labels) if data.labels else []
        })

    def _fillupdatekwargs(self, data, old, kwargs):

        self._filladdkwargs(data=data, kwargs=kwargs)

        kwargs['state_event'] = data.state

    def _remove(self, data):

        # close issue instead of deleting it (deprecated)
        data.state = 'close'
        self._update(data)

        return data

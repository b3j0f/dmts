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

"""GitLab milestone accessor module."""

__all__ = ['MilestoneAccessor']

from .base import GitLabAccessor

from ...model.milestone import Milestone


class MilestoneAccessor(GitLabAccessor):
    """Milestone accessor."""

    __datatype__ = Milestone
    __scopes__ = ['projects', 'milestones']

    def sdata2data(self, sdata):
        """Convert a sdata to a milestone."""

        result = self.create(
            # milestones fields
            duedate=sdata['duedate'],  # TODO; convert to datetime
            state=sdata['state'],
            project=self.store.get(
                accessor='projects', _id=sdata['project_id']
            ),
            _id=sdata['id'],  # Data fields
            name=sdata['title'],
            description=sdata['description'],
            created=sdata['created_at'],
            updated=sdata.get('updated_at')
        )

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        return self.get(_id=name, pids=pnames, globalid=globalname)

    def find(self, name=None, _id=None, pids=None, **kwargs):

        if name is None:
            name = _id

        result = []

        if pids:
            response = self.store._processquery(
                scopes=['projects', 'milestones'], pids=pids
            )
            if response:
                result = map(self.sdata2data, response)

        else:
            projects = self.store._processquery(scopes='projects')
            for project in projects:
                milestones = self.find(pids=project['id'], name=name, **kwargs)
                result += milestones

        # TODO: check kwargs

        return result

    def _filladdkwargs(self, data, kwargs):

        kwargs.update({
            'title': data.name, 'description': data.description,
            'due_date': data.duedate
        })

    def _fillupdatekwargs(self, data, old, kwargs):

        self._filladdkwargs(data=data, kwargs=kwargs)

        kwargs['state_event'] = data.state

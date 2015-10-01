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

"""GitLab project accessor module."""

__all__ = ['ProjectAccessor']

from b3j0f.sync import Accessor

from .base import GitLabAccessor
from ...model.project import Project


class ProjectAccessor(GitLabAccessor):
    """Project accessor."""

    __datatype__ = Project

    __scopes__ = 'projects'

    def sdata2data(self, sdata):
        """Convert a response to a project."""

        result = self.create(
            avatar=sdata['avatar_url'],  # project fields
            public=sdata['public'],
            url=sdata['web_url'],  # item fields
            owner=self.store.sdata2data(
                accessor='accounts', sdata=sdata['owner']
            ) if 'owner' in sdata else None,
            archived=sdata['archived'],
            tags=sdata['tag_list'],
            _id=sdata['id'],  # Data fields
            name=sdata['name'],  # element fields
            description=sdata['description'],
            created=sdata['created_at'],  # TODO: format to a datetime
            updated=sdata.get('updated_at')  # TODO: format to a datetime
        )

        return result

    def getbyname(self, name, **_):

        response = self.store._processquery(scopes='projects/search', _id=name)

        if response:
            result = self.sdata2data(sdata=response[0])

        else:
            result = None

        return result

    def find(self, name=None, **kwargs):

        if name:
            kwargs = {'_id': name}

        elif kwargs:
            kwargs = {'search': kwargs}

        result = super(ProjectAccessor, self).find(**kwargs)

        return result

    def _addkwargs(self, data):

        result = {
            'name': data.name,
            'description': data.description,
            'public': data.public
        }

        if data.owner is None:
            result['scopes'] = 'projects'

        else:
            result['scopes'] = 'projects/user/{0}'.format(data.owner._id)

        return result

    def _updatekwargs(self, data, old):

        result = {
            '_id': data._id, 'name': data.name, 'public': data.public,
            'description': data.description
        }

        return result

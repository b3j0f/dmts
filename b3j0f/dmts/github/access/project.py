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

from b3j0f.sync import Accessor
from b3j0f.dmts.model.project import Project


class ProjectAccessor(Accessor):
    """Project accessor."""

    __datatype__ = Project

    def _responsetodata(self, response):
        """Convert a response to a project."""

        result = self.create(
            avatar=response['avatar_url'],  # project fields
            public=response['public'],
            state=response['state'],
            url=response['web_url'],  # item fields
            owner=response['owner']['username'],
            archived=response['archived'],
            tags=response['tag_list'],
            _id=response['id'],  # Data fields
            name=response['name'],  # element fields
            description=response['description'],
            created=response['created_at'],  # TODO: format to a datetime
            updated=response.get('updated_at')  # TODO: format to a datetime
        )

        return result

    def get(self, _id, pids=None, globalid=None):

        response = self.store._processquery(scopes='projects', _id=_id)

        result = self._responsetodata(response=response)

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        response = self.store._processquery(
            scopes='projects/search', _id=name
        )

        if response:
            result = self._responsetodata(response=response[0])

        else:
            result = None

        return result

    def find(self, name=None, **kwargs):

        if name:
            response = self.store._processquery(
                scopes='projects', _id=kwargs['name']
            )

        else:
            response = self.store._processquery(
                scopes='projects', search=kwargs
            )

        result = map(self._responsetodata, response)

        return result

    def _add(self, data):

        if data.owner is None:
            scopes = 'projects'

        else:
            scopes = 'projects/user/{0}'.format(data.owner)

        response = self.store._processquery(
            verb='post', scopes=scopes, name=data.name,
            description=data.description, public=data.public
        )

        result = self._responsetodata(response)

        return result

    def _update(self, data, old):

        response = self.store._processquery(
            verb='put', scopes='projects', _id=data._id,
            name=data.name, description=data.description, public=data.public
        )

        result = self._responsetodata(response=response)

        return result

    def _remove(self, data):

        self._processquery(
            verb='delete', scopes='projects', _id=data._id
        )

        return data

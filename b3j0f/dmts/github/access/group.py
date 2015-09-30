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

"""GitLab group accessor module."""

from b3j0f.sync import Accessor
from b3j0f.dmts.model.group import Group


class GroupAccessor(Accessor):
    """Group accessor."""

    __datatype__ = Group

    def _responsetodata(self, response):
        """Convert a response to a group."""

        result = self.create(
            path=response['path'],  # group fields
            _id=response['name'],  # Data fields
            name=response['name'],
            description=response['description']
        )

        return result

    def get(self, _id, pids=None, globalid=None):

        response = self.store._processquery(scopes='groups', _id=_id)

        result = self._responsetodata(response=response)

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        return self.get(_id=name, pids=pnames, globalid=globalname)

    def find(self, name=None, **kwargs):

        if name:
            response = self._processquery(scopes='groups', search=name)

        else:

            response = self._processquery(scopes='groups')

        result = []

        for resp in response:
            for key in kwargs:
                value = kwargs[key]
                if value is not None and resp.get(key) == value:
                    group = self._responsetodata(resp)
                    result.append(group)

        return result

    def _add(self, data):

        response = self.store._processquery(
            verb='post', scopes='groups', name=data.name,
            description=data.description, path=data.path
        )

        result = self._responsetodata(response)

        return result

    def _remove(self, data):

        self._processquery(
            verb='delete', scopes='groups', _id=data._id
        )

        return data

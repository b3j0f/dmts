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

"""GitLab label accessor module."""

from b3j0f.sync import Accessor
from b3j0f.dmts.model.label import Label


class LabelAccessor(Accessor):
    """Label accessor."""

    __datatype__ = Label

    def _responsetoproject(self, response):
        """Convert a response to a label."""

        result = self.create(
            color=response['color'],  # label fields
            _id=response['name'],  # Data fields
            name=response['name'],  # element fields
        )

        return result

    def get(self, _id, pids=None, globalid=None):

        response = self.store._processquery(
            scopes=['projects', 'labels'], _id=_id, pids=pids
        )

        result = self._responsetoproject(response=response)

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        return self.get(_id=name, pids=pnames, globalid=globalname)

    def find(self, name=None, _id=None, pids=None, **kwargs):

        if name is None:
            name = _id

        result = []

        if pids:
            response = self._processquery(
                scopes=['projects', 'labels'], pids=pids
            )
            result = map(self._responsetoproject, response)

        else:
            projects = self._processquery(scopes='projects')
            for project in projects:
                labels = self.find(pids=project['id'], name=name, **kwargs)
                result += labels

        # TODO: check kwargs

        return result

    def _add(self, data):

        response = self.store._processquery(
            operation='post', scopes=['projects', 'labels'], pids=data.pids,
            name=data.name, color=data.color
        )

        result = self._responsetoproject(response)

        return result

    def _update(self, data, old):

        response = self.store._processquery(
            operation='put', scopes=['projects', 'labels'], pids=data.pids,
            name=data.name, color=data.color, new_name=old.name
        )

        result = self._responsetoproject(response=response)

        return result

    def _remove(self, data):

        self._processquery(
            operation='delete', scopes=['projects', 'labels'], pids=data.pids,
            name=data.name,
        )

        return data

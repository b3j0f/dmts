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

__all__ = ['GitLabAccessor']

from b3j0f.utils.iterable import first

from b3j0f.sync import Accessor, getidwpids

from ...http.store import HTTPStore


class GitLabAccessor(Accessor):
    """GitLab accessor."""

    __scopes__ = None

    def get(self, _id, pids=None, globalid=None):

        result = None

        if globalid is not None:
            _id, pids = getidwpids(globalid)

        try:
            response = self.store._processquery(
                scopes=self.__scopes__, _id=_id, pids=pids
            )
        except HTTPStore.Error:
            pass
        else:
            if response is not None:
                result = self.sdata2data(response=response)

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        result = None

        response = self.find(name=name)

        if response:
            response = first(response)
            result = self.sdata2data(response=response)

        return result

    def find(self, scopes=None, **kwargs):

        result = []

        if scopes is None:
            scopes = self.__scopes__

        response = self.store._processquery(scopes=scopes, **kwargs)

        if response:
            result = map(self.sdata2data, response)

        return result

    def _add(self, data):

        kwargs = self._addkwargs(data)

        response = self.store._processquery(method=HTTPStore.POST, **kwargs)

        result = self.sdata2data(response)

        return result

    def _addkwargs(data):
        """Method to override in order to specify self._add kwargs."""

        raise NotImplementedError()

    def _update(self, data, old):

        kwargs = self._updatekwargs(data=data, old=old)

        response = self.store._processquery(method=HTTPStore.PUT, **kwargs)

        result = self.sdata2data(response=response)

        return result

    def _updatekwargs(data, old):
        """Method to override in order to specify self._update kwargs."""

        raise NotImplementedError()

    def _remove(self, data):

        kwargs = self._removekwargs(data=data)

        result = self.store._processquery(method=HTTPStore.DELETE, **kwargs)

        if isinstance(result, dict):
            result = self.sdata2data(sdata=result)

        else:
            result = data

        return data

    def _removekwargs(self, data):
        """Method to override in order to specify self._remove kwargs."""

        result = {
            '_id': data._id,
            'pids': data.pids,
            'scopes': self.__scopes__
        }

        return result

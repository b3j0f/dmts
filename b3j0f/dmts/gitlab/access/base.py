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

        sdata = None

        try:
            sdata = self.store._processquery(
                scopes=self.__scopes__, _id=_id, pids=pids
            )

        except HTTPStore.Error:
            # try a global research
            if pids is not None:
                scope = self.__scopes__[-1]
                try:
                    sdata = self.store._processquery(scopes=scope)
                except HTTPStore.Error:
                    pass
                else:
                    if sdata:
                        for sdata in sdata:
                            if sdata['id'] == _id:
                                sdata = sdata
                                break

        if sdata is not None:
            result = self.sdata2data(sdata=sdata)

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        result = None

        sdata = self.find(name=name)

        if sdata:
            sdata = first(sdata)
            result = self.sdata2data(sdata=sdata)

        return result

    def find(self, scopes=None, **kwargs):

        result = []

        if scopes is None:
            scopes = self.__scopes__

        sdata = self.store._processquery(scopes=scopes, **kwargs)

        if sdata:
            result = map(self.sdata2data, sdata)

        return result

    def _add(self, data):

        kwargs = {'scopes': self.__scopes__, 'pids': data.pids}

        self._filladdkwargs(data, kwargs)

        sdata = self.store._processquery(method=HTTPStore.POST, **kwargs)

        result = self.sdata2data(sdata=sdata)

        return result

    def _filladdkwargs(self, data, kwargs):
        """Method to override in order to update self._add kwargs."""

        raise NotImplementedError()

    def _update(self, data, old):

        kwargs = {
            'scopes': self.__scopes__, '_id': data._id, 'pids': data.pids
        }

        self._fillupdatekwargs(data=data, old=old, kwargs=kwargs)

        sdata = self.store._processquery(method=HTTPStore.PUT, **kwargs)

        result = self.sdata2data(sdata=sdata)

        return result

    def _fillupdatekwargs(self, data, old, kwargs):
        """Method to override in order to specify self._update kwargs."""

        raise NotImplementedError()

    def _remove(self, data):

        kwargs = {
            '_id': data._id, 'pids': data.pids, 'scopes': self.__scopes__
        }
        self._fillremovekwargs(data=data, kwargs=kwargs)

        result = self.store._processquery(method=HTTPStore.DELETE, **kwargs)

        if isinstance(result, dict):
            result = self.sdata2data(sdata=result)

        else:
            result = data

        return data

    def _fillremovekwargs(self, data, kwargs):
        """Method to override in order to specify self._remove kwargs."""

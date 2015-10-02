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

__all__ = ['LabelAccessor']

from .base import GitLabAccessor

from ...model.label import Label


class LabelAccessor(GitLabAccessor):
    """Label accessor."""

    __datatype__ = Label
    __scopes__ = ['projects', 'labels']

    def sdata2data(self, sdata):
        """Convert a sdata to a label."""

        if isinstance(sdata, dict):

            result = self.create(
                color=sdata['color'],  # label fields
                _id=sdata['name']  # Data fields
            )

        else:
            result = self.create(_id=sdata)

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        return self.get(_id=name, pids=pnames, globalid=globalname)

    def find(self, name=None, _id=None, pids=None, **kwargs):

        if name is None:
            name = _id

        result = []

        if pids:
            sdata = self.store._processquery(
                scopes=self.__scopes__, pids=pids
            )
            if sdata:
                result = map(self.sdata2data, sdata)

        else:
            projects = self.store._processquery(scopes='projects')
            for project in projects:
                labels = self.find(pids=project['id'], name=name, **kwargs)
                result += labels

        # TODO: check kwargs

        return result

    def _filladdkwargs(self, data, kwargs):

        kwargs.update({
            'name': data.name, 'color': data.color
        })

    def _fillupdatekwargs(self, data, old, kwargs):

        self._filladdkwargs(data=data, kwargs=kwargs)

        kwargs['name'] = old.name
        kwargs['new_name'] = data.name

    def _fillremovekwargs(self, data, kwargs):

        kwargs['name'] = data.name

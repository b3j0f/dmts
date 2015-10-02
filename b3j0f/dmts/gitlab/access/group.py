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

__all__ = ['GroupAccessor']

from .base import GitLabAccessor

from ...model.group import Group


class GroupAccessor(GitLabAccessor):
    """Group accessor."""

    __datatype__ = Group
    __scopes__ ='groups'

    def sdata2data(self, sdata):
        """Convert a sdata to a group."""

        result = self.create(
            path=sdata['path'],  # group fields
            _id=sdata['name'],  # Data fields
            description=sdata['description']
        )

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        return self.get(_id=name, pids=pnames, globalid=globalname)

    def find(self, name=None, **kwargs):

        if name:
            sdata = self.store._processquery(
                scopes=self.__scopes__, search=name
            )

        else:
            sdata = self.store._processquery(scopes=self.__scopes__)

        result = []

        for resp in sdata:
            for key in kwargs:
                value = kwargs[key]
                if value is not None and resp.get(key) == value:
                    group = self.sdata2data(resp)
                    result.append(group)

        return result

    def _filladdkwargs(self, data, kwargs):

        kwargs.update({
            'name': data.name, 'description': data.description,
            'path': data.path
        })

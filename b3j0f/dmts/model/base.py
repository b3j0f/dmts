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

"""Module of model base classes.

Contains abstract classes used to design all data useful in development
management projects.
"""

from b3j0f.sync import Data, datafields


@datafields('owner')
class Element(Data):

    def __init__(self, owner, *args, **kwargs):
        """
        :param Account owner: owner id.
        """

        super(Element, self).__init__(*args, **kwargs)

        self._owner = owner


@datafields('project')
class ProjectElement(Data):

    def __init__(self, project, *args, **kwargs):
        """
        :param Project project: project.
        """

        super(ProjectElement, self).__init__(*args, **kwargs)

        self._project = project

    def _pids(self):

        return self.project._id

    def _pnames(self):

        return self.project.name


@datafields('url', 'archived', 'tags')
class Item(Element):
    """Development management tool item."""

    class Error(Exception):
        """Handle item errors."""

    def __init__(
        self, url=None, owner=None, archived=False, tags=None, **kwargs
    ):
        """
        :param str url: item url.
        :param bool archived: item archiving state.
        :param list tags: item tags.
        """

        super(Item, self).__init__(**kwargs)

        self._url = url
        self._archived = archived
        self._tags = tags

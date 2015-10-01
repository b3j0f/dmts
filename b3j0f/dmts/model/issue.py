# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014 Jonathan Labéjof <jonathan.labejof@gmail.com>
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

"""Issue module."""

from .base import Item

from b3j0f.sync import datafields


@datafields('project', 'labels', 'assignee', 'parent', 'milestone', 'state')
class Issue(Item):
    """Embed issue information."""

    def __init__(
            self, project=None, labels=None, assignee=None,
            parent=None, milestone=None, state=None, *args, **kwargs
    ):
        """
        :param Project project: parent project.
        :param list labels: label names.
        :param str assignee: issue assignee.
        :param Issue parent: parent issue.
        :param str milestone: issue milestone.
        :param str state: issue state.
        """

        super(Issue, self).__init__(*args, **kwargs)

        self._project = project
        self._pids = [project]
        self._labels = labels
        self._assignee = assignee
        self._parent = parent
        self._milestone = milestone
        self._state = state

    def _pids(self):

        return self.project._id

    def _pnames(self):

        return self.project.name

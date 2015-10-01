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

from .base import Element
from b3j0f.sync import datafields


@datafields('project', 'issue', 'content', 'attachment')
class Comment(Element):
    """Embed issue information."""

    def __init__(
            self,
            project, issue, content=None, account=None, attachment=None,
            **kwargs
    ):
        """
        :param Project project: parent project.
        :param Issue issue: parent issue.
        :param str content: content.
        :param str attachment: attachment.
        """

        super(Comment, self).__init__(**kwargs)

        self._project = project
        self._issue = issue
        self._content = content
        self._attachment = attachment

    def _pids(self):

        return self.project._id, self.issue._id

    def _pnames(self):

        return self.project.name, self.issue.name


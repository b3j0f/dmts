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

"""Resource module in charge of storing data."""

from b3j0f.conf import Configurable
from b3j0f.dmts.rpc.resource import RpcResource

from b3j0f.dmts.model import (
    Account, Label, Milestone, Project, Issue, Comment, Attachment
)

from jira import JIRA


class JiraResource(RpcResource):
    """Jira resource."""

    def connect(self):
        """Connect to the remote element with self attributes."""

        kwargs = {'server': self.url}

        if self.login is not None:
            kwargs['basic_auth'] = (self.login, self.pwd)

        if self.oauth is not None:
            kwargs['oauth'] = self.oauth

        self.conn = JIRA(**kwargs)

    def getelement(self, _id, _type, pid=None):
        """Get item by id and type.

        :param int _id: item id.
        :param type _type: item type. Subclass of Element
        :return: element which corresponds to input _id and _type.
        :rtype: Element
        """

        result = None

        if issubclass(_type, Account):
            jirauser = self.conn.user(id=_id, expand=True)
            result = Account(**jirauser)

        elif issubclass(_type, Issue):
            jiraissue = self.conn.issue(id=_id, fields=issue)
            result = Issue(**jiraissue)

        elif issubclass(_type, Project):
            jiraproject = self.conn.project(id=_id)
            result = Project(**jiraproject)

        elif issubclass(_type, Label):
            issuetype = self.conn.issue_type(id=_id)
            result = Label(**issuetype)

        elif issubclass(_type, Comment):
            comment = self.conn.comment(issue=pid, comment=_id)
            result = Comment(**comment)

        elif issubclass(_type, Attachment):
            attachment = self.conn.attachment(id=_id)
            result = Attachment(**attachment)

        else:
            raise self.Error('Wrong type {0}.'.format(_type))

        return result

    def findelements(
            self,
            names=None, descs=None, created=None, updated=None,
            _type=(Account, Label, Milestone, Project, Issue),
            **kwargs
    ):
        """Get a list of elements matching with input parameters.

        :param list names: element names to retrieve. If None, get all
            elements.
        :param list descs: list of regex to find in element description.
        :param datetime created: starting creation time.
        :param datetime updated: starting updated time.
        :param dict kwargs: additional elemnt properties to select.
        :param list _type: element classes to retrieve. Subclass of Element.
        :return: list of Elements.
        :rtype: list
        """

        result = []

        if _type is None:
            _type = (Account, Label, Milestone, Project, Issue)

        for typ in _type:
            if issubclass(typ, Project):
                projects = self.conn.projects()
                for project in projects:
                    pro = Project(**project)
                    result.append(pro)

            elif issubclass(typ, Issue):
                issues = self.conn.searchissues()
                for issue in issues:
                    iss = Issue(**issue)
                    result.append(iss)

            elif issubclass(typ, Account):
                accounts = self.conn.search_users()
                for account in accounts:
                    acc = Account(**account)
                    result.append(acc)

            elif issubclass(typ, Label):
                issuetypes = self.conn.issue_types()
                for issuetype in issuetypes:
                    label = Label(**issuetype)
                    result.append(label)

            elif issubclass(typ, Comment):
                for name in names:
                    jiracomments = self.conn.comments(issue=name)
                    for jiracomment in jiracomments:
                        comment = Comment(**jiracomment)
                        result.append(comment)

            else:
                raise JiraResource.Error('Unknown type {0}'.format(typ))

        return result

    def _addelement(self, element):
        """Method to override in order to add the input element.

        This method is called by the public method ``addelement``.

        :param Element element: element to add.
        :return: added element.
        :rtype: Element
        :raises: Resource.Error if element already exists or information are
            missing.
        """

        result = element

        if isinstance(element, Project):
            self.conn.create_project(
                key=element.name[0:3].upper(), name=element.name,
                assignee=element.owner
            )

        elif isinstance(element, Account):
            self.conn.add_user(
                username=element.name, email=element.email,
                password=element.pwd, fullname=element.fullname
            )

        elif isinstance(element, Comment):
            self.conn.add_comment(issue=element.issue, body=element.content)

        elif isinstance(element, Issue):
            self.conn.create_issue(fields=element)

        elif isinstance(element, Attachment):
            self.conn.add_attachment(
                issue=element.issue, attachment=element.content,
                filename=element.filename
            )

        else:
            raise self.Error('Wrong type {0}.'.format(element))

        return result

    def _updateelement(self, element, old, upsert):
        """Method to override in order to update the input element.

        This method is called by the public method ``updateelement``.

        :param Element element: element to update.
        :param bool upsert: add the element if it does not exists.
        :raises: Resource.Error if element does not exist.
        """

        result = element

        if isinstance(element, Account):
            self.conn.add_user(
                username=element.name, email=element.email,
                password=element.pwd, fullname=element.fullname
            )
            if old is not None:
                if old.name != element.name:
                    self.conn.rename_user(
                        old_user=old.name, new_user=element.name
                    )
                if old.avatar != element.avatar:
                    self.conn.set_user_avatar(
                        username=element.name, avatar=element.avatar
                    )

        elif isinstance(element, Project):
            self.conn.create_project(
                key=self.pid(element), name=element.name,
                assignee=element.owner
            )

        elif isinstance(element, Comment):
            self.conn.add_comment(issue=element.issue, body=element.content)

        elif isinstance(element, Issue):
            self.conn.assign_issue(
                issue=element.name, assignee=element.assignee
            )

        else:
            raise self.Error('Wrong type {0}'.format(element))

        return result

    def _delelement(self, element):
        """Method to override in order to delete the input element.

        This method is called by the public method ``delelement``.

        :param Project element: element to delete.
        :return: deleted element.
        :rtype: Element
        :raises: Resource.Error if element does not exist.
        """

        result = element

        if isinstance(element, Account):
            self.conn.delete_user(username=element.name)

        elif isinstance(element, Project):
            self.conn.delete_project(pid=self.pid(element))

        else:
            raise self.Error('Wrong type {0}'.format(element))

        return result

    @staticmethod
    def pid(project):
        """Get project pid.

        :return: first 3 characters in upper cases.
        :rtype: str
        """

        return project.name[:2].upper()

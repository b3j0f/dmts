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

"""Store module in charge of storing data."""

from b3j0f.conf import conf_paths
from b3j0f.dmts.rpc.store import RpcStore

from b3j0f.dmts.model import (
    Account, Label, Milestone, Project, Issue, Comment, Attachment
)

from jira import JIRA


@conf_paths('jirastore.conf')
class JiraStore(RpcStore):
    """Jira store."""

    def connect(self):
        """Connect to the remote data with self attributes."""

        kwargs = {'server': self.url}

        if self.login is not None:
            kwargs['basic_auth'] = (self.login, self.pwd)

        if self.oauth is not None:
            kwargs['oauth'] = self.oauth

        self.conn = JIRA(**kwargs)

    def get(self, _id, _type, pid=None):
        """Get item by id and type.

        :param int _id: item id.
        :param type _type: item type. Subclass of Element
        :return: data which corresponds to input _id and _type.
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

    def find(
            self,
            names=None, descs=None, created=None, updated=None,
            _type=(Account, Label, Milestone, Project, Issue),
            **kwargs
    ):
        """Get a list of elements matching with input parameters.

        :param list names: data names to retrieve. If None, get all
            elements.
        :param list descs: list of regex to find in data description.
        :param datetime created: starting creation time.
        :param datetime updated: starting updated time.
        :param dict kwargs: additional elemnt properties to select.
        :param list _type: data classes to retrieve. Subclass of Element.
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
                raise JiraStore.Error('Unknown type {0}'.format(typ))

        return result

    def _add(self, data):
        """Method to override in order to add the input data.

        This method is called by the public method ``addelement``.

        :param Element data: data to add.
        :return: added data.
        :rtype: Element
        :raises: Store.Error if data already exists or information are
            missing.
        """

        result = data

        if isinstance(data, Project):
            self.conn.create_project(
                key=data.name[0:3].upper(), name=data.name,
                assignee=data.owner
            )

        elif isinstance(data, Account):
            self.conn.add_user(
                username=data.name, email=data.email,
                password=data.pwd, fullname=data.fullname
            )

        elif isinstance(data, Comment):
            self.conn.add_comment(issue=data.issue, body=data.content)

        elif isinstance(data, Issue):
            self.conn.create_issue(fields=data)

        elif isinstance(data, Attachment):
            self.conn.add_attachment(
                issue=data.issue, attachment=data.content,
                filename=data.filename
            )

        else:
            raise self.Error('Wrong type {0}.'.format(data))

        return result

    def _update(self, data, old, upsert):
        """Method to override in order to update the input data.

        This method is called by the public method ``updateelement``.

        :param Element data: data to update.
        :param bool upsert: add the data if it does not exists.
        :raises: Store.Error if data does not exist.
        """

        result = data

        if isinstance(data, Account):
            self.conn.add_user(
                username=data.name, email=data.email,
                password=data.pwd, fullname=data.fullname
            )
            if old is not None:
                if old.name != data.name:
                    self.conn.rename_user(
                        old_user=old.name, new_user=data.name
                    )
                if old.avatar != data.avatar:
                    self.conn.set_user_avatar(
                        username=data.name, avatar=data.avatar
                    )

        elif isinstance(data, Project):
            self.conn.create_project(
                key=self.pid(data), name=data.name,
                assignee=data.owner
            )

        elif isinstance(data, Comment):
            self.conn.add_comment(issue=data.issue, body=data.content)

        elif isinstance(data, Issue):
            self.conn.assign_issue(
                issue=data.name, assignee=data.assignee
            )

        else:
            raise self.Error('Wrong type {0}'.format(data))

        return result

    def _del(self, data):
        """Method to override in order to delete the input data.

        This method is called by the public method ``delelement``.

        :param Project data: data to delete.
        :return: deleted data.
        :rtype: Element
        :raises: Store.Error if data does not exist.
        """

        result = data

        if isinstance(data, Account):
            self.conn.delete_user(username=data.name)

        elif isinstance(data, Project):
            self.conn.delete_project(pid=self.pid(data))

        else:
            raise self.Error('Wrong type {0}'.format(data))

        return result

    @staticmethod
    def pid(project):
        """Get project pid.

        :return: first 3 characters in upper cases.
        :rtype: str
        """

        return project.name[:10].upper()

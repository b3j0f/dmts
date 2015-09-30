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

"""Gitlab store module in charge of storing data."""

from b3j0f.conf import Configurable, conf_paths, add_category
from b3j0f.dmts.rest.store import RESTStore
from b3j0f.dmts.model import (
    Account, Label, Milestone, Project, Issue, Comment, Attachment, Group,
    Member
)

import requests

from gitlab import Gitlab


@conf_paths('b3j0fdmts-gitlabstore.conf')
@add_category('GITLABSTORE')
class GitlabStore(RESTStore):
    """Gitlab store."""

    def currentaccount(self):
        """Get current account data."""

        response = self._processquery(scopes='user')

        result = self.accessor['accounts']._responsetodata(response=response)

        return result

    def connect(self):

        currentaccount()  # raise an error if it is impossible to run

    def _isconnected(self):

        result = False

        try:
            currentaccount()

        except GitlabStore.Error:
            pass

        else:
            result = True

        return result

    def disconnect(self):
        pass

    def _query(self, scopes, _id=None, pids=None, **params):
        """Process an http function.

        :param list scopes: scope names. For example, an issue uses
            ['projects', 'issues'].
        :param int _id: data id.
        :param list pids: parent ids.
        :param dict params: query parameters.
        """

        result = self.url

        # prepare path
        result = '{0}/api/v3/'.format(self.url)

        # prepare scopes
        scopes = ensureiterable(scopes, exclude=str)
        for index, scope in enumerate(scopes):
            result = '{0}/{{{0}}}/'.format(index)

        scopeformatparams = []
        if pids:
            pids = ensureiterable(pids, exclude=str)
            scopeformatparams += pids

        if _id:
            scopeformatparams.append(_id)

        elif scopes:
            result = result[:-4]

        result = result.format(scopeformatparams)

        # prepare parameters
        if self.token is not None:
            params['private_token'] = self.token

        elif self.oauth is not None:
            params['access_token'] = self.oauth

        elif self.login or self.email:  # session mode
            sessionparams = {}
            if self.login:
                sessionparams['login'] = self.login
            if self.email:
                sessionparams['email'] = self.email
            sessionparams['password'] = self.pwd

            response = self._processquery(
                operation='post', scopes='session', **kwargs
            )
            self.token = params['private_token']  # set private token
            params['private_token'] = self.token  # use private token

        if params:  # add '?' for url parameters
            result = '{0}?'.format(result)

        for param in params:
            val = params[param]
            if isinstance(val, list):  # remove '[]'
                val = str(val)[1:-1]
            result = '{0}&{1}={2}'.format(result, param, val)

        return result

    def _processquery(
            self, operation='get', scopes, _id=None, pids=None, **params
    ):
        """Process an http function.

        :param str operation: rest operation name. Default 'get'.
        :param str(s) scopes: scope names. For example, an issue uses
            ['projects', 'issues'].
        :param int _id: data id.
        :param int(s) pids: parent id(s).
        :param dict params: query parameters.
        """

        query = self._query(scopes=scopes, _id=_id, pids=pids, **params)

        procparams = {'url': query}

        request = requests[operation](query)

        if request.status_code not in [200, 201]:
            raise GitlabStore.Error(
                'Wrong query {0} ({1} - {2}).'.format(
                    query, request.status_code, request.reason
                )
            )

        else:
            return request.json()

    def get(self, _id, pids=None):

        result = None

        if issubclass(_type, Account):
            account = self.conn.getuser(user_id=_id)
            result = Account(**account)

        elif issubclass(_type, Label):


        elif issubclass(_type, Project):
            project = self.conn.getproject(project_id=_id)
            result = Project(**project)

        elif issubclass(_type, Group):
            group = self.conn.getgroups(project_id=_id)
            result = Group(**group)

        elif issubclass(_type, Comment):
            projects = self.conn.getprojects()
            if projects:
                for project in projects:
                    comment = self.conn.getissuewallnote(
                        project_id=project['id'],
                        issue_id=pid, note_id=_id
                    )
                    if comment:
                        result = comment
                        break

        elif issubclass(_type, Milestone):
            milestone = self.conn.getmilestone(
                project_id=pid, milestone_id=_id
            )
            result = Milestone(**milestone)

        else:
            raise self.Error('Wrong type {0}.'.format(_type))

        return result

    def find(
            self, names=None, descs=None, created=None, updated=None, **kwargs
    ):

        result = []

        if _type is None:
            _type = (
                Account, Label, Milestone, Project, Issue, Comment, Group,
                Member
            )

        for typ in _type:

            if issubclass(typ, Label):
                projects = self.conn.getprojects()
                if projects:
                    for project in projects:
                        labels = self.conn.getlabels(project_id=project['id'])
                        if labels:
                            for label in labels:
                                lab = Label(**label)
                                result.append(lab)

            if issubclass(typ, Project):
                projects = self.conn.getprojects()
                if projects:
                    for gitlabproject in projects:
                        project = Project(**gitlabproject)
                        result.append(project)

            elif issubclass(typ, Issue):
                issues = self.conn.getissues()
                if issues:
                    for issue in issues:
                        iss = Issue(**issue)
                        result.append(iss)

            elif issubclass(typ, Account):
                users = self.conn.getusers()
                if users:
                    for user in users:
                        account = Account(**user)
                        result.append(account)

            elif issubclass(typ, Group):
                groups = self.conn.getgroups()
                if groups:
                    for group in groups:
                        gro = Group(**group)
                        result.append(gro)

            elif issubclass(typ, Member):
                members = self.conn.getgroupmembers(group_id=data.group)
                if members:
                    for member in members:
                        mem = Member(**member)
                        result.append(mem)

            elif issubclass(typ, Comment):
                projects = self.conn.getprojects()
                if projects:
                    for project in projects:
                        issues = self.conn.getissues()
                        if issues:
                            for issue in issues:
                                comments = self.conn.getissuewallnotes(
                                    project_id=project['id'],
                                    issue_id=issue['id']
                                )
                                for comment in comments:
                                    com = Comment(**comment)
                                    result.append(mem)

            elif issubclass(typ, Milestone):
                projects = self.conn.projects()
                if projects:
                    for project in projects:
                        milestones = self.conn.getmilestones(
                            project_id=project['id']
                        )
                        if milestones:
                            for milestone in milestones:
                                mil = Milestone(**milestone)
                                result.append(mil)

            else:
                raise JiraStore.Error('Unknown type {0}'.format(typ))

        return result

    def _add(self, data):

        result = data

        if isinstance(data, Project):
            if not self.conn.createproject(name=data.name, **data):
                result = None

        elif isinstance(data, Account):
            if not self.conn.createuser(
                name=data.name, username=data.fullname,
                password=data.pwd, email=data.email
            )
            result = None

        elif isinstance(data, Milestone):
            if not self.conn.createmilestone(
                project_id=data.project, title=data.name, **data
            ):
                result = None

        elif isinstance(data, Issue):
            if not self.conn.createissue(
                project_id=data.project, title=data.name, **data
            ):
                result = None

        elif isinstance(data, Group):
            if not self.conn.creategroup(name=data.name, **data):
                result = None

        elif isinstance(data, Member):
            if not self.conn.addgroupmember(
                group_id=data.group, user_id=data.account,
                access_level=data.access_lvl
            )
            result = None

        elif isinstance(data, Comment):
            if not self.conn.createissuewallnote(
                project_id=data.group, issue_id=data.issue,
                content=data.content
            )
            result = None

        elif isinstance(data, Label):
            if not self.conn.createlabel(
                project_id=data.group, name=data.name, color=data.color
            )
            result = None

        else:
            raise self.Error('Wrong type {0}.'.format(data))

        return result

    def _update(self, data, old):

        result = data

        if isinstance(data, Account):
            if not self.conn.edituser(user_id=data._id, **data):
                result = None

        elif isinstance(data, Project):
            if not self.conn.editproject(project_id=data._id, **data):
                result = None

        elif isinstance(data, Milestone):
            if not self.conn.editmilestone(
                project_id=data.project, milestone_id=data._id, **data
            ):
                result = None

        elif isinstance(data, Issue):
            if not self.conn.editissue(
                project_id=data.project, issue_id=data._id, **data
            ):
                result = None

        elif isinstance(data, Group):
            if old is not None:  # are there members ?
                newmembers = set(data.accounts)
                oldmembers = set(old.accounts)
                memberstoremove = oldmembers - newmembers
                memberstoadd = newmembers - oldmembers

        elif isinstance(data, Member):
            if not self.conn.editgroupmember(
                group_id=data.group, user_id=data.account,
                access_level=data.access_lvl
            ):
                result = None

        elif isinstance(data, Label):
            if not self.conn.editlabel(
                project_id=data.project, name=old.name, new_name=data.name,
                color=data.color
            ):
                result = None

        else:
            raise self.Error('Wrong type {0}'.format(data))

        return result

    def _del(self, data):

        result = data

        if isinstance(data, Account):
            if not self.conn.deleteuser(user_id=data._id):
                result = None

        elif isinstance(data, Project):
            if not self.conn.deleteproject(project_id=data._id):
                result = None

        elif isinstance(data, Group):
            if not self.conn.deletegroup(group_id=data._id):
                result = None

        elif isinstance(data, Member):
            if not self.conn.deletegroupmember(
                group_id=data.group, user_id=data.account
            ):
                result = None

        elif isinstance(data, Label):
            if not self.conn.deletelabel(project_id=data.group, name=data.name):
                result = None

        else:
            raise self.Error('Wrong type {0}'.format(data))

        return result

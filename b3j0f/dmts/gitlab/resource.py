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

"""Gitlab resource module in charge of storing data."""

from b3j0f.conf import Configurable
from b3j0f.dmts.rpc.resource import RpcResource

from b3j0f.dmts.model import (
    Account, Label, Milestone, Project, Issue, Comment, Attachment, Group,
    Member
)

from gitlab import Gitlab


class GitlabResource(RpcResource):
    """Gitlab resource."""

    def connect(self):
        """Connect to the remote element with self attributes."""

        kwargs = {'host': self.url}

        if self.login is not None:
            kwargs['basic_auth'] = (self.login, self.pwd)

        if self.oauth is not None:
            kwargs['oauth_token'] = self.oauth

        if self.token is not None:
            kwargs['token'] = self.token

        self.conn = Gitlab(**kwargs)

        if self.login is not None:
            self.conn.login(
                user=self.login, password=self.pwd, email=self.email
            )

    def getelt(self, _id, _type, pid=None):

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

    def findelts(
            self,
            names=None, descs=None, created=None, updated=None, _type=None,
            **kwargs
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
                members = self.conn.getgroupmembers(group_id=elt.group)
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
                raise JiraResource.Error('Unknown type {0}'.format(typ))

        return result

    def _addelt(self, elt):

        result = elt

        if isinstance(elt, Project):
            if not self.conn.createproject(name=elt.name, **elt):
                result = None

        elif isinstance(elt, Account):
            if not self.conn.createuser(
                name=elt.name, username=elt.fullname,
                password=elt.pwd, email=elt.email
            )
            result = None

        elif isinstance(elt, Milestone):
            if not self.conn.createmilestone(
                project_id=elt.project, title=elt.name, **elt
            ):
                result = None

        elif isinstance(elt, Issue):
            if not self.conn.createissue(
                project_id=elt.project, title=elt.name, **elt
            ):
                result = None

        elif isinstance(elt, Group):
            if not self.conn.creategroup(name=elt.name, **elt):
                result = None

        elif isinstance(elt, Member):
            if not self.conn.addgroupmember(
                group_id=elt.group, user_id=elt.account,
                access_level=elt.access_lvl
            )
            result = None

        elif isinstance(elt, Comment):
            if not self.conn.createissuewallnote(
                project_id=elt.group, issue_id=elt.issue,
                content=elt.content
            )
            result = None

        elif isinstance(elt, Label):
            if not self.conn.createlabel(
                project_id=elt.group, name=elt.name, color=elt.color
            )
            result = None

        else:
            raise self.Error('Wrong type {0}.'.format(elt))

        return result

    def _updateelt(self, elt, old, upsert):

        result = elt

        if isinstance(elt, Account):
            if not self.conn.edituser(user_id=elt._id, **elt):
                result = None

        elif isinstance(elt, Project):
            if not self.conn.editproject(project_id=elt._id, **elt):
                result = None

        elif isinstance(elt, Milestone):
            if not self.conn.editmilestone(
                project_id=elt.project, milestone_id=elt._id, **elt
            ):
                result = None

        elif isinstance(elt, Issue):
            if not self.conn.editissue(
                project_id=elt.project, issue_id=elt._id, **elt
            ):
                result = None

        elif isinstance(elt, Group):
            if old is not None:  # are there members ?
                newmembers = set(elt.accounts)
                oldmembers = set(old.accounts)
                memberstoremove = oldmembers - newmembers
                memberstoadd = newmembers - oldmembers

        elif isinstance(elt, Member):
            if not self.conn.editgroupmember(
                group_id=elt.group, user_id=elt.account,
                access_level=elt.access_lvl
            ):
                result = None

        elif isinstance(elt, Label):
            if not self.conn.editlabel(
                project_id=elt.project, name=old.name, new_name=elt.name,
                color=elt.color
            ):
                result = None

        else:
            raise self.Error('Wrong type {0}'.format(elt))

        return result

    def _delelt(self, elt):

        result = elt

        if isinstance(elt, Account):
            if not self.conn.deleteuser(user_id=elt._id):
                result = None

        elif isinstance(elt, Project):
            if not self.conn.deleteproject(project_id=elt._id):
                result = None

        elif isinstance(elt, Group):
            if not self.conn.deletegroup(group_id=elt._id):
                result = None

        elif isinstance(elt, Member):
            if not self.conn.deletegroupmember(
                group_id=elt.group, user_id=elt.account
            ):
                result = None

        elif isinstance(elt, Label):
            if not self.conn.deletelabel(project_id=elt.group, name=elt.name):
                result = None

        else:
            raise self.Error('Wrong type {0}'.format(elt))

        return result

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

"""GitLab account accessor module."""

__all__ = ['AccountAccessor']

from .base import GitLabAccessor

from ...model.account import Account


class AccountAccessor(GitLabAccessor):
    """Account accessor."""

    __datatype__ = Account
    __scopes__ = 'accounts'

    def sdata2data(self, sdata):
        """Convert a sdata to an account."""

        result = self.create(
            email=sdata.get('email'),  # account fields
            pwd=sdata.get('password'),
            fullname=sdata['name'],
            avatar=sdata['avatar_url'],
            state=sdata['state'],
            _id=sdata['id'],  # Data fields
            name=sdata['username'],  # element fields
            # TODO: format to a datetime
            created=sdata.get('created_at'),
            updated=sdata.get('current_sign_in_at')
        )

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        result = None

        response = self.store._processquery(scopes='users')

        for resp in response:
            if resp['username'] == name:
                result = self.sdata2data(sdata=resp)

        return result

    def find(self, **kwargs):

        result = []

        response = self.store._processquery(scopes='users')

        accounts = []
        for resp in response:
            for key in kwargs:
                value = kwargs[key]
                if value is not None and resp.get(key) == value:
                    accounts.append(resp)

            if accounts:
                result = map(self.sdata2data, accounts)

        return result

    def _addkwargs(self, data):

        result = {
            'email': data.email, 'password': data.pwd, 'username': data.name,
            'name': data.fullname
        }

        return result

    def _updatekwargs(self, data, old):

        return self._addkwargs(data)

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

from b3j0f.sync import Accessor
from b3j0f.dmts.model.account import Account


class AccountAccessor(Accessor):
    """Account accessor."""

    __datatype__ = Account

    def _responsetodata(self, response):
        """Convert a response to a account."""

        result = self.create(
            email=response['email'],  # account fields
            fullname=response['name'],
            avatar=response['avatar_url'],
            state=response['state'],
            _id=response['id'],  # Data fields
            name=response['username'],  # element fields
            # TODO: format to a datetime
            created=response['created_at'],
            updated=response.get('current_sign_in_at')
        )

        return result

    def get(self, _id, pids=None, globalid=None):

        response = self.store._processquery(scopes='users', _id=_id)

        result = self._responsetodata(response=response)

        return result

    def getbyname(self, name, pnames=None, globalname=None):

        result = None

        response = self.store._processquery(scopes='users')

        for resp in response:
            if resp['username'] == name:
                result = self._responsetodata(resp)

        return result

    def find(self, **kwargs):

        response = self.store._processquery(scopes='users')

        accounts = []
        for resp in response:
            for key in kwargs:
                value = kwargs[key]
                if value is not None and resp.get(key) == value:
                    accounts.append(resp)
            result = map(self._responsetodata, accounts)

        return result

    def _add(self, data):

        response = self.store._processquery(
            operation='post', scopes='users', email=data.email,
            password=data.pwd, username=data.name, name=data.fullname,
        )

        result = self._responsetodata(response)

        return result

    def _update(self, data, old):

        response = self.store._processquery(
            operation='put', scopes='users', email=data.email,
            password=data.pwd, username=data.name, name=data.fullname,
        )

        result = self._responsetodata(response=response)

        return result

    def _remove(self, data):

        response = self._processquery(
            operation='delete', scopes='users', _id=data._id
        )

        result = self._responsetodata(response)

        return result

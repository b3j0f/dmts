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

from b3j0f.utils.iterable import ensureiterable
from b3j0f.conf import conf_paths, add_category
from b3j0f.dmts.http.store import HTTPStore

import requests


@conf_paths('b3j0fdmts-gitlabstore.conf')
@add_category('GITLABSTORE')
class GitLabStore(HTTPStore):
    """Gitlab store."""

    def currentaccount(self):
        """Get current account data."""

        response = self._processquery(scopes='user')

        result = self.accessor['accounts']._responsetodata(response=response)

        return result

    def connect(self):

        self.currentaccount()  # raise an error if it is impossible to run

    def _isconnected(self):

        result = False

        try:
            self.currentaccount()

        except GitLabStore.Error:
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

            response = self._processquery(verb='post', scopes='session')
            self.token = response['private_token']  # set private token
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
            self, scopes, verb='get', _id=None, pids=None, **params
    ):
        """Process an http function.

        :param str verb: rest verb name. Default 'get'.
        :param str(s) scopes: scope names. For example, an issue uses
            ['projects', 'issues'].
        :param int _id: data id.
        :param int(s) pids: parent id(s).
        :param dict params: query parameters.
        """

        query = self._query(scopes=scopes, _id=_id, pids=pids, **params)

        request = requests[verb](query)

        if request.status_code not in [200, 201]:
            raise GitLabStore.Error(
                'Wrong query {0} ({1} - {2}).'.format(
                    query, request.status_code, request.reason
                )
            )

        else:
            return request.json()

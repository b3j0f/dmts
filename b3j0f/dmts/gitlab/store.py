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

__all__ = ['GitLabStore']

from b3j0f.utils.iterable import ensureiterable
from b3j0f.conf import conf_paths, add_category

from ..http.store import HTTPStore


@conf_paths('b3j0fdmts-gitlabstore.conf')
@add_category('GITLABSTORE')
class GitLabStore(HTTPStore):
    """Gitlab store."""

    DEFAULT_URL = '/api/v'
    DEFAULT_VERSION = 3

    def __init__(
            self, url=DEFAULT_URL, version=DEFAULT_VERSION, *args, **kwargs
    ):
        """
        :param str url: default request url. Default is ``/api/v``.
        :param str version: api version. Default is 3.
        """
        super(GitLabStore, self).__init__(url=url, *args, **kwargs)

        self.version = version

    def _currentaccount(self):
        """Get current account data."""

        response = self._processquery(scopes='user')

        result = self.accessors['accounts'].sdata2data(sdata=response)

        return result

    def _urlwparams(self, scopes, _id=None, pids=None, **params):
        """Process an http function.

        :param list scopes: scope names. For example, an issue uses
            ['projects', 'issues'].
        :param int _id: data id.
        :param list pids: parent ids.
        :param dict params: query parameters.
        """

        # prepare path
        url = path = '{0}{1}'.format(self.url, self.version)
        # prepare scopes
        scopes = ensureiterable(scopes, exclude=str)
        for index, scope in enumerate(scopes):
            url = '{0}/{1}/{{{2}}}/'.format(url, scope, index)

        scopeformatparams = []
        if pids:
            pids = ensureiterable(pids, exclude=str)
            scopeformatparams += pids

        if _id:
            url = url[:-1]
            scopeformatparams.append(_id)

        elif scopes:
            url = url[:-5]

        url = url.format(*scopeformatparams)

        # prepare parameters
        if self.token is not None:
            url = '{0}?private_token={1}'.format(url, self.token)

        elif self.oauth is not None:
            url = '{0}?access_token={1}'.format(url, self.oauth)

        elif self.login or self.email:  # session mode
            sessionparams = {}
            if self.login:
                sessionparams['login'] = self.login
            if self.email:
                sessionparams['email'] = self.email
            sessionparams['password'] = self.pwd

            sessionurl = '{0}/session'.format(path)
            response = self.request(
                method=HTTPStore.POST, url=sessionurl, params=sessionparams
            )
            # set private token
            self.token = response['private_token']
            url = '{0}?private_token={1}'.format(url, self.token)

        return url, params

    def _processquery(
            self,
            scopes, method=HTTPStore.DEFAULT_METHOD, _id=None, pids=None,
            **params
    ):
        """Process an http function with business paramters.

        :param str method: rest method name. Default 'get'.
        :param str(s) scopes: scope names. For example, an issue uses
            ['projects', 'issues'].
        :param int _id: data id.
        :param int(s) pids: parent id(s).
        :param dict params: query parameters.
        """

        url, params = self._urlwparams(
            scopes=scopes, _id=_id, pids=pids, **params
        )

        result = self.request(method=method, url=url, params=params)

        return result

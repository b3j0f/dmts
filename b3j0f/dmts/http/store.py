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

__all__ = ['HTTPStore']

from httplib import (
    HTTPConnection, HTTPSConnection, OK, CREATED, ResponseNotReady
)

from urllib import urlencode

from b3j0f.sync import Store

from json import loads


class HTTPStore(Store):
    """HTTP store.

    Access to data from an http server.
    """

    VALIDE_STATUS = [OK, CREATED]  #: VALID STATUS RESPONSES.

    DEFAULT_URL = ''  #: defult url value.
    DEFAULT_METHOD = 'GET'  #: default request method.

    GET = 'GET'  #: GET method.
    POST = 'POST'  #: POST method.
    PUT = 'PUT'  #: PUT method.
    DELETE = 'DELETE'  #: DELETE method.
    HEAD = 'HEAD'  #: HEAD method.

    def __init__(
            self,
            host=None, port=None, url=DEFAULT_URL,
            login=None, pwd=None, email=None,
            token=None, oauth=None, ssl=False, key_file=None, cert_file=None,
            timeout=None,
            *args, **kwargs
    ):
        """
        :param str host: host connection.
        :param int port: port connection.
        :param str url: default request url.
        :param str login: login connection.
        :param str pwd: pwd connection.
        :param str email: email connection.
        :param str token: token connection.
        :param str oauth: oauth connection.
        :param bool ssl: use ssl connection.
        :param str key_file: name of a PEM formatted file with a private key.
        :param str cert_file: PEM formatted certificate chain file.
        :param int timeout: connection timeout.
        """

        super(HTTPStore, self).__init__(*args, **kwargs)

        # set private attribute
        self._conn = None
        self._account = None

        # set public attributes
        self.host = host
        self.port = port
        self.url = url
        self.login = login
        self.pwd = pwd
        self.email = email
        self.token = token
        self.oauth = oauth
        self.ssl = ssl
        self.key_file = key_file
        self.cert_file = cert_file
        self.timeout = timeout

    @property
    def currentaccount(self):
        """Get current account data."""

        if self._account is None:
            self._account = self._currentaccount()

        return self._account

    def _currentaccount(self):
        """Method to override in order to get current account data."""

        raise NotImplementedError()

    def connect(self):

        conn_kwargs = {
            'host': self.host, 'timeout': self.timeout, 'port': self.port
        }

        if self.ssl:
            conn_kwargs['key_file'] = self.key_file
            conn_kwargs['cert_file'] = self.cert_file
            conncls = HTTPSConnection

        else:
            conncls = HTTPConnection

        self._conn = conncls(**conn_kwargs)

    def _is_connected(self):

        return self._conn is not None and self.currentaccount is not None

    def disconnect(self):

        self._conn.close()
        self._conn = None
        self._account = None

    def request(
            self, url=None, method=DEFAULT_METHOD, params=None, headers=None
    ):
        """Process an http request with input parameters.

        :param str url: url request. None by default.
        :param str method: method request. Default ``GET``.
        :param params: optional data to send with the request.
        :param dict headers: optional header request.
        :param dict kwargs: used to enrich params for easy access.
        :return: request response deserialized json format.
        :raises: HTTPStore.Error if response status is not in
            HTTPStore.VALIDE_STATUS.
        """

        result = None

        if url is None:  # init url with default if necessary
            url = self.url

        if params is not None:  # ensure params is encoded
            params = urlencode(params)

        request_params = {'url': url, 'method': method}

        if headers:
            request_params['headers'] = headers

        if method == HTTPStore.DEFAULT_METHOD:
            if params:
                request_params['url'] = '{0}{1}{2}'.format(
                    url, '' if '?' in url else '?', params
                )

        else:
            request_params['body'] = params

        self._conn.request(**request_params)

        if method != 'HEAD':

            try:
                response = self._conn.getresponse()

            except ResponseNotReady:  # if response not ready, reconnect this
                self.disconnect()
                self.connect()
                self._conn.request(**request_params)
                response = self._conn.getresponse()

            content = response.read()

            try:
                result = loads(content)
            except ValueError:
                pass

            if response.status not in [OK, CREATED]:
                raise HTTPStore.Error(
                    'Wrong request response\n{0}{1}'.format(
                        response.msg, content
                    )
                )

        return result

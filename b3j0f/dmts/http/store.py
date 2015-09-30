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

from b3j0f.sync import Store


class HTTPStore(Store):
    """HTTP store."""

    def __init__(
            self,
            url=None, login=None, pwd=None, email=None, token=None, oauth=None,
            *args, **kwargs
    ):
        """
        :param str url: host.
        :param str login: login connection.
        :param str pwd: pwd connection.
        :param str email: email connection.
        :param str token: token connection.
        :param str oauth: oauth connection.
        """

        super(HTTPStore, self).__init__(*args, **kwargs)

        # set attributes
        self.url = url
        self.login = login
        self.pwd = pwd
        self.email = email
        self.token = token
        self.oauth = oauth

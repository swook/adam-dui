# Copyright 2018 AdaM Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
from user import User

class Element:

    name = ''
    importance = 0
    min_width = 0
    max_width = 0
    min_height = 0
    max_height = 0
    requirements = None

    prohibited_users = []
    allowed_users = []

    def __init__(self, name, importance, min_width, max_width, min_height,
                 max_height, requirements):
        self.name = name
        self.importance = importance
        self.requirements = requirements

        self.min_width = min_width
        self.min_height = min_height
        self._min_area = min_width * min_height

        self.max_width = max_width
        self.max_height = max_height
        self._max_area = max_width * max_height

        self.prohibited_users = []
        self.allowed_users = []

    def user_has_access(self, user):
        if len(self.prohibited_users) > 0:
            assert len(self.allowed_users) == 0
            return user not in self.prohibited_users

        elif len(self.allowed_users) > 0:
            assert len(self.prohibited_users) == 0
            return user in self.allowed_users

        return True

    def user_give_access(self, users):
        assert len(self.prohibited_users) == 0
        if isinstance(users, User):
            users = [users]
        assert isinstance(users, list)
        for user in users:
            assert isinstance(user, User)
            self.allowed_users.append(user)

    def user_prohibit_access(self, users):
        assert len(self.allowed_users) == 0
        if isinstance(users, User):
            users = [users]
        assert isinstance(users, list)
        for user in users:
            assert isinstance(user, User)
            self.prohibited_users.append(user)

    def __repr__(self):
        return '[Element "%s" importance=%d size_range=(%d,%d)~(%d,%d) requirements=%s]' % \
                (self.name, self.importance, self.min_width, self.min_height, self.max_width,
                 self.max_height, self.requirements)

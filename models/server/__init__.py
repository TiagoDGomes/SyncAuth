# Created on 2022/03/26
#
# Author: Tiago Gomes
#
# Copyright 2022 Tiago Gomes
#
# This file is part of SyncAuthProject.
#
# SyncAuthProject is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SyncAuthProject is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SyncAuthProject in the COPYING and COPYING.LESSER files.
# If not, see <http://www.gnu.org/licenses/>.

import logging
import warnings


class AuthServer:
    ''' AuthServer class model '''

    def __init__(self, address, domain, name=None, admin_username=None, admin_password=None):
        self.address = address
        self.domain = domain
        self.name = (name if name else domain)
        self.admin_username = admin_username
        self.admin_password = admin_password
        self._connection = None

    def sync_user(self, user):
        raise ServerUnimplementedException("Implementation sync_user?")

    def check_connection(self):
        warnings.warn("check_connection", ServerUnimplementedWarning)
        return False

    def authenticate(self, user):
        warnings.warn("authenticate", ServerUnimplementedWarning)
        return False

    def hash_password(self, plain_password):
        warnings.warn("hash_password = text_plain", ServerUnimplementedWarning)
        return plain_password

    def update_atrributes_for_user(self, user):
        raise ServerUnimplementedException(
            "Implementation update_atrributes_for_user?")

    def update_password_for_user(self, user):
        raise ServerUnimplementedException(
            "Implementation update_password_for_user?")

    def __repr__(self):
        return str({"name": self.name, "domain": self.domain, "address": self.address})





class ServerException(Exception):
    pass


class ServerEmptyValuePropertyException(ServerException):
    pass


class ServerUnimplementedException(ServerException):
    pass

class ServerUnimplementedWarning(UserWarning):
    pass


class ServerInvalidCredentialException(ServerException):
    pass


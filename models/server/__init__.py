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

import ldap3


class AuthServer:
    ''' AuthServer class model '''
    admin_username = None
    admin_password = None
    _connection = None

    def __init__(self, address, domain, name=None):
        self.address = address
        self.domain = domain
        self.name = (name if name else domain)

    def sync_user(self, user):
        raise ServerUnimplementedException("Implementation sync_user?")

    def check_connection(self):
        self._connection = None
        raise ServerUnimplementedException("Implementation check_connection?")

    def authenticate(self, user):
        raise ServerUnimplementedException("Implementation authenticate?")

    def hash_password(self, plain_password):
        return plain_password

    def update_atrributes_for_user(self, user):
        raise ServerUnimplementedException(
            "Implementation update_atrributes_for_user?")

    def update_password_for_user(self, user):
        raise ServerUnimplementedException(
            "Implementation update_password_for_user?")

    def __repr__(self):
        return str({"name": self.name, "domain": self.domain, "address": self.address})


class LDAPServer(AuthServer):
    def __init__(self, address, domain,
                 required_values=[],
                 auto_bind=ldap3.AUTO_BIND_TLS_BEFORE_BIND,
                 version=3,
                 user_as_auth=True,
                 search_base="",
                 search_user_filter="(uid={username})",
                 search_groups_filter="(objectClass=*)", field_user_password="userPassword",
                 user_auth_format=None,
                 user_group_attribute=None
                 ):
        self.required_values = required_values
        self.domain = domain
        self.address = address
        self.auto_bind = auto_bind
        self.version = version
        self.user_as_auth = user_as_auth
        self.search_base = search_base
        self.search_user_filter = search_user_filter
        self.search_groups_filter = search_groups_filter
        self.field_user_password = field_user_password
        self.user_auth_format = user_auth_format
        self.user_group_attribute = user_group_attribute

    def check_connection(self):
        ''' Check if connection is active '''
        logging.debug(("check_connection", ))
        if not self.search_base:
            raise ServerEmptyValueException("search_base")
        if self._connection is None or self._connection.closed:
            logging.debug(("check_connection disconnected", ))
            return self.connect()

    def connect(self, username=None, password=None):
        ''' Connect LDAP server. If no value is passed, authentication is done with the administrator account '''
        admin_mode = False
        if not username or not password:
            username = self.admin_username
            password = self.admin_password
            admin_mode = True
        user_formatted = self.user_auth_format.format(
            username=username,
            domain=self.domain,
        )
        try:
            c = ldap3.Connection(server=self.address, user=user_formatted,
                                 password=password, auto_bind=self.auto_bind)
            if admin_mode:
                self._connection = c
            logging.debug((username, "connect ok",))
            return True
        except ldap3.core.exceptions.LDAPBindError as e:
            logging.error((username, "LDAPBindError", e))
            pass

    def authenticate(self, user):
        ''' Authenticates the user with username and password. '''
        logging.debug((user.user_name, "authenticate"))
        if not self.search_base:
            raise ServerEmptyValueException("search_base")
        authenticated = False
        if self.user_as_auth:
            if self.connect(username=user.user_name, password=user.plain_password):
                authenticated = True
        else:
            raise ServerUnimplementedException("authenticate - user_as_auth")
        if authenticated:
            self.update_atrributes_for_user(user)
        return authenticated

    def update_password_for_user(self, user):
        ''' Directly update the user's password on the server. '''
        logging.debug((user.user_name, "update_password_for_user","prepare"))
        self.check_connection()
        self.update_atrributes_for_user(user)
        logging.debug((user.user_name, "update_password_for_user","start"))
        attr_update = {
            self.field_user_password: [
                (ldap3.MODIFY_REPLACE,  self.hash_password(user.plain_password))]
        }
        try:
            r = self._connection.modify(
                user.attributes[self.domain]['dn'], attr_update)
            logging.debug(
                (user.user_name, "update_password_for_user","result", r))
        except Exception as e:
            logging.error(
                (user.user_name, "update_password_for_user","error", e))

    def update_atrributes_for_user(self, user):
        ''' Updates user attributes (local variable). '''
        logging.debug((user.user_name, "update_atrributes_for_user","start"))
        self.check_connection()
        search = self.search_user_filter.format(
            username=user.user_name,
            domain=self.domain
        )
        ret = self._connection.search(
            search_base=self.search_base, search_filter=search, attributes=[
                ldap3.ALL_ATTRIBUTES]
        )
        if ret:
            for entry in self._connection.response:
                if 'dn' in entry:
                    user.attributes[self.domain] = entry
                    user.groups[self.domain] = entry['attributes'][self.user_group_attribute]
                    logging.debug(
                        (user.user_name, self.domain,
                         user.groups[self.domain]
                         )
                    )
                    user.attributes[self.domain]['dn'] = entry['dn']
                    logging.debug((user.user_name, "dn", entry['dn']))
                    break


class DomainControllerServer(LDAPServer):
    def __init__(self, *args, **kwargs):
        super(DomainControllerServer, self).__init__(
            field_user_password="unicodePwd",
            user_group_attribute="memberOf",
            search_user_filter="(|(userPrincipalName={username})(cn={username})(sAMAccountName={username}))",
            user_auth_format="{username}@{domain}",
            *args, **kwargs)

    def sync_user(self, user):
        print("fake sync")

    def hash_password(self, plain_password):
        ''' The DC requires that the password value be specified in 
        a UTF-16 encoded Unicode string containing the password surrounded
        by quotation marks, which has been BER-encoded as an octet string 
        per the Object(Replica-Link) syntax. 
        Link: https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/6e803168-f140-4d23-b2d3-c3a8ab5917d2
        '''
        return ('\"' + plain_password + '\"').encode('utf-16-le')


class WebProxyLDAPServer(AuthServer):
    pass


class DataBaseAuthServer(AuthServer):
    pass


class ServerException(Exception):
    pass


class ServerEmptyValueException(ServerException):
    pass


class ServerUnimplementedException(ServerException):
    pass


class ServerInvalidCredentialException(ServerException):
    pass

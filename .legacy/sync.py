# -*- coding: utf-8 -*-

# Created on 2017/03/08
#
# Author: Tiago Gomes
#
# Copyright 2017 Tiago Gomes
#
# This file is part of RADIUSSyncServer.
#
# RADIUSSyncServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RADIUSSyncServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RADIUSSyncServer in the COPYING and COPYING.LESSER files.
# If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import settings
import ldap3


    


def auth(username, password):
    valid = {}
    for server_config in settings.LDAP_SERVERS:
        if not valid:
            conn_auth = None
            try:
                server_ldap = ldap3.Server(server_config['uri'], get_info=ldap3.ALL)
                conn_auth = ldap3.Connection(server=server_ldap, 
                                             authentication=ldap3.SIMPLE, 
                                             user=username, 
                                             password=password,
                                             auto_bind=True)
                conn_auth.unbind()    
            except: 
                pass        
            if conn_auth:
                valid['domain'] = server_config['domain']
                
                conn_prop = ldap3.Connection(server=server_ldap, 
                                             authentication=ldap3.SIMPLE, 
                                             user=server_config['admin_user_dn'], 
                                             password=server_config['admin_password'],
                                             auto_bind=True)
                
                result = conn_prop.search(
                                search_base=server_config['base_dn'], 
                                search_filter=server_config['filter_user'].format(username=username), 
                                search_scope=ldap3.SUBTREE,)
                
                conn_prop.unbind()
                
        if valid:        
            sync_user(username, password)
            

def sync_user(username, password):
    pass









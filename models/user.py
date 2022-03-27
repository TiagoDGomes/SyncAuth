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

    

class User:
    def __init__(self, user_name="", plain_password="", attributes=dict(), server_order=[]):            
        self.user_name = user_name
        self.plain_password = plain_password
        self.attributes = attributes
        self._groups = dict()
        self.server_order = server_order

    def __repr__(self):
        return str({"user_name": self.user_name, "plain_password": self.plain_password, "groups": self.groups, "attributes": self.attributes})   

    
    def rebuild(self, known_groups):
        #print(("rebuild start",self._groups))
        self._groups[None] = []
        for group_name in known_groups:
            #print(("group_name", group_name))
            for domain, groups_dn in self._groups.items():
                #print(("group domain group_dn", domain, groups_dn))
                #print(("group kg gn", known_groups[group_name]))
                for group_dn in groups_dn:
                    if group_dn in known_groups[group_name]:
                        self._groups[None].append(group_name)

        #print(("rebuild ok",self._groups))

    @property
    def groups(self):
        class groups_gen(dict):
            def __init__(self, g):
                #print(("iniciando property...", g))
                self.g = g
                if not None in self.g:
                    self.g[None] = []
                #return self.g

            def __contains__(self, o):
                #print(("contains property...", o))
                return o in self.g[None]

            def __iter__(self):
                #print(("iter property...", self.g))
                return self.g.items
            
            def __getitem__(self, name):
                #print(("get item...", name))
                return self.g[name]

            def __setitem__(self, name, value):
                #print(("set item...", name, value))
                self.g[name] = value

            def __repr__(self):
                return str(self.g)
            
            

        return groups_gen(self._groups)

        

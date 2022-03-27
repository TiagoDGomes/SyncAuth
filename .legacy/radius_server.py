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
from pyrad import server, packet
import sync


class RADIUSServer(server.Server):
    def HandleAuthPacket(self, pkt):
        reply = self.CreateReplyPacket(pkt, **{})
        valid = None
        try:
            username = pkt['User-Name']
            password = map(pkt.PwDecrypt,pkt['User-Password'])
            valid = sync.auth(username, password)
        except:
            pass
        if valid:                
            reply.code = packet.AccessAccept
        else:
            reply.code = packet.AccessReject
        self.SendReplyPacket(pkt.fd, reply)
        
            
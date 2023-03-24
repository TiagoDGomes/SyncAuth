import logging
import time
import ldap3
from models.server import AuthServer, ServerEmptyValuePropertyException


class LDAPServer(AuthServer):
    def __init__(self, address, domain,
                 admin_username,
                 admin_password,
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
        super(LDAPServer, self).__init__(address, domain)
        self.required_values = required_values
        self.auto_bind = auto_bind
        self.version = version
        self.user_as_auth = user_as_auth
        self.search_base = search_base
        self.search_user_filter = search_user_filter
        self.search_groups_filter = search_groups_filter
        self.field_user_password = field_user_password
        self.user_auth_format = user_auth_format
        self.user_group_attribute = user_group_attribute
        self.admin_username = admin_username
        self.admin_password = admin_password

    def __del__(sel, *args, **kwargs):        
        logging.debug(('__del__','unbind'))
        try:
            self._connection.unbind()
        except:
            pass
        #super(LDAPServer, self).__del__(*args, **kwargs)

    def check_connection(self):
        ''' Check if connection is active '''
        logging.debug(("check_connection", ))
        if not self.search_base:
            raise ServerEmptyValuePropertyException("search_base")
        if self._connection is None or self._connection.closed:
            logging.debug(("check_connection disconnected", ))
            return self.connect()

    def connect(self, username=None, password=None):
        ''' Connect LDAP server. If no value is passed, authentication is done with the administrator account '''
        admin_mode = False
        logging.debug((username, 'connect'))
        if not username or not password:
            if not self.admin_username :
                raise ServerEmptyValuePropertyException("admin_username")
            if not self.admin_password:
                raise ServerEmptyValuePropertyException("admin_password")
            username = self.admin_username
            password = self.admin_password
            admin_mode = True
            
        user_formatted = self.user_auth_format.format(
            username=username,
            domain=self.domain,
        )
        try:
            logging.debug((username, 'connect pass Connection',user_formatted, password ))
            c = ldap3.Connection(server=self.address, user=user_formatted,
                                 password=password, auto_bind=self.auto_bind, lazy=False)
            
            logging.debug((username, 'admin_mode', admin_mode))
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
        authenticated = False
        user_formatted = self.user_auth_format.format(
            username=user.user_name,
            domain=self.domain,
        )
        c = None
        try:
            # logging.debug((user.user_name, 'authenticate pass connection sleep', user_formatted, user.plain_password))
            # time.sleep(3)
            logging.debug((user.user_name, 'authenticate pass connection wake', user_formatted, user.plain_password))
            s = ldap3.Server(self.address, get_info=ldap3.ALL)
            c = ldap3.Connection(s, 
                                 user=user_formatted,
                                 password=user.plain_password, 
                                 auto_bind=True,
                                 lazy=False,)   
            if c.bind():                                   
                logging.debug((user.user_name, "authenticate ok"))
                authenticated = True
                logging.debug((user.user_name, "authenticate unbind",))          
        except ldap3.core.exceptions.LDAPBindError as e:            
            logging.error((user.user_name, "LDAPBindError", e))
        finally:
            logging.debug((user.user_name, "authenticate finally",))
            try:
                c.unbind() 
                del c   
            except Exception as ex:
                logging.debug((user.user_name, "authenticate finally exception", ex))        
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
            #logging.debug((user.user_name, "update_password_for_user","connection", self._connection))
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
                    # logging.debug(
                    #     (user.user_name, user)
                    # )
                    user.attributes[self.domain]['dn'] = entry['dn']
                    logging.debug((user.user_name, "dn", entry['dn']))
                    break

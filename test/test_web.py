
import logging
import unittest

from models import user
from models.server.web import WebProxyLDAPServer

try:
    from test.local_config import *
except Exception as e: 
    logging.debug(('import local config error', e))
    TEST_WEB_URL = "http://www.example.com/ldap_json_proxy.php"
    TEST_WEB_DOMAIN = "web.example.com"
    TEST_WEB_ADDRESS = "192.168.1.1"
    TEST_WEB_SEARCH_BASE = "dc=vvvv,dc=www,dc=zzz"
    TEST_WEB_KEY = "this_is_a_secret_key"
    TEST_WEB_FORM_KEY = "key"
    TEST_WEB_FORM_ADDRESS = "address"
    TEST_WEB_FORM_USERNAME = "username"
    TEST_WEB_FORM_PASSWORD = "password"
    TEST_WEB_FORM_ADMIN_USERNAME = "admin_dn"
    TEST_WEB_FORM_ADMIN_PASSWORD = "admin_pass"
    TEST_WEB_ADMIN_USERNAME="uid=abc,ou=cde,ou=efg,ou=hij,dc=klm,dc=com,dc=br",
    TEST_WEB_ADMIN_PASSWORD="my_secret_pass",


class TestWebProxyLDAP(unittest.TestCase):

    def test_invalid_credentials(self):
        self.user = user.User()
        self.user.user_name = "aaaaaa"
        self.user.plain_password = "bbbbbb" 
        self.assertFalse(self.server.authenticate(self.user), "Expected: invalid credentials") 

    def test_valid(self):
        global TEST_USER_NAME, TEST_USER_PASS
        self.user = user.User()
        self.user.user_name = TEST_USER_NAME
        self.user.plain_password = TEST_USER_PASS 
        self.assertTrue(self.server.authenticate(self.user), "Expected: valid credentials") 

    def test_change_password(self):   
        pass

    def setUp(self):
        self.server = WebProxyLDAPServer(
                            TEST_WEB_ADDRESS, 
                            TEST_WEB_DOMAIN, 
                            url=TEST_WEB_URL, 
                            base_dn=TEST_WEB_SEARCH_BASE, 
                            key=TEST_WEB_KEY,
                            form_key=TEST_WEB_FORM_KEY,
                            form_user_name=TEST_WEB_FORM_USERNAME,
                            form_user_pass=TEST_WEB_FORM_PASSWORD, 
                            form_address=TEST_WEB_FORM_ADDRESS,                            
                            form_admin_user_name=TEST_WEB_FORM_ADMIN_USERNAME,
                            form_admin_password=TEST_WEB_FORM_ADMIN_PASSWORD, 
                            admin_user_name=TEST_WEB_ADMIN_USERNAME,
                            admin_password=TEST_WEB_ADMIN_PASSWORD,                            
                            )
    
    def set_user(self):
        self.user = user.User()
        self.user.user_name = TEST_USER_NAME
        self.user.plain_password = TEST_USER_PASS  

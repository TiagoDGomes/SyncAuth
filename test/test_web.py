
import unittest
from models.server.web import WebProxyLDAPServer
from models import user
import logging

try:
    from test.local_config import *
except Exception as e: 
    logging.debug(('import local config error', e))
    TEST_WEB_URL = "http://www.example.com/ldap_json_proxy.php"
    TEST_WEB_DOMAIN = "web.example.com"
    TEST_WEB_ADDRESS = "192.168.1.1"
    TEST_WEB_SEARCH_BASE = "dc=vvvv,dc=www,dc=zzz"
    TEST_WEB_KEY = "this_is_a_secret_key"


class TestWebProxyLDAP(unittest.TestCase):

    def test_invalid_credentials(self):
        self.user = user.User()
        self.user.user_name = "aaaaaa"
        self.user.plain_password = "bbbbbb" 
        self.assertFalse(self.server.authenticate(self.user)) 

    def test_valid(self):
        global TEST_USER_NAME, TEST_USER_PASS
        self.user = user.User()
        self.user.user_name = TEST_USER_NAME
        self.user.plain_password = TEST_USER_PASS 
        self.assertTrue(self.server.authenticate(self.user)) 

    def test_change_password(self):   
        pass

    def setUp(self):
        self.server = WebProxyLDAPServer(TEST_WEB_ADDRESS, TEST_WEB_DOMAIN, url=TEST_WEB_URL, base_dn=TEST_WEB_SEARCH_BASE, key=TEST_WEB_KEY)
    
    def set_user(self):
        self.user = user.User()
        self.user.user_name = TEST_USER_NAME
        self.user.plain_password = TEST_USER_PASS  
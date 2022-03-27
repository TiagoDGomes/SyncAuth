


import logging
import unittest
import sys
from models.server.dc import DomainControllerServer
from models import user
from pprint import pprint


logging.basicConfig(encoding='utf-8', level=logging.DEBUG, 
        #filename='test.log', 
        stream=sys.stdout,
)

try:
    from test.local_config import *
except: 
    TEST_AD_SERVER_ADDRESS = "192.168.0.1"
    TEST_AD_SERVER_DOMAIN = "abc.example.com"
    TEST_AD_USER_AUTH_FORMAT = "{username}@{domain}"
    TEST_AD_SEARCH_BASE = "DC=zzzzzzzz,DC=yyyyyyyyy,DC=wwwwwwww,DC=vvvvvvvv"

    TEST_AD_ADMIN_USER_NAME = "aaaaaaaaaaaaa"
    TEST_AD_ADMIN_PASSWORD = "bbbbbbbbbbbbbb"

    TEST_USER_NAME = "xxxxxxxxxxxxxxxx"
    TEST_USER_PASS = "yyyyyyyyyyyyyyyy"

    TEST_AD_USER_DN_GROUP='CN=rrrrrrr,OU=xxxxxx,OU=xxxxxx,'+TEST_AD_SEARCH_BASE
    TEST_AD_USER_GROUP='Users'

    TEST_GRUPOS_CONHECIDOS = {
    'Servidores' : [
        'CN=tttttt,OU=qqqqq,OU=eeeeee,DC=ggggggg,DC=nnnnnn,DC=zzzzzz,DC=xxx',
        TEST_AD_USER_DN_GROUP,
        ],
        'Users': [
        'CN=Domain Users,CN=Users,'+TEST_AD_SEARCH_BASE,
        ],
    }





class TestDomainController(unittest.TestCase):
    def set_normal(self):      
        self.ad_server = DomainControllerServer(TEST_AD_SERVER_ADDRESS, TEST_AD_SERVER_DOMAIN)      
        self.ad_server.admin_username = TEST_AD_ADMIN_USER_NAME
        self.ad_server.admin_password = TEST_AD_ADMIN_PASSWORD
        self.ad_server.search_base = TEST_AD_SEARCH_BASE   

    def set_user(self):
        self.user = user.User()
        self.user.user_name = TEST_USER_NAME
        self.user.plain_password = TEST_USER_PASS  

    def test_invalid_admin_credentials(self):
        logging.debug("test_invalid_credentials")   
        self.ad_server = DomainControllerServer(TEST_AD_SERVER_ADDRESS, TEST_AD_SERVER_DOMAIN)      
        self.ad_server.admin_username = "aaaaaa"
        self.ad_server.admin_password = "bbbbbb"
        self.ad_server.search_base = TEST_AD_SEARCH_BASE
        self.assertFalse(self.ad_server.check_connection())

    def test_valid(self):
        logging.debug("test_valid")  
        self.set_normal()
        self.set_user()
        logging.debug("test_valid authenticate")          
        self.assertTrue(self.ad_server.authenticate(self.user))
        logging.debug("test_valid groups")
        self.assertIn(TEST_AD_USER_DN_GROUP, self.user.groups[TEST_AD_SERVER_DOMAIN])
        logging.debug("test_valid rebuild")
        self.user.rebuild(TEST_GRUPOS_CONHECIDOS)        
        logging.debug("test_valid groups known_groups")
        self.assertIn(TEST_AD_USER_GROUP , self.user.groups)
        

    def test_change_password(self):    
        logging.debug("test_change_password")
        self.set_normal()
        self.set_user()
        self.user.rebuild(TEST_GRUPOS_CONHECIDOS) 
        self.user.plain_password = "a1b2P5232iwrfsdf321ewqd"
        self.assertFalse(self.ad_server.authenticate(self.user), "User cannot authenticate with invalid password")
        self.ad_server.update_password_for_user(self.user)
        self.assertTrue(self.ad_server.authenticate(self.user), "User with changed password needs to authenticate")       
        self.user.plain_password = TEST_USER_PASS
        self.assertFalse(self.ad_server.authenticate(self.user), "User cannot authenticate with old password")
        self.ad_server.update_password_for_user(self.user)
        self.assertTrue(self.ad_server.authenticate(self.user), "User with reset password needs to authenticate")



        
    def test_error_search_base_empty(self):        
        self.ad_server = DomainControllerServer(TEST_AD_SERVER_ADDRESS, TEST_AD_SERVER_DOMAIN)      
        self.ad_server.admin_username = TEST_AD_ADMIN_USER_NAME
        self.ad_server.admin_password = TEST_AD_ADMIN_PASSWORD
        self.set_user()
        with self.assertRaises(Exception):            
            self.ad_server.check_connection()         
            self.ad_server.authenticate(self.user)



    
        
if __name__ == "__main__":
    unittest.main()
    

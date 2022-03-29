import logging

import requests
from models.server import AuthServer


class WebProxyLDAPServer(AuthServer):
    def __init__(self, address, domain, url, base_dn, key=None, form_user_name="username", form_user_pass="password", 
                form_default_method="post", form_key="", form_address="addr", form_base_dn="dn", 
                *args, **kwargs):
        super(WebProxyLDAPServer, self).__init__(address, domain, *args, **kwargs)
        self.form_user_name = form_user_name
        self.form_user_pass = form_user_pass
        self.form_key = form_key
        self.key = key
        self.form_default_method = form_default_method
        self.form_address = form_address
        self.form_base_dn = form_base_dn
        self.base_dn = base_dn
        self.url = url

    def submit(self, data={}, method="post",):        
        if method.lower() == "get":
            req = requests.get      
        else:
            req = requests.post
        response = req(self.url, data)
        #logging.debug((method, response.json()))
        return response.json()

        

    def authenticate(self, user):        
        logging.debug((user.user_name, 'authenticate', ))
        result = self.submit({
            self.form_user_name: user.user_name,
            self.form_user_pass: user.plain_password,
            self.form_address: self.address,
            self.form_base_dn: self.base_dn,
            self.form_key: self.key,
        })
        if len(result) > 1:
            logging.debug((user.user_name, 'authenticate', "ok" ))
            user.attributes[self.domain] = result
            return True
        logging.debug((user.user_name, 'authenticate', "fail"))
        return False
        

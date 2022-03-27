from models.server.ldap import LDAPServer

class DomainControllerServer(LDAPServer):
    def __init__(self, *args, **kwargs):
        super(DomainControllerServer, self).__init__(*args, **kwargs)        
        self.field_user_password="unicodePwd"
        self.user_group_attribute="memberOf"
        self.search_user_filter="(|(userPrincipalName={username})(cn={username})(sAMAccountName={username}))"
        self.user_auth_format="{username}@{domain}"

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


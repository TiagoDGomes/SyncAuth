
from __future__ import unicode_literals

LDAP_SERVERS = [

                {   
                    'uri' : 'ldap://example.net:389',
                    'domain' : 'example.net',
                    'base_dn': 'DC=ldap,DC=example,DC=net',
                    'admin_user_dn': None,
                    'admin_password': None,
                    'filter_user': '(uid={username})',
                    'containers': {
                                    'administrators' : 'OU=administrators,DC=ldap,DC=example,DC=net',
                                    'customer': 'OU=customer,DC=ldap,DC=example,DC=net',
                                    None: 'OU=guests,DC=ldap,DC=example,DC=net', # default container
                                  },
                    'groups' : {
                                    'administrators' : 'OU=administrators,CN=groups,DC=ldap,DC=example,DC=net',
                                    'customer': 'OU=customer,CN=groups,DC=ldap,DC=example,DC=net',
                                    None: 'OU=guests,CN=grupos,DC=ldap,DC=example,DC=net', # default group
                                },
                    'password_attr': None, # deixe None para não sincronizar senha
                 },

                {                    
                    'uri' : 'ldap://domain.example.net:389',
                    'domain' : 'domain.example.net',
                    'base_dn': 'DC=domain,DC=example,DC=net',
                    'admin_user_dn': 'CN=Administrator,CN=Users,DC=domain,DC=example,DC=net',
                    'admin_password': '123456789',
                    'filter_user': '(|(uid={username})(cn=*{username}*)(sAMAccountName={username}))',
                    'password_attr': 'unicodePwd',
                    'containers': {
                                    'administrators' : 'OU=adms,OU=domain,DC=example,DC=net',
                                    'customer': 'OU=cust,OU=domain,DC=example,DC=net',
                                    None: 'OU=guests,OU=domain,DC=domain,DC=example,DC=net', # default container
                                  },
                    'groups' : {
                                    'administrators' : 'CN=adms,CN=Groups,DC=domain,DC=example,DC=net',
                                    'customer': 'CN=cust,CN=Groups,DC=domain,DC=example,DC=net',
                                    None: 'CN=guests,CN=Groups,DC=domain,DC=example,DC=net', # default group
                                },
                    
                    'skeletons' : {
                                    'administrators' : 'CN=user.base,OU=adms,DC=domain,DC=example,DC=net',
                                    'customer': 'CN=customer.base,OU=customer,DC=domain,DC=example,DC=net',
                                    None: 'CN=guest.base,OU=guests,DC=domain,DC=example,DC=net', # default user
                                },
                    
                    'user_properties': {
                                    'cn': '{uid}' ,
                                    'description': '{username} - {displayName} ({mail})',
                                    'objectClass' : [str('top'), str('user'), str('person'), str('organizationalPerson')],
                                    'uid' : '{username}',
                                    'name': '{username} - {displayName} ({mail})',
                                    'sAMAccountName' : '{username}',
                                    'msSFU30Name' : '{username}',
                                    'displayName': '{displayName}',
                                    'givenName': '{givenName}',
                                    'sn' : '{sn}',
                                    'userAccountControl': ['512'],
                                    'userPrincipalName' : "{uid}@{domain}" ,
                                    },
                    'properties_replace': {
                                    'aluno.base': '{username}',
                                    'visitante.base': '{username}',
                                    'servidor.base': '{username}',                                  
                    },
                    'forbidden_properties_copy':  [
                                    'objectSid','distinguishedName','whenCreated','objectCategory','uSNChanged',
                                    'uSNCreated','objectGUID','createTimeStamp','modifyTimeStamp','uidNumber',
                                    'primaryGroupID','sAMAccountType','isCriticalSystemObject',
                                    'msDS-User-Account-Control-Computed','memberOf','cn'],
                    
                 },
                   
                   
                {   
                    'uri' : 'ldap://otherldap.example.net:389',
                    'domain' : 'otherldap.example.net',
                    'base_dn': 'DC=otherldap,DC=example,DC=net',
                    'filter_user': '(uid={username})',
                    'admin_user_dn': 'cn=admin,DC=otherldap,DC=example,DC=net',
                    'admin_password': '123456789',
                    'password_attr': None,
                 },                
               ]

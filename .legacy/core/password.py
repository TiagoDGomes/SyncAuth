# -*- coding: utf-8 -*-
''' Pacote para tratamento de senhas e hashes '''
from __future__ import unicode_literals

import base64
import binascii
import hashlib
import os


try:
    import bcrypt
except ImportError:
    print('bcrypt não está instalado. Execute: pip install bcrypt.')

TYPE_ACTIVE_DIRECTORY_PASSWORD = 'AD'
TYPE_SSHA_PASSWORD = 'SSHA'
TYPE_SHA_PASSWORD = 'SHA'
TYPE_SHA256_PASSWORD = 'SHA256'
TYPE_MD5_PASSWORD = 'MD5'
TYPE_BLOWFISH_PASSWORD = 'BLOWFISH'
TYPE_PLAIN_PASSWORD = 'PLAIN'
TYPE_NTLM_PASSWORD = 'NTLM'


def check_password(plain_password, raw_password):
    ''' Verifica se a senha em texto plano é a mesma em hash'''
    if raw_password.upper().startswith('{SSHA}'):
        print('ok ssha')
        return check_ssha(plain_password, raw_password[6:])
    elif raw_password.upper().startswith('{SHA}'):
        print('ok sha')
        return check_sha(plain_password, raw_password[5:])
    elif raw_password.upper().startswith('{SHA256}'):
        print('ok sha256')
        return check_sha256(plain_password, raw_password[8:])
    elif raw_password.upper().startswith('{MD5}'):
        print('ok md5')
        return check_md5(plain_password, raw_password[5:])
    elif raw_password.upper().startswith('$2'):        
        print('ok blow')
        ret = check_blowfish(plain_password, raw_password)
        if ret:
            return True
    # Se nenhuma das anteriores funcionar,
    # tentar identificar automaticamente.
    return plain_password == raw_password  \
        or check_sha(plain_password, raw_password) \
        or check_md5(plain_password, raw_password) \
        or check_ssha(plain_password, raw_password) \
        or check_sha256(plain_password, raw_password) \
        or check_md4(plain_password, raw_password) \
        


def check_ssha(plain_value, ssha_value):
    ''' Verifica se o texto plano é o mesmo em SSHA'''
    return ssha_value == generate_password(plain_value, TYPE_SSHA_PASSWORD)


def check_sha(plain_value, sha_value):
    ''' Verifica se o texto plano é o mesmo em SHA'''
    return sha_value == generate_password(plain_value, TYPE_SHA_PASSWORD)


def check_sha256(plain_value, value):
    ''' Verifica se o texto plano é o mesmo em SHA'''
    return value == generate_password(plain_value, TYPE_SHA256_PASSWORD)


def check_md5(plain_value, value):
    ''' Verifica se o texto plano é o mesmo em MD5'''
    return value == generate_password(plain_value, TYPE_MD5_PASSWORD)



def check_md4(plain_value, value):
    ''' Verifica se o texto plano é o mesmo em MD4'''
    return value == generate_password(plain_value, type_password=TYPE_NTLM_PASSWORD)
    


def check_blowfish(plain_value, value):
    ''' Verifica se o texto em blowfish condiz com texto plano'''
    return value == generate_password(plain_value, type_password=TYPE_BLOWFISH_PASSWORD)

def check_ad_password(plain_value, value):
    ''' Verifica se o texto em utf-16-le condiz com texto plano'''
    return value == generate_password(plain_value, type_password=TYPE_ACTIVE_DIRECTORY_PASSWORD)



def generate_password(plain_password, type_password=TYPE_PLAIN_PASSWORD, salt=None):
    ''' Função que gera a senha de acordo com o tipo de senha desejado'''
    new_password = plain_password
    if type_password == TYPE_BLOWFISH_PASSWORD:
        try:
            new_password = bcrypt.hashpw(
                (plain_password.encode("utf-8")), bcrypt.gensalt(rounds=4)).decode("utf-8")
        except NameError:
            print('''bcrypt não está instalado. Senha gerada será em texto plano.''')
    elif type_password == TYPE_ACTIVE_DIRECTORY_PASSWORD:
        password = plain_password
        new_password = ('\"' + password + '\"').encode('utf-16-le')
    elif type_password == TYPE_NTLM_PASSWORD:
        plain_password = plain_password.encode('utf-16le')
        pass_digest = hashlib.new('md4', plain_password).digest()
        new_password = ( binascii.hexlify(pass_digest)  ).decode('UTF-8') 
       
    elif type_password == TYPE_MD5_PASSWORD:
        pass_digest = hashlib.new('md5', plain_password.encode("utf-8")).digest()
        new_password = (b'{MD5}' + binascii.hexlify(pass_digest)).decode('UTF-8') 
    elif type_password == TYPE_SHA_PASSWORD:
        pass_digest = hashlib.new('sha1', plain_password.encode("utf-8")).digest()
        new_password = (b'{SHA}' + binascii.hexlify(pass_digest)).decode('UTF-8') 
    elif type_password == TYPE_SHA256_PASSWORD:
        pass_digest = hashlib.new('sha256', plain_password.encode("utf-8")).digest()
        new_password = (b'{SHA256}' + binascii.hexlify(pass_digest)).decode('UTF-8') 
    elif type_password == TYPE_SSHA_PASSWORD:
        if not salt:
            salt = os.urandom(4)
        sha1_hash = hashlib.sha1(plain_password.encode("utf-8"))
        sha1_hash.update(salt)
        new_password = (b'{SSHA}' + base64.b64encode(sha1_hash.digest() + salt)).decode('UTF-8')
    #print(("plain_password", plain_password, "new_password", new_password,"type", type(new_password) ,  "type_password", type_password))
    return new_password

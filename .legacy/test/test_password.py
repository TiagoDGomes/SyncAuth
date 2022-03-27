
import unittest
from core import password
from core.password import check_password, generate_password, check_md4
import binascii



class TestHash(unittest.TestCase):


    def test_sha(self):
        self.assertTrue(check_password('1234','{SHA}cRDtpNCeBiql5KOQsKVyrA0sAiA=')) #sha 1 
        self.assertFalse(check_password('1235','{SHA}cRDtpNCeBiql5KOQsKVyrA0sAiA=')) #sha 2
        self.assertTrue(check_password('1234','cRDtpNCeBiql5KOQsKVyrA0sAiA=')) #sha 3
        self.assertFalse(check_password('1235','cRDtpNCeBiql5KOQsKVyrA0sAiA=')) #sha 4
    
    def test_ssha(self):    
        self.assertTrue(check_password('1234','{SSHA}qWOSG9l889y55Ck9icB2ORPeHlVU0a3sU29wBg==')) #ssha 1
        self.assertFalse(check_password('1235','{SSHA}qWOSG9l889y55Ck9icB2ORPeHlVU0a3sU29wBg==')) #ssha 2
        self.assertTrue(check_password('1234','qWOSG9l889y55Ck9icB2ORPeHlVU0a3sU29wBg==')) #ssha 3
        self.assertFalse(check_password('1235','qWOSG9l889y55Ck9icB2ORPeHlVU0a3sU29wBg==')) #ssha 4
    
    def test_sha256(self):    
        self.assertTrue(check_password('1234','{SHA256}A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=')) #sha256 1
        self.assertFalse(check_password('1235','{SHA256}A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=')) #sha256 2 
        self.assertTrue(check_password('1234','A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=')) #sha256 3 
        self.assertFalse(check_password('1235','A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=')) #sha256 4 
    
    def test_md5(self):    
        self.assertTrue(check_password('1234','{MD5}gdyb21LQTcIANtvYMT7QVQ=='))  #md5 1
        self.assertFalse(check_password('1235','{MD5}gdyb21LQTcIANtvYMT7QVQ=='))  #md5 2
        self.assertTrue(check_password('1234','gdyb21LQTcIANtvYMT7QVQ==='))  #md5 3
        self.assertFalse(check_password('1235','gdyb21LQTcIANtvYMT7QVQ==='))  #md5 4
    
    def test_plain(self):
        self.assertTrue(check_password('12345','12345'))  # plain
        

    def test_blowfish(self):    
        self.assertFalse(check_password('12347','$2y$15$rOj5wE3Owypvgrb5klq.v.C70JRF09CS9kGU3fceV4MZjvr9VWB/O')) #blowfish 1
        self.assertFalse(check_password('543210','$2y$15$GSsMXMrKHQHHpoPbw7WH8uEfjeBF12UEMm0YtSYV2f9Sj/AqPf6dC')) #blowfish 2     
        self.assertTrue(check_password('12345','$2y$15$rOj5wE3Owypvgrb5klq.v.C70JRF09CS9kGU3fceV4MZjvr9VWB/O')) #blowfish 3
        self.assertTrue(check_password('54321','$2y$15$GSsMXMrKHQHHpoPbw7WH8uEfjeBF12UEMm0YtSYV2f9Sj/AqPf6dC')) #blowfish 4 
        self.assertTrue(check_password('12345','$2b$15$lxxW/s0UuxUX0X8B8OwEu.PIM4FyUip96l0wuSpBTtVvAdjWjx4PW')) #blowfish 5

        

        
    # def test_ad(self): 
    #     self.assertTrue(check_password('teste_senha_ad', 'teste_senha_ad'.encode('UTF-16-LE')))
    #     self.assertFalse(check_password('aaaaaaaaaaaaa', 'teste_senha_ad'.encode('UTF-16-LE')))
        
    def test_ntlm(self):
        self.assertFalse(check_password('teste_erro_md4','7cd4642b602a12a4c0aab055ea45edd3'))  #ntlm 1
        self.assertTrue(check_password('teste_senha_md4','7cd4642b602a12a4c0aab055ea45edd3')) #ntlm 3 checado
        self.assertTrue(check_md4('abcdefghijklmnopqrstuvwxyz','d79e1c308aa5bbcdeea8ed63df412da9')) #ntlm 4

        
    def test_generate_ntlm(self):
        p = generate_password('teste_senha_md4', type_password=password.TYPE_NTLM_PASSWORD)    
        self.assertEqual(p,'7cd4642b602a12a4c0aab055ea45edd3')

    def test_generate_ad(self):    
        p = generate_password('1234', type_password=password.TYPE_ACTIVE_DIRECTORY_PASSWORD) 
        self.assertEqual(p,'"1234"'.encode('utf-16-le'))
    
    def test_generate_md5(self):
        p = generate_password('teste_senha_md5', type_password=password.TYPE_MD5_PASSWORD)
        self.assertNotEqual(p,'teste_senha_md5')
        self.assertEqual(p,'{MD5}fab90b086e400fbe5850962e9b41e959')

    def test_generate_sha1(self):
        p = generate_password('teste_sha1', type_password=password.TYPE_SHA_PASSWORD)
        self.assertNotEqual(p,'teste_sha1')
        self.assertEqual(p,'{SHA}fc9c94e31a80bf223a35b5432ac333d2ad02f37c')

    def test_generate_sha256(self):    
        p = generate_password('teste_sha256', type_password=password.TYPE_SHA256_PASSWORD)
        self.assertNotEqual(p,'teste_sha256')
        self.assertEqual(p,'{SHA256}bffa416bb7c30ad81ebd0b08f17442bcaed8d81db58c35a599c1373f60c609e4')

    def test_generate_ssha256(self):   
        p = generate_password('teste_ssha', type_password=password.TYPE_SSHA_PASSWORD)
        self.assertNotEqual(p,'1234')
        #ps = generate_password('teste_ssha', type_password=password.TYPE_SSHA_PASSWORD, salt=binascii.a2b_hex(b'd1cc0883b5f6fa42'))
        ps = generate_password('teste_ssha', type_password=password.TYPE_SSHA_PASSWORD, salt=binascii.a2b_hex('d1cc0883b5f6fa42'))
        self.assertEqual(ps,'{SSHA}xHdM7MBzP/BIGCiqZs7ZPF91PwTRzAiDtfb6Qg==')    

    def test_generate_blowfish(self):   
        pass_bf = generate_password('1234', type_password=password.TYPE_BLOWFISH_PASSWORD)
        print(pass_bf)
        self.assertTrue(check_password('1234', pass_bf))
       
        
        
        
if __name__ == "__main__":
    unittest.main()
    
def main():
    unittest.main()
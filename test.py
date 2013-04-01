# encoding: utf-8

import unittest
from main import encrypt, decrypt, encrypt_fp


class DESTestCase(unittest.TestCase):
    def setUp(self):
        self.key = '\x01\x23\x34\x56\x78\x9a\xbc\xde'
        self.cipher = 'L\x9c\x19\r\xf7y\xdc7S\xd5T=\x9a(\x9a\xde\x18\xe0\xd7\x0e!\x9dbnN\x9f\xa6e\xbf\xb7^\x93'
        self.plaintext = 'panzerkampfwagen tiger ii'


    def test_encrypt(self):
        cipher = encrypt(self.key, self.plaintext)
        self.assertEqual(cipher, self.cipher)


    def test_decrypt(self):
        plaintext = decrypt(self.key, self.cipher)
        self.assertEqual(plaintext, self.plaintext)



if __name__ == '__main__':
    unittest.main()


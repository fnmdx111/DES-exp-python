# encoding: utf-8
import StringIO

from libs.des import feistel_s, feistel_ba
from libs.keyschedule import key_schedule_s, key_schedule_ba
from libs.misc import len_fp, pre_process_raw, key_pre_process_func, padding


def encrypt_fp(secret_key, plaintext_fp, cipher_fp):
    key = pre_process_raw(secret_key,
                          func=key_pre_process_func)
    keys = key_schedule_ba(key)

    length = len_fp(plaintext_fp)
    while True:
        block = plaintext_fp.read(8)
        pos = plaintext_fp.tell()
        block_len = len(block)
        if block_len < 8:
            block += padding(block_len)
            pos += 8 - block_len
        cipher_fp.write(feistel_ba(bytearray(block), keys))
        if pos > length:
            break

    return cipher_fp


def decrypt_fp(secret_key, cipher_fp, plaintext_fp):
    key = pre_process_raw(secret_key,
                          func=key_pre_process_func)
    keys = key_schedule_ba(key)[::-1]

    length = len_fp(cipher_fp)
    while True:
        block = cipher_fp.read(8)
        plaintext_block = feistel_ba(bytearray(block), keys)
        if cipher_fp.tell() == length:
            plaintext_block = plaintext_block[:-plaintext_block[-1]]
            plaintext_fp.write(plaintext_block)
            break

        plaintext_fp.write(plaintext_block)

    return plaintext_fp


def encrypt(secret_key, plaintext):
    cipher = encrypt_fp(secret_key, StringIO.StringIO(plaintext), StringIO.StringIO())
    cipher.seek(0)

    return cipher.read()


def decrypt(secret_key, cipher):
    plaintext = decrypt_fp(secret_key, StringIO.StringIO(cipher), StringIO.StringIO())
    plaintext.seek(0)

    return plaintext.read()



if __name__ == '__main__':
    print encrypt('\x01\x23\x34\x56\x78\x9a\xbc\xde', 'panzerkampfwagen ii')
    print decrypt('\x01\x23\x34\x56\x78\x9a\xbc\xde', encrypt('\x01\x23\x34\x56\x78\x9a\xbc\xde', 'panzerkampfwagen ii'))
    pass



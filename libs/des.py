# encoding: utf-8

from libs.keyschedule import key_schedule_s
from libs.tables import expansion_table, sbox, b2i_d, i2b_d, sbox_perm_table, init_perm_table, inv_init_perm_table
from libs.misc import take, map_, xor_s, expand, sbox_perm, init_perm, inv_init_perm, xor_s_32, xor_s_48


def init_perm_b(plaintext):
    plaintext = ''.join(plaintext)
    plaintext = init_perm(plaintext)

    return plaintext[:32], plaintext[32:]


def f(r, k):
    e = expand(r)
    mid = xor_s_48(e, k)

    sbox_res = []
    for i in range(0, 48, 6):
        cur_sbox = sbox[i / 6]
        coord = (
            b2i_d[mid[i] + mid[i + 5]],
            b2i_d[mid[i + 1] + mid[i + 2] + mid[i + 3] + mid[i + 4]]
        )
        sbox_res.append(i2b_d[cur_sbox[coord[0]][coord[1]]])
    sbox_res = ''.join(sbox_res)

    return sbox_perm(sbox_res)


def inverse_init_perm_b(c):
    return inv_init_perm(c)


def feistel_s(plaintext_byte_s, keys_s):
    l, r = init_perm_b(plaintext_byte_s)

    l, r = r, xor_s_32(l, f(r, keys_s[0]))
    l, r = r, xor_s_32(l, f(r, keys_s[1]))
    l, r = r, xor_s_32(l, f(r, keys_s[2]))
    l, r = r, xor_s_32(l, f(r, keys_s[3]))
    l, r = r, xor_s_32(l, f(r, keys_s[4]))
    l, r = r, xor_s_32(l, f(r, keys_s[5]))
    l, r = r, xor_s_32(l, f(r, keys_s[6]))
    l, r = r, xor_s_32(l, f(r, keys_s[7]))
    l, r = r, xor_s_32(l, f(r, keys_s[8]))
    l, r = r, xor_s_32(l, f(r, keys_s[9]))
    l, r = r, xor_s_32(l, f(r, keys_s[10]))
    l, r = r, xor_s_32(l, f(r, keys_s[11]))
    l, r = r, xor_s_32(l, f(r, keys_s[12]))
    l, r = r, xor_s_32(l, f(r, keys_s[13]))
    l, r = r, xor_s_32(l, f(r, keys_s[14]))
    l, r = r, xor_s_32(l, f(r, keys_s[15]))
    l, r = r, l

    return map(lambda bits: ''.join(bits), take(inverse_init_perm_b(l + r)))


def encrypt_s(plaintext, key):
    keys = key_schedule_s(key)

    return feistel_s(plaintext, keys)


def decrypt_s(cipher, keys):
    return feistel_s(cipher, keys)



if __name__ == '__main__':
    plaintext = ['00110000', '00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111']
    key = ['00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000']

    assert plaintext == decrypt_s(encrypt_s(plaintext, key), key)

    print encrypt_s(plaintext, key)
    print decrypt_s(encrypt_s(plaintext, key), key)



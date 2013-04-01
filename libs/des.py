# encoding: utf-8

from libs.keyschedule import key_schedule_s, key_schedule_ba
from libs.tables import expansion_table, sbox, b2i_d, i2b_d, sbox_perm_table, init_perm_table, inv_init_perm_table
from libs.misc import take, map_, xor_s, map_ba, xor_ba, idx_ba


def init_perm_b(plaintext):
    plaintext = ''.join(plaintext)
    plaintext = map_(plaintext, table=init_perm_table)

    return plaintext[:32], plaintext[32:]


def init_perm_ba(plaintext):
    plaintext = map_ba(plaintext, init_perm_table)
    return plaintext[:4], plaintext[4:]


def f_s(r, k):
    e = map_(r, table=expansion_table)
    mid = xor_s(e, k)

    sbox_res = []
    for i in range(0, 48, 6):
        cur_sbox = sbox[i / 6]
        coord = (
            b2i_d[mid[i] + mid[i + 5]],
            b2i_d[mid[i + 1] + mid[i + 2] + mid[i + 3] + mid[i + 4]]
        )
        sbox_res.append(i2b_d[cur_sbox[coord[0]][coord[1]]])
    sbox_res = ''.join(sbox_res)

    return map_(sbox_res, table=sbox_perm_table)


def f_ba(r, k):
    e = map_ba(r, expansion_table, size=6)
    mid = xor_ba(e, k)

    ret = bytearray(4)
    for i in range(0, 48, 6):
        n = i / 6
        cur_sbox = sbox[n]
        coord = (
            idx_ba(i, mid) << 1 | idx_ba(i + 5, mid),
            idx_ba(i + 1, mid) << 3 | idx_ba(i + 2, mid) << 2 | idx_ba(i + 3, mid) << 2 | idx_ba(i + 4, mid)
        )
        sbox_ret = cur_sbox[coord[0]][coord[1]]
        if not n % 2:
            ret[n / 2] = sbox_ret << 4
        else:
            ret[n / 2] |= sbox_ret

    return map_ba(ret, sbox_perm_table)


def inverse_init_perm_b(c):
    return map_(c, table=inv_init_perm_table)


def inverse_init_perm_ba(c):
    return map_ba(c, inv_init_perm_table)


def feistel_s(plaintext_byte_s, keys_s):
    l, r = init_perm_b(plaintext_byte_s)

    for i in range(16):
        l, r = r, xor_s(l, f_s(r, keys_s[i]))
    l, r = r, l

    return map(lambda bits: ''.join(bits), take(inverse_init_perm_b(l + r)))


def feistel_ba(plaintext_ba, keys_ba):
    l, r = init_perm_ba(plaintext_ba)
    for i in range(16):
        l, r = r, xor_ba(l, f_ba(r, keys_ba[i]))
    l, r = r, l
    l.extend(r)

    return inverse_init_perm_ba(l)


def encrypt_s(plaintext, key):
    keys = key_schedule_s(key)

    return feistel_s(plaintext, keys)


def encrypt_ba(plaintext, key):
    keys = key_schedule_ba(key)

    return feistel_ba(plaintext, keys)


def decrypt_s(cipher, key):
    keys = key_schedule_s(key)[::-1]

    return feistel_s(cipher, keys)


def decrypt_ba(cipher, key):
    keys = key_schedule_ba(key)[::-1]

    return feistel_ba(cipher, keys)



if __name__ == '__main__':
    def process(sa):
        return bytearray(map(lambda x: int(x, base=2), sa))


    plaintext = ['00110000', '00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111']
    plaintext_ba = process(plaintext)
    key = ['00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000']

    assert plaintext == decrypt_s(encrypt_s(plaintext, key), key)

    print encrypt_s(plaintext, key)
    print decrypt_s(encrypt_s(plaintext, key), key)

    assert plaintext_ba == decrypt_ba(encrypt_ba(plaintext_ba, key), key)



import os
import operator
from libs.tables import init_perm_table


def take(it, by=8):
    """
    >>> list(take(range(16), by=5))
    [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15]]
    """
    while it:
        if len(it) > by:
            s = by
        else:
            s = len(it)
        yield it[:s]
        it = it[s:]


def xor_ba(x, y):
    """
    >>> xor_ba(bytearray([0b11100100]), bytearray([0b10010001]))
    bytearray(b'u')
    """
    return bytearray(map(operator.xor, x, y))


def map_(src, table):
    """
    >>> ''.join(map_('0011000000110001001100100011001100110100001101010011011000110111', table=init_perm_table))
    '0000000011111111111100001010101000000000111111110000000011001100'
    """

    return map(lambda i: src[i - 1], table)


def _bitwise_op(dba, sba, di, si):
    si_mod_8 = (7 - si) % 8
    di_mod_8 = (7 - di) % 8
    bit = sba[si / 8] & (1 << si_mod_8)
    if si_mod_8 > di_mod_8:
        bit >>= si_mod_8 - di_mod_8
    else:
        bit <<= di_mod_8 - si_mod_8

    dba[di / 8] |= bit


def map_ba(src, table, size=None):
    ret = bytearray(len(src) if not size else size)
    [_bitwise_op(ret, src, i, j - 1) for i, j in enumerate(table)]

    return ret


def idx_ba(idx, array):
    """
    >>> idx_ba(5, bytearray([0b10111001]))
    0
    >>> idx_ba(3, bytearray([0b10010001]))
    1
    """
    shift = (7 - idx) % 8
    return (array[idx / 8] & (1 << shift)) >> shift


def len_fp(fp):
    fp.seek(0, os.SEEK_END)
    length = fp.tell()
    fp.seek(0)

    return length


key_pre_process_func = lambda x: ord(x) << 1 & 0xff


def pre_process_raw(raw, func=ord):
    """
    >>> pre_process_raw('abcdefgh', func=key_pre_process_func)
    ['11000010', '11000100', '11000110', '11001000', '11001010', '11001100', '11001110', '11010000']
    >>> pre_process_raw('\x01\x23\x34\x56\x78\x9a\xbc\xde', func=key_pre_process_func)
    ['00000010', '01000110', '01101000', '10101100', '11110000', '00110100', '01111000', '10111100']
    """
    return ['{0:08b}'.format(func(i)) for i in raw]


def padding(size):
    """
    >>> padding(0)
    '\\x08\\x08\\x08\\x08\\x08\\x08\\x08\\x08'
    >>> padding(3)
    '\\x05\\x05\\x05\\x05\\x05'
    """
    pad_size = 8 - size % 8
    return chr(pad_size) * (pad_size if pad_size else 8)



if __name__ == '__main__':
    ba = bytearray([0b00110000, 0b00110001, 0b00110010, 0b00110011, 0b00110100, 0b00110101, 0b00110110, 0b00110111])
    map_ba(ba, init_perm_table)


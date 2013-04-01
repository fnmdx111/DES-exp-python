import os
from tables import xor_s_d, init_perm_table


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


def xor_s(x, y):
    """
    >>> xor_s('11100100', '10010001')
    ['0', '1', '1', '1', '0', '1', '0', '1']
    """
    return [xor_s_d[i, j] for i, j in zip(x, y)]


def map_(src, table):
    """
    >>> ''.join(map_('0011000000110001001100100011001100110100001101010011011000110111', table=init_perm_table))
    '0000000011111111111100001010101000000000111111110000000011001100'
    """

    return map(lambda i: src[i - 1], table)


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
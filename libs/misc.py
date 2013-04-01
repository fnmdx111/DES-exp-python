from itertools import izip
import os
from libs.tables import xor_s_d, init_perm_table


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


def expand(x):
    return [x[31], x[0], x[1], x[2], x[3], x[4], x[3], x[4],
            x[5], x[6], x[7], x[8], x[7], x[8], x[9], x[10],
            x[11], x[12], x[11], x[12], x[13], x[14], x[15], x[16],
            x[15], x[16], x[17], x[18], x[19], x[20], x[19], x[20],
            x[21], x[22], x[23], x[24], x[23], x[24], x[25], x[26],
            x[27], x[28], x[27], x[28], x[29], x[30], x[31], x[0]]


def sbox_perm(x):
    return [x[15], x[6], x[19], x[20], x[28], x[11], x[27], x[16],
            x[0], x[14], x[22], x[25], x[4], x[17], x[30], x[9],
            x[1], x[7], x[23], x[13], x[31], x[26], x[2], x[8],
            x[18], x[12], x[29], x[5], x[21], x[10], x[3], x[24]]


def init_perm(x):
    return [x[57], x[49], x[41], x[33], x[25], x[17], x[9], x[1],
            x[59], x[51], x[43], x[35], x[27], x[19], x[11], x[3],
            x[61], x[53], x[45], x[37], x[29], x[21], x[13], x[5],
            x[63], x[55], x[47], x[39], x[31], x[23], x[15], x[7],
            x[56], x[48], x[40], x[32], x[24], x[16], x[8], x[0],
            x[58], x[50], x[42], x[34], x[26], x[18], x[10], x[2],
            x[60], x[52], x[44], x[36], x[28], x[20], x[12], x[4],
            x[62], x[54], x[46], x[38], x[30], x[22], x[14], x[6]]


def inv_init_perm(x):
    return [x[39], x[7], x[47], x[15], x[55], x[23], x[63], x[31],
            x[38], x[6], x[46], x[14], x[54], x[22], x[62], x[30],
            x[37], x[5], x[45], x[13], x[53], x[21], x[61], x[29],
            x[36], x[4], x[44], x[12], x[52], x[20], x[60], x[28],
            x[35], x[3], x[43], x[11], x[51], x[19], x[59], x[27],
            x[34], x[2], x[42], x[10], x[50], x[18], x[58], x[26],
            x[33], x[1], x[41], x[9], x[49], x[17], x[57], x[25],
            x[32], x[0], x[40], x[8], x[48], x[16], x[56], x[24]]


def xor_s(x, y):
    """
    >>> xor_s('11100100', '10010001')
    ['0', '1', '1', '1', '0', '1', '0', '1']
    """
    return [xor_s_d[i, j] for i, j in izip(x, y)]


def xor_s_16(x, y):
    return [xor_s_d[x[0], y[0]], xor_s_d[x[1], y[1]], xor_s_d[x[2], y[2]], xor_s_d[x[3], y[3]],
            xor_s_d[x[4], y[4]], xor_s_d[x[5], y[5]], xor_s_d[x[6], y[6]], xor_s_d[x[7], y[7]],
            xor_s_d[x[8], y[8]], xor_s_d[x[9], y[9]], xor_s_d[x[10], y[10]], xor_s_d[x[11], y[11]],
            xor_s_d[x[12], y[12]], xor_s_d[x[13], y[13]], xor_s_d[x[14], y[14]], xor_s_d[x[15], y[15]]]


def xor_s_32(x, y):
    ret = xor_s_16(x[:16], y[:16])
    ret.extend(xor_s_16(x[16:], y[16:]))
    return ret


def xor_s_48(x, y):
    ret = xor_s_16(x[:16], y[:16])
    ret.extend(xor_s_16(x[16:32], y[16:32]))
    ret.extend(xor_s_16(x[32:], y[32:]))
    return ret


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
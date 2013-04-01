# encoding: utf-8
from libs.misc import map_, take


perm2_table = [14, 17, 11, 24, 1, 5, 3, 28,
               15, 6, 21, 10, 23, 19, 12, 4,
               26, 8, 16, 7, 27, 20, 13, 2,
               41, 52, 31, 37, 47, 55, 30, 40,
               51, 45, 33, 48, 44, 49, 39, 56,
               34, 53, 46, 42, 50, 36, 29, 32]


def rotate_left(x, n):
    mask = reduce(lambda acc, i: (acc << 1) | i,
                  map(int, '1' * n + '0' * (28 - n)),
                  0)
    return 0xfffffff & (x << n) | (mask & x) >> (28 - n)


rot1 = lambda x: 0xfffffff & (x << 1) | (x & 0x8000000) >> 27
rot2 = lambda x: 0xfffffff & (x << 2) | (x & 0xc000000) >> 26
rotate_table = [rot1] * 2 + [rot2] * 6 + [rot1] + [rot2] * 6 + [rot1]


rot1_s = lambda x: x[1:] + x[0]
rot2_s = lambda x: x[2:] + x[:2]
rotate_table_s = [rot1_s] * 2 + [rot2_s] * 6 + [rot1_s] + [rot2_s] * 6 + [rot1_s]


def perm1_s(key):
    """
    >>> perm1_s(['00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000'])
    ('0000000000000000111111111111', '0110011001111000100000001111')
    """
    transposed = map(lambda *_: ''.join(_[::-1]), *key)[:-1]

    return (
        ''.join(transposed[:3] + [transposed[3][:4]]),
        ''.join(transposed[:3:-1] + [transposed[3][4:]])
    )


def perm2_s(k):
    """
    >>> perm2_s('00000000000000011111111111101100110011110001000000011110')
    '010100000010110010101100010101110010101011000010'
    """
    return ''.join(map_(k, table=perm2_table))


def key_schedule_s(key):
    c, d = perm1_s(key)

    keys = []
    for i in range(16):
        rot_f = rotate_table_s[i]
        c = rot_f(c)
        d = rot_f(d)

        keys.append(perm2_s(c + d))

    return keys


def key_schedule_ba(key):
    c, d = perm1_s(key)

    keys = []
    for i in range(16):
        rot_f = rotate_table_s[i]
        c = rot_f(c)
        d = rot_f(d)

        keys.append(bytearray(map(lambda i: int(i, base=2), take(perm2_s(c + d)))))

    return keys



if __name__ == '__main__':
    keys = key_schedule_ba(['00110001', '00110010', '00110011', '00110100',
                          '00110101', '00110110', '00110111', '00111000'])
    for key in keys:
        for i in key:
            print '{0:08b}'.format(i),
        print


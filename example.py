import cProfile
import profile
import pstats
from main import encrypt_fp, decrypt_fp


key = '\x01\x23\x34\x56\x78\x9a\xbc\xde'


def test():
    return encrypt_fp(key,
                      open('d:/tddownload/motherboard_driver_ahci_amd_sb7xx_bootdisk_win7-64bit.exe', 'rb'),
                      open('d:/tddownload/motherboard_driver_ahci_amd_sb7xx_bootdisk_win7-64bit.des', 'wb'))


profile.run('test()', 'encrypt_prof_ix')


def test_():
    return decrypt_fp(key,
                      open('d:/tddownload/motherboard_driver_ahci_amd_sb7xx_bootdisk_win7-64bit.des', 'rb'),
                      open('d:/tddownload/motherboard_driver_ahci_amd_sb7xx_bootdisk_win7-64bit1.exe', 'wb'))


# cProfile.run('test_()', 'decrypt_prof')

pstats.Stats('encrypt_prof').strip_dirs().sort_stats('calls').print_stats()
# pstats.Stats('decrypt_prof').strip_dirs().sort_stats('calls').print_stats()


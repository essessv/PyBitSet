# For ASCII codes, refer http://www.ascii-code.com/
from unittest import TestCase
from nose.tools import raises
from functools import wraps

from pybitset.pybitset import BitSet


class TestPyBitSet(TestCase):

    test_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result_string = "ABCDEFGHIJKLMNOPqRSTUVWXYZ"

    def setup_bitset(initString=test_string):
        def outer(func):
            @wraps(func)
            def inner(instance):
                b = BitSet(len(initString) * 8)
                # ugly mangling to get set the "private" member.
                b._BitSet__bitset = bytearray(initString)
                func(instance, b)
            return inner
        return outer

    def change_bitset(self, b, string):
        _byte_size = len(string)
        _bit_size = len(string) * 8
        b._BitSet__bitset = bytearray(string)
        b._BitSet__byte_size = _byte_size
        b._BitSet__bit_size = _bit_size
        return b

    @raises(TypeError, ValueError)
    def test_bitset_is_set_invalid(self):
        BitSet(-1)
        BitSet(0)
        BitSet(None)
        BitSet("some string")
        BitSet(list())
        BitSet(set())

    def test_bitset_valid_initialization(self):
        b = BitSet(255)
        assert b.size() == 255
        bs = b.bitset_as_string()
        # ugly mangling to get to byte_size and not recalculate
        assert bs == (chr(0) * b._BitSet__byte_size)

    @raises(ValueError)
    def test_bitset_set_out_of_bounds(self):
        b = BitSet(1)
        b.bitset_set(2)

    @raises(ValueError)
    def test_bitset_unset_out_of_bounds(self):
        b = BitSet(1)
        b.bitset_unset(2)

    def test_bitset_set_unset_and_if_bitset_set(self):
        b = BitSet(8)
        b.bitset_set(1)
        b.bitset_set(7)
        assert b.bitset_as_string() == 'A'
        b.bitset_set(6)
        assert b.bitset_as_string() == 'C'

        assert b.bitset_is_set(6) is True
        b.bitset_unset(6)
        assert b.bitset_as_string() == 'A'

        assert b.bitset_is_set(6) is False
        assert b.bitset_is_set(2) is False

    @setup_bitset(test_string)
    def test_bitset_set_unset_and_if_bitset_set_large_bitset(self, b):
        b.bitset_set(130)
        assert b.bitset_as_string() == self.result_string

        assert b.bitset_is_set(201) is True
        assert b.bitset_is_set(200) is False

    @setup_bitset(test_string)
    def test_bitset_count_set_bits(self, b):
        assert b.bitset_count_set_bits() == 86
        b.bitset_set(130)
        assert b.bitset_count_set_bits() == 87

    @setup_bitset("0" * 8192)
    def test_bitset_count_set_bits_large_bitset(self, b):
        assert b.bitset_count_set_bits() == 16384

    def test_bitset_count_unset_bits(self):
        b = BitSet(65535)
        b.bitset_set(1000)
        assert b.bitset_count_set_bits() == 1
        assert b.bitset_count_unset_bits() == 65534
        b.bitset_set_range(start=65000, end=65100)
        assert b.bitset_count_set_bits() == 102
        assert b.bitset_count_unset_bits() == 65433

    @setup_bitset("0" * 8192)
    def test_bitset_count_unset_bits_large_bitset(self, b):
        assert b.bitset_count_unset_bits() == 49152

    @setup_bitset(chr(251) + chr(251) + chr(251))
    def test_bitset_find_unset_bit(self, b):
        assert b.bitset_find_unset_bit() == 5
        assert self.change_bitset(
            b, chr(255) + chr(251) + chr(251)).bitset_find_unset_bit() == 13
        assert self.change_bitset(
            b, chr(255) + chr(255) + chr(251)).bitset_find_unset_bit() == 21
        assert self.change_bitset(
            b, chr(255) + chr(255) + chr(255)).bitset_find_unset_bit() == -1

    @setup_bitset(chr(251) + chr(251) + chr(251))
    def test_bitset_find_unset_bit_range(self, b):
        assert b.bitset_find_unset_bit(start=9, end=None) == 13
        assert self.change_bitset(
            b, chr(255) + chr(251) + chr(251)).bitset_find_unset_bit(
            end=13) == 13
        assert self.change_bitset(
            b, chr(255) + chr(255) + chr(255)).bitset_find_unset_bit(
            start=-1, end=30) == -1

    @setup_bitset("A")
    def test_bitset_set_range_true(self, b):
        b.bitset_set_range()
        assert b.bitset_as_string() == chr(255)

        b = self.change_bitset(b, "ABC")
        b.bitset_set_range()
        assert b.bitset_as_string() == chr(255) + chr(255) + chr(255)

        b = self.change_bitset(b, chr(000))
        b.bitset_set_range(start=2, end=5)
        assert b.bitset_as_string() == chr(074)

        b = self.change_bitset(b, self.test_string)
        b.bitset_set_range(start=122, end=130)
        assert b.bitset_as_string() == 'ABCDEFGHIJKLMNO\x7f\xf1RSTUVWXYZ'

    @setup_bitset("A")
    def test_bitset_set_range_false(self, b):
        b.bitset_set_range(value=False)
        assert b.bitset_as_string() == chr(0)

        b = self.change_bitset(b, "ABC")
        b.bitset_set_range(value=False)
        assert b.bitset_as_string() == chr(0) + chr(0) + chr(0)

        b = self.change_bitset(b, chr(000))
        b.bitset_set_range(start=2, end=5, value=False)
        assert b.bitset_as_string() == chr(0)

        b = self.change_bitset(b, self.test_string)
        b.bitset_set_range(start=122, end=130, value=False)
        assert b.bitset_as_string() == 'ABCDEFGHIJKLMNO@\x11RSTUVWXYZ'

    @setup_bitset("A")
    def test_bitset_set_range_invalid_range(self, b):
        with self.assertRaises(ValueError):
            b.bitset_set_range(start=6, end=5)
        with self.assertRaises(ValueError):
            b.bitset_set_range(start=-1, end=-1)
        with self.assertRaises(ValueError):
            b.bitset_set_range(start=10, end=10)

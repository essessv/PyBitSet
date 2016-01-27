"""
A simple BitSet library to manage a python string as a bitset.
"""

from math import ceil


class BitSet(object):
    """
    A simple BitSet class library that allows users to create and manage
    bitsets.
    """

    __bit_size = None
    __byte_size = None
    __bitset = None

    def __init__(self, bits):
        """
        Constructs an object of type BitSet.

        Args:
            bits: number of bits this BitSet manages.

        Returns:
            An object of type BitSet

        Raises:
            TypeError: passed argument bits is not of type int.
            ValueError: passed argument bits is negative or zero.
        """

        if not isinstance(bits, int):
            raise TypeError("passed argument 'bits' is not of type int")
        if bits <= 0:
            raise ValueError("passed bits is negative or zero")
        self.__byte_size = int(ceil(float(bits) / 8))
        self.__bit_size = bits
        self.__bitset = bytearray(chr(0) * self.__byte_size)

    def size(self):
        """
        Returns the size of the BitSet, i.e. the current number of bits.
        """
        return self.__bit_size

    def bitset_as_string(self):
        """
        Returns the string representation of the bitset.
        """
        return str(self.__bitset)

    def _validate_offset(self, offset=None):
        if offset is not None and not isinstance(offset, int):
            raise TypeError("Passed offset %s is not an int" % offset)
        if offset is not None and offset < 0 or offset > self.__bit_size:
            raise ValueError("offset %s is out of bounds" % offset)

    def bitset_is_set(self, offset):
        """
        Checks if a given bit is set to 1.

        Args:
            offset: the bit at the offset in the BitSet to check.

        Returns:
            True if set to 1, False if set to 0.
        """
        self._validate_offset(offset)
        byte, bit = divmod(offset, 8)
        return bool((128 >> bit) & self.__bitset[byte])

    def bitset_set(self, offset):
        """
        Sets the offset bit in the BitSet to 1.

        Args:
            offset: the offset in the BitSet at
                    which the bit has to be set to 1.

        Returns:
            None
        """
        self._validate_offset(offset)
        byte, bit = divmod(offset, 8)
        self.__bitset[byte] = self.__bitset[byte] | (128 >> bit)

    def bitset_unset(self, offset):
        """
        Sets the offset bit in the BitSet to 0.

        Args:
            offset: the offset in the BitSet at
                    which the bit has to be set to 0.

        Returns:
            None
        """
        self._validate_offset(offset)
        byte, bit = divmod(offset, 8)
        self.__bitset[byte] = self.__bitset[byte] & ~(128 >> bit)

    def __bitset_count_set_bits(self):
        count = 0
        for i in self.__bitset:
            count += bin(i).count("1")
        return count

    def bitset_count_set_bits(self):
        """
        Counts the number of bits that are set to 1 in the BitSet.

        Returns:
            An int that equals the number of bits set to 1.
        """
        return self.__bitset_count_set_bits()

    def bitset_count_unset_bits(self):
        """
        Counts the number of bits that are set to 0 in BitSet.

        Returns:
            An int that equals the number of bits set to 0.
        """
        return self.__bit_size - self.__bitset_count_set_bits()

    def __find_first_unset_bit_in_byte(self, byte, start, end):
        for idx in range(start, end + 1):
            if byte & (128 >> idx):
                continue
            else:
                return idx
        return -1

    def bitset_find_unset_bit(self, start=None, end=None):
        """
        Finds an unset bit in a given range.

        Args:
            start: start offset in the range
            end: end offset in the range

        Returns:
            Index of the first unset bit in the BitSet in the
            range ['start', 'end'].

            -1 if there is no bit set to 0.
        """
        if start is None or start < 0:
            start = 0
        if end is None or end <= 0 or end >= len(self.__bitset) * 8:
            end = self.__bit_size - 1

        start_byte, start_bit = divmod(start, 8)
        end_byte, end_bit = divmod(end, 8)

        unset_bit = self.__find_first_unset_bit_in_byte(
            self.__bitset[start_byte], start_bit, 7)
        if unset_bit >= 0 and start_byte >= 0:
            return start_byte * 8 + unset_bit

        for idx, val in enumerate(self.__bitset[start_byte + 1:end_byte]):
            unset_bit = self.__find_first_unset_bit_in_byte(val, 0, 7)
            if unset_bit >= 0:
                return (start_byte + idx + 1) * 8 + unset_bit

        unset_bit = self.__find_first_unset_bit_in_byte(
            self.__bitset[end_byte], 0, end_bit)
        if unset_bit >= 0:
            return end_byte * 8 + unset_bit
        return -1

    def bitset_set_range(self, start=None, end=None, value=True):
        """
        Sets bits from 'start' to 'end' to 1 if value=True.
        Sets bits from 'start' to 'end' to 0 if value=False.

        Args:
            start: start offset in the range
            end: end offset in the range
            value: boolean, bit is set if True, unset if False

        Returns:
            None
        """
        if start is None:
            start = 0
        if end is None:
            end = self.__bit_size - 1

        if value is not True and value is not False:
            raise TypeError("passed value has to be either True or False")

        if start > end:
            raise ValueError(
                "start %s cannot be greater than end %s" % (start, end))
        if start < 0 or end < 0:
            raise ValueError("start and end cannot be negative")
        if start > self.__bit_size or end > self.__bit_size:
            raise ValueError(
                "start and/or end cannot be greater than size of the bitset")

        start_byte, start_bit = divmod(start, 8)
        end_byte, end_bit = divmod(end, 8)

        if start_byte == end_byte:
            for bit in xrange(start_bit, end_bit + 1):
                if value:
                    self.__bitset[start_byte] = self.__bitset[
                        start_byte] | (128 >> bit)
                else:
                    self.__bitset[start_byte] = self.__bitset[
                        start_byte] & ~(128 >> bit)
        else:
            # set start byte bits and end byte bits
            for bit in xrange(start_bit, 8):
                if value:
                    self.__bitset[start_byte] = self.__bitset[
                        start_byte] | (128 >> bit)
                else:
                    self.__bitset[start_byte] = self.__bitset[
                        start_byte] & ~(128 >> bit)

            for bit in xrange(0, end_bit + 1):
                if value:
                    self.__bitset[end_byte] = self.__bitset[
                        end_byte] | (128 >> bit)
                else:
                    self.__bitset[end_byte] = self.__bitset[
                        end_byte] & ~(128 >> bit)

            # now set all bytes between start_byte and end_byte
            for byte in xrange(start_byte + 1, end_byte):
                if value:
                    self.__bitset[byte] = chr(255)
                else:
                    self.__bitset[byte] = chr(0)

import pytest
from emulator import MyEmulator


class TestReplaceBit:
    @pytest.fixture
    def emulator(self):
        return MyEmulator()

    # Tests for 1-bit numbers
    def test_replace_bit_1bit_set(self, emulator):
        num = 0b1  # Binary: 0 (0 in decimal)
        loc = 0  # Set bit at position 0 (rightmost)
        val = 1  # Set to 1
        result = emulator.__replace_bit__(num, loc, val)
        assert result == 0b1  

    def test_replace_bit_1bit_clear(self, emulator):
        num = 0b1  # Binary: 1 (1 in decimal)
        loc = 0  # Clear bit at position 0 (rightmost)
        val = 0  # Set to 0
        result = emulator.__replace_bit__(num, loc, val)
        assert result == 0b0 

    # Tests for 2-bit numbers
    def test_replace_bit_2bits_set(self, emulator):
        num = 0b01  # Binary: 01 (1 in decimal)
        loc = 1  # Set bit at position 1 (second bit from the right)
        val = 1  # Set to 1
        result = emulator.__replace_bit__(num, loc, val)
        assert result == 0b11  

    def test_replace_bit_2bits_clear(self, emulator):
        num = 0b11  # Binary: 11 (3 in decimal)
        loc = 1  # Clear bit at position 1 (second bit from the right)
        val = 0  # Set to 0
        result = emulator.__replace_bit__(num, loc, val)
        assert result == 0b01 

    # Tests for 3-bit numbers
    def test_replace_bit_3bits_set(self, emulator):
        num = 0b101  # Binary: 101 (5 in decimal)
        loc = 1  # Set bit at position 2 (third bit from the right)
        val = 1  # Set to 1
        result = emulator.__replace_bit__(num, loc, val)
        assert result == 0b111  

    def test_replace_bit_3bits_clear(self, emulator):
        num = 0b111  # Binary: 111 (7 in decimal)
        loc = 2  # Clear bit at position 2 (leftmost)
        val = 0  # Set to 0
        result = emulator.__replace_bit__(num, loc, val)
        assert result == 0b011  


class TestReplaceBits:
    @pytest.fixture
    def emulator(self):
        return MyEmulator()

    # Tests for 1-bit numbers
    def test_replace_bits_1bit_set(self, emulator):
        num = 0b0  # Binary: 0 (0 in decimal)
        locs = [0]  # Set bit at position 0
        vals = [1]  # Set to 1
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b1 

    def test_replace_bits_1bit_clear(self, emulator):
        num = 0b1  # Binary: 1 (1 in decimal)
        locs = [0]  # Clear bit at position 0
        vals = [0]  # Set to 0
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b0  

    # Tests for 2-bit numbers
    def test_replace_bits_2bits_set(self, emulator):
        num = 0b00  # Binary: 00 (0 in decimal)
        locs = [0, 1]  # Set bits at positions 0 and 1
        vals = [0, 1]  # Set both bits to 1
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b10 

    # Tests for 2-bit numbers
    def test_replace_bits_2bits_reverse(self, emulator):
        num = 0b00  # Binary: 00 (0 in decimal)
        locs = [0, 1]  # Set bits at positions 0 and 1
        vals = [1, 0]  # Set both bits to 1
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b01  

    def test_replace_bits_2bits_clear(self, emulator):
        num = 0b11  # Binary: 11 (3 in decimal)
        locs = [0, 1]  # Clear bits at positions 0 and 1
        vals = [0, 0]  # Set both bits to 0
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b00

    def test_replace_bits_2bits_set_reverse(self, emulator):
        num = 0b10  # Binary: 10 (2 in decimal)
        locs = [0, 1]  # Set bits at positions 0 and 1
        vals = [1, 1]  # Set both bits to 1
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b11  

    # Tests for 3-bit numbers
    def test_replace_bits_3bits_set(self, emulator):
        num = 0b000  # Binary: 000 (0 in decimal)
        locs = [0, 1, 2]  # Set bits at positions 0, 1, and 2
        vals = [1, 1, 1]  # Set all bits to 1
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b111  

    def test_replace_bits_3bits_clear(self, emulator):
        num = 0b111  # Binary: 111 (7 in decimal)
        locs = [0, 1, 2]  # Clear bits at positions 0, 1, and 2
        vals = [0, 0, 0]  # Set all bits to 0
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b000  

    def test_replace_bits_3bits_mixed(self, emulator):
        num = 0b101  # Binary: 101 (5 in decimal)
        locs = [0, 1, 2]  # Set bits at positions 0, 1, and 2
        vals = [1, 0, 1]  # Set first and third bits to 1, second to 0
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b101  

    def test_replace_bits_3bits_partial_set(self, emulator):
        num = 0b100  # Binary: 100 (4 in decimal)
        locs = [1, 2]  # Set bits at positions 1 and 2
        vals = [1, 0]  # Set second bit to 1 and third bit to 0
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b010  

    def test_replace_bits_3bits_flip(self, emulator):
        num = 0b110  # Binary: 110 (6 in decimal)
        locs = [0, 2]  # Set bits at positions 1 and 2
        vals = [1, 0]  # Flip second bit to 0, third bit to 1
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == 0b011  

    def test_replace_bits_3bits_empty(self, emulator):
        num = 0b110  # Binary: 110 (6 in decimal)
        locs = []  # No bits to modify
        vals = []  # No values to set
        result = emulator.__replace_bits__(num, locs, vals)
        assert result == num  # Nothing changes

    # Edge case: more locs than vals (should raise assertion error)
    def test_replace_bits_more_locs_than_vals(self, emulator):
        num = 0b111  # Binary: 111 (7 in decimal)
        locs = [0, 1, 2]  # Three positions
        vals = [1, 0]  # Only two values
        with pytest.raises(AssertionError):
            emulator.__replace_bits__(num, locs, vals)

    # Edge case: more vals than locs (should raise assertion error)
    def test_replace_bits_more_vals_than_locs(self, emulator):
        num = 0b111  # Binary: 111 (7 in decimal)
        locs = [0, 1]  # Two positions
        vals = [1, 0, 1]  # Three values
        with pytest.raises(AssertionError):
            emulator.__replace_bits__(num, locs, vals)
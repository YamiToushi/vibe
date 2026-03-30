import unittest
from bin2dec.validator import validate_binary_input
from bin2dec.converter import convert_binary_to_decimal

class TestBinaryValidator(unittest.TestCase):
    def test_valid_binary_strings(self):
        """Test that valid 8-digit binary strings are accepted"""
        valid_inputs = ["00000000", "11111111", "10101010", "01010101"]
        for input_str in valid_inputs:
            with self.subTest(input_str=input_str):
                self.assertTrue(validate_binary_input(input_str))
    
    def test_invalid_length(self):
        """Test that strings with incorrect length are rejected"""
        invalid_inputs = ["1010101", "101010101", "101", ""]
        for input_str in invalid_inputs:
            with self.subTest(input_str=input_str):
                self.assertFalse(validate_binary_input(input_str))
    
    def test_invalid_characters(self):
        """Test that strings with non-binary characters are rejected"""
        invalid_inputs = ["10101012", "1010101a", "1010101 ", "1010101-"]
        for input_str in invalid_inputs:
            with self.subTest(input_str=input_str):
                self.assertFalse(validate_binary_input(input_str))

class TestBinaryConverter(unittest.TestCase):
    def test_convert_valid_binary(self):
        """Test conversion of valid binary strings to decimal"""
        test_cases = [
            ("00000000", 0),
            ("00000001", 1),
            ("00000010", 2),
            ("00000100", 4),
            ("00001000", 8),
            ("00010000", 16),
            ("00100000", 32),
            ("01000000", 64),
            ("10000000", 128),
            ("11111111", 255),
            ("10101010", 170),
            ("01010101", 85)
        ]
        
        for binary, expected in test_cases:
            with self.subTest(binary=binary):
                self.assertEqual(convert_binary_to_decimal(binary), expected)
    
    def test_convert_invalid_binary(self):
        """Test that conversion raises ValueError for invalid inputs"""
        invalid_inputs = ["1010101", "10101012", "1010101a", "1010101 "]
        for input_str in invalid_inputs:
            with self.subTest(input_str=input_str):
                with self.assertRaises(ValueError):
                    convert_binary_to_decimal(input_str)

if __name__ == '__main__':
    unittest.main()
"""
Binary to decimal conversion module.

This module provides functions to convert binary strings to decimal numbers.
"""

def convert_binary_to_decimal(binary_string: str) -> int:
    """
    Converts an 8-digit binary string to its decimal equivalent using manual calculation.
    
    Args:
        binary_string (str): 8-character binary string
        
    Returns:
        int: Decimal equivalent of the binary number
        
    Raises:
        ValueError: If the input is not a valid 8-character binary string
        
    Example:
        >>> convert_binary_to_decimal("11111111")
        255
        >>> convert_binary_to_decimal("10101010")
        170
    """
    # Validate input first
    if not isinstance(binary_string, str) or len(binary_string) != 8:
        raise ValueError("Input must be an 8-character string")
    
    for char in binary_string:
        if char not in ('0', '1'):
            raise ValueError("Input must contain only '0' and '1' characters")
    
    decimal_value = 0
    
    # Manual conversion using loop with 7-i exponent pattern
    for i in range(8):
        if binary_string[i] == '1':
            decimal_value += 2 ** (7 - i)
    
    return decimal_value
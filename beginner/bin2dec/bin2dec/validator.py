"""
Input validation module for binary string validation.

This module provides functions to validate binary strings for the bin2dec tool.
"""

def validate_binary_input(binary_string: str) -> bool:
    """
    Validates that the input is an 8-character string consisting only of '0' and '1' characters.
    
    Args:
        binary_string (str): The input string to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Example:
        >>> validate_binary_input("11110000")
        True
        >>> validate_binary_input("1111000")
        False
    """
    # Check if string has exactly 8 characters
    if len(binary_string) != 8:
        return False
    
    # Check if all characters are either '0' or '1'
    for char in binary_string:
        if char not in ('0', '1'):
            return False
    
    return True
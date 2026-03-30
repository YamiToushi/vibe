#!/usr/bin/env python3
"""
CLI tool for converting 8-digit binary strings to decimal numbers.

Usage: bin2dec 11110000

This tool converts an 8-digit binary string to its decimal equivalent.
The input must be exactly 8 characters long and contain only '0' and '1' characters.
"""

import argparse
import logging
from bin2dec.validator import validate_binary_input
from bin2dec.converter import convert_binary_to_decimal

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Convert 8-digit binary string to decimal number",
        prog="bin2dec"
    )
    parser.add_argument(
        "binary_string",
        help="8-digit binary string consisting of 0s and 1s"
    )
    
    args = parser.parse_args()
    
    try:
        # Validate input
        if not validate_binary_input(args.binary_string):
            raise ValueError("Input must be an 8-character string of 0s and 1s")
        
        # Convert binary to decimal
        decimal_result = convert_binary_to_decimal(args.binary_string)
        print(decimal_result)
        
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        # Log unexpected errors for debugging
        logger.error(f"Unexpected error occurred: {type(e).__name__}: {e}")
        print(f"Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
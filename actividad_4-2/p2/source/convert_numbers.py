"""
convert_numbers.py

This module reads a file containing numbers and converts them to
binary and hexadecimal bases using basic algorithms (no built-in functions).
It handles invalid data, measures execution time, and outputs results
to the console and a file in CSV format.
"""

import sys
import time
import os


def read_file(file_path):
    """
    Reads a file and returns a list of valid numbers.
    Invalid lines are logged to the console.
    Handles numbers with commas as decimal separators (e.g., '12,5' -> 12.5).
    """
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                try:
                    # Handle special case: replace comma with dot for decimals
                    sanitized_line = stripped_line.replace(',', '.')

                    # Attempt to convert line to float first
                    number = float(sanitized_line)

                    # For conversion, we typically want integers.
                    # We cast to int to ensure clean binary/hex conversion.
                    if number.is_integer():
                        data.append(int(number))
                    else:
                        print(f"Warning: Line {line_num} contains float "
                              f"'{stripped_line}', truncating to int.")
                        data.append(int(number))
                except ValueError:
                    print(f"Error: Line {line_num} contains invalid data: "
                          f"'{stripped_line}'")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except OSError as err:
        print(f"Error reading file: {err}")
        sys.exit(1)

    return data


def to_binary(number):
    """
    Converts a number to binary string using basic algorithms.
    """
    if number == 0:
        return "0"

    is_negative = False
    if number < 0:
        is_negative = True
        number = abs(number)

    binary_digits = []
    while number > 0:
        remainder = number % 2
        binary_digits.append(str(remainder))
        number = number // 2

    # The algorithm gives digits in reverse order
    binary_digits.reverse()
    binary_string = "".join(binary_digits)

    if is_negative:
        return "-" + binary_string
    return binary_string


def to_hexadecimal(number):
    """
    Converts a number to hexadecimal string using basic algorithms.
    """
    if number == 0:
        return "0"

    is_negative = False
    if number < 0:
        is_negative = True
        number = abs(number)

    hex_map = "0123456789ABCDEF"
    hex_digits = []

    while number > 0:
        remainder = number % 16
        hex_digits.append(hex_map[remainder])
        number = number // 16

    hex_digits.reverse()
    hex_string = "".join(hex_digits)

    if is_negative:
        return "-" + hex_string
    return hex_string


def write_results(results, input_file_path):
    """
    Writes the results to a file in the ../tests directory relative
    to the source file.
    """
    input_dir = os.path.dirname(os.path.abspath(input_file_path))
    base_name = os.path.basename(input_file_path)
    file_name_no_ext = os.path.splitext(base_name)[0]
    output_filename = f"ConvertionResults_{file_name_no_ext}.txt"

    if 'source' in input_dir:
        output_dir = input_dir.replace('source', 'tests')
    else:
        output_dir = os.path.join(input_dir, 'tests')

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    try:
        with open(output_path, "w", encoding='utf-8') as out_file:
            for line in results:
                out_file.write(line + "\n")
        print(f"Results written to: {output_path}")
    except OSError as err:
        print(f"Error writing output file: {err}")


def main():
    """
    Main execution function.
    """
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python convert_numbers.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    data = read_file(input_file)

    if not data:
        print("No valid data found in the file.")
        sys.exit(1)

    results = []
    # CSV Header
    results.append("NUMBER, BINARY, HEX")

    for num in data:
        binary_val = to_binary(num)
        hex_val = to_hexadecimal(num)
        # CSV Row
        line_str = f"{num}, {binary_val}, {hex_val}"
        print(line_str)
        results.append(line_str)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Append time execution as a footer row in CSV format
    time_msg = f"Execution Time, {elapsed_time:.6f} seconds,"
    print(time_msg)
    results.append(time_msg)

    write_results(results, input_file)


if __name__ == "__main__":
    main()

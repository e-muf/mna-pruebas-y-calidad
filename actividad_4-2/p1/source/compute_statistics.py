"""
compute_statistics.py

This module reads a file containing numbers, computes descriptive statistics
(count, mean, median, mode, standard deviation, and variance) using basic
algorithms, and outputs the results to the console and a file in CSV format.
It handles inputs with commas as decimal separators.
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
                    sanitized_line = stripped_line.replace(',', '.').replace(';', '.')

                    # Attempt to convert line to float
                    number = float(sanitized_line)
                    data.append(number)
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


def calculate_mean(data):
    """Calculates the arithmetic mean of the data."""
    if not data:
        return 0.0
    return sum(data) / len(data)


def calculate_median(data):
    """
    Calculates the median of the data.
    Requires the data to be sorted first.
    """
    if not data:
        return 0.0

    sorted_data = sorted(data)
    n_items = len(sorted_data)
    mid_index = n_items // 2

    if n_items % 2 != 0:
        return sorted_data[mid_index]

    return (sorted_data[mid_index - 1] + sorted_data[mid_index]) / 2.0


def calculate_mode(data):
    """
    Calculates the mode of the data.
    Returns the most frequent number. If multiple exist, returns the first found.
    """
    if not data:
        return 0.0

    frequency = {}
    for item in data:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1

    max_count = 0
    mode_value = data[0]

    for key, count in frequency.items():
        if count > max_count:
            max_count = count
            mode_value = key

    return mode_value


def calculate_variance(data, mean):
    """
    Calculates the sample variance (N-1) using basic arithmetic.
    """
    n_items = len(data)
    if n_items < 2:
        return 0.0

    sum_squared_diff = sum((x - mean) ** 2 for x in data)
    return sum_squared_diff / (n_items - 1)


def calculate_stdev(variance):
    """
    Calculates the standard deviation (sqrt of variance).
    Uses exponentiation (**) instead of math.sqrt.
    """
    return variance ** 0.5


def write_results(results, input_file_path):
    """
    Writes the results to a file in the ../tests directory relative
    to the source file.
    """
    # 1. Get the absolute directory of the input file (e.g., .../p1/source)
    input_dir = os.path.dirname(os.path.abspath(input_file_path))

    # 2. Determine the filename (e.g., TC1.txt -> TC1)
    base_name = os.path.basename(input_file_path)
    file_name_no_ext = os.path.splitext(base_name)[0]
    output_filename = f"StatisticsResults_{file_name_no_ext}.txt"

    # 3. Construct the output directory path
    # Replace 'source' with 'tests' in the path
    if 'source' in input_dir:
        output_dir = input_dir.replace('source', 'tests')
    else:
        # Fallback: Create a 'tests' folder in the current directory
        output_dir = os.path.join(input_dir, 'tests')

    # 4. Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # 5. Full output path
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
        print("Usage: python compute_statistics.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    data = read_file(input_file)

    if not data:
        print("No valid data found in the file.")
        sys.exit(1)

    # Compute Statistics
    count_val = len(data)
    mean_val = calculate_mean(data)
    median_val = calculate_median(data)
    mode_val = calculate_mode(data)
    variance_val = calculate_variance(data, mean_val)
    stdev_val = calculate_stdev(variance_val)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Format Results (CSV Style)
    results = []
    # Header Row
    results.append("Count,Mean,Median,Mode,Standard Deviation,Variance,Time")
    # Data Row
    results.append(f"{count_val},{mean_val},{median_val},{mode_val},"
                   f"{stdev_val},{variance_val},{elapsed_time:.6f}")

    # Print to Screen
    for line in results:
        print(line)

    # Write to File using dynamic path logic
    write_results(results, input_file)


if __name__ == "__main__":
    main()

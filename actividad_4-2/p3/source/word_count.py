"""
word_count.py

This module reads a file containing words, identifies distinct words,
computes their frequency using basic algorithms, and outputs the
results to the console and a file in CSV format.
Results are ordered by frequency (descending).
"""

import sys
import time
import os


def read_file(file_path):
    """
    Reads a file and returns a list of words.
    Invalid lines are logged to the console, but execution continues.
    """
    words = []
    try:
        # Open with utf-8 and 'replace' to handle invalid characters gracefully
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            for line_num, line in enumerate(file, 1):
                stripped_line = line.strip()
                if not stripped_line:
                    continue

                # Split line by whitespace to get words
                line_words = stripped_line.split()

                if not line_words:
                    print(f"Warning: Line {line_num} contains no valid words.")
                    continue

                words.extend(line_words)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except OSError as err:
        print(f"Error reading file: {err}")
        sys.exit(1)

    return words


def count_words(word_list):
    """
    Counts the frequency of each distinct word in the list.
    Returns a dictionary with word as key and frequency as value.
    """
    if not word_list:
        return {}

    frequency = {}
    for word in word_list:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


def write_results(results, input_file_path):
    """
    Writes the results to a file in the ../tests directory relative
    to the source file.
    """
    input_dir = os.path.dirname(os.path.abspath(input_file_path))
    base_name = os.path.basename(input_file_path)
    file_name_no_ext = os.path.splitext(base_name)[0]
    output_filename = f"WordCountResults_{file_name_no_ext}.txt"

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
        print("Usage: python word_count.py fileWithData.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    word_list = read_file(input_file)

    if not word_list:
        print("No valid data found in the file.")
        sys.exit(1)

    # Calculate frequencies
    word_counts = count_words(word_list)

    # Sort items by count (descending)
    sorted_items = sorted(word_counts.items(), key=lambda item: item[1],
                          reverse=True)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Format Results (CSV Style)
    results = []
    results.append("WORD, COUNT")

    grand_total = 0

    for word, count in sorted_items:
        line = f"{word}, {count}"
        print(line)
        results.append(line)
        grand_total += count

    # Footer Row: Grand Total
    total_line = f"GRAND TOTAL, {grand_total}"
    print(total_line)
    results.append(total_line)

    # Footer Row: Execution Time
    time_msg = f"Execution Time, {elapsed_time:.6f} seconds"
    print(time_msg)
    results.append(time_msg)

    write_results(results, input_file)


if __name__ == "__main__":
    main()

"""
This module computes the total sales from a JSON file using a price catalogue.
It handles file paths dynamically to save results in a sibling 'tests' folder.
"""

import sys
import json
import time
import os


def load_json_file(filename):
    """
    Loads and parses a JSON file.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        list/dict: The parsed JSON data, or None if an error occurs.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' contains invalid JSON.")
        return None


def create_price_lookup(catalogue):
    """
    Creates a dictionary for O(1) price lookups from the product catalogue.

    Args:
        catalogue (list): List of product dictionaries.

    Returns:
        dict: A dictionary mapping product titles to their prices.
    """
    price_map = {}
    for item in catalogue:
        title = item.get("title")
        price = item.get("price")
        if title and isinstance(price, (int, float)):
            price_map[title] = price
    return price_map


def compute_total_cost(price_map, sales_record):
    """
    Calculates the total cost of sales based on the price map.

    Args:
        price_map (dict): Dictionary of product prices.
        sales_record (list): List of sales transactions.

    Returns:
        float: The total calculated cost.
    """
    total_cost = 0.0

    for sale in sales_record:
        product = sale.get("Product")
        quantity = sale.get("Quantity")

        if product not in price_map:
            print(f"Error: Product '{product}' not found in catalogue.")
            continue

        if not isinstance(quantity, (int, float)):
            print(f"Error: Invalid quantity for '{product}'.")
            continue

        sale_value = price_map[product] * quantity
        total_cost += sale_value

    return total_cost


def get_output_path(sales_file_path):
    """
    Constructs the output file path based on the sales filename
    and directory structure.
    Target: ../tests/SalesResults_Suffix.txt

    Args:
        sales_file_path (str): The path provided in command line.

    Returns:
        str: The full path where the result file should be saved.
    """
    # 1. Extract filename (e.g., "TC1.Sales.json")
    filename = os.path.basename(sales_file_path)

    # 2. Extract ID (e.g., "TC1") assuming format "ID.Something.json"
    file_id = filename.split('.')[0]

    # 3. Determine directory structure
    # If path is 'actividad_5-2/source/file.json', base is parent dir
    base_dir = os.path.dirname(sales_file_path)

    # If base_dir is empty (file in current dir), use current working dir
    if not base_dir:
        base_dir = os.getcwd()

    # Go up one level to find the parent folder (e.g., 'actividad_5-2')
    parent_dir = os.path.dirname(base_dir)

    # Define 'tests' directory path
    tests_dir = os.path.join(parent_dir, "tests")

    # Create 'tests' directory if it doesn't exist
    if not os.path.exists(tests_dir):
        try:
            os.makedirs(tests_dir)
        except OSError as error:
            print(f"Warning: Could not create tests dir ({error}). "
                  f"Using current.")
            tests_dir = "."

    # 4. Construct final filename
    output_filename = f"SalesResults_{file_id}.txt"
    return os.path.join(tests_dir, output_filename)


def main():
    """
    Main function to execute the sales computation.
    """
    start_time = time.time()

    if len(sys.argv) != 3:
        print("Usage: python compute_sales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    catalogue = load_json_file(price_file)
    sales_record = load_json_file(sales_file)

    if catalogue is None or sales_record is None:
        sys.exit(1)

    price_map = create_price_lookup(catalogue)
    total_cost = compute_total_cost(price_map, sales_record)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Formatting results
    results = (
        f"TOTAL SALES COST\n"
        f"{'-' * 30}\n"
        f"Total Cost:   ${total_cost:,.2f}\n"
        f"Execution Time: {elapsed_time:.4f} seconds\n"
    )

    # Print to screen
    print(results)

    # Write to file in tests folder
    output_path = get_output_path(sales_file)
    try:
        with open(output_path, "w", encoding='utf-8') as result_file:
            result_file.write(results)
        print(f"Results saved to: {output_path}")
    except IOError as error:
        print(f"Error writing to results file: {error}")


if __name__ == "__main__":
    main()

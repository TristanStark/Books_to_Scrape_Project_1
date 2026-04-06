import csv
import os


def write_to_csv(data: list, filename: str) -> None:
    """Write the data to a CSV file."""
    if not data:
        return

    file_exists = os.path.exists(filename)
    file_is_empty = (not file_exists) or os.path.getsize(filename) == 0

    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if file_is_empty:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

import csv 


def write_to_csv(data: list, filename: str) -> None:
    """Write the data to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
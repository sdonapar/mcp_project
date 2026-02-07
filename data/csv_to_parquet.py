import pandas as pd

def csv_to_parquet(csv_file_path: str, parquet_file_path: str) -> None:
    """
    Convert a CSV file to Parquet format.

    Parameters:
    csv_file_path (str): The file path of the input CSV file.
    parquet_file_path (str): The file path where the output Parquet file will be saved.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    for column_name in df.columns:
        print(f"Column: {column_name}, Type: {df[column_name].dtype}")
    # Write the DataFrame to a Parquet file
    df.to_parquet(parquet_file_path, index=False)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert CSV to Parquet format.")
    parser.add_argument("csv_file_path", type=str, help="Path to the input CSV file.")
    parser.add_argument("parquet_file_path", type=str, help="Path to save the output Parquet file.")

    args = parser.parse_args()
    csv_to_parquet(args.csv_file_path, args.parquet_file_path)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def process_data(filename):
  """
  This function reads a CSV file, performs basic data processing, and saves the results.
    Args:
      filename: The CSV file.

  Returns:
      None
  """

  # Reads the CSV file into pandas DataFrame
  df = pd.read_csv(filename)

  # Prints basic information about the data
  print(f"Dataframe shape: {df.shape}")
  print(f"Dataframe columns: {df.columns.tolist()}")
  print(f"Data types:\n{df.dtypes}")

  # Calculates summary statistics for numerical columns
  numeric_cols = df.select_dtypes(include=[np.number])
  print("\nSummary statistics:")
  print(numeric_cols.describe())

  # Filters data based on a specific criteria (e.g country)
  filtered_df = df[df['Country'] == "South Africa"]
  print("\nFiltered data (South African customers):")
  print(filtered_df.head())

  # Generates a histogram for a specific column (e.g subscription date year)
  df["Subscription Year"] = pd.to_datetime(df["Subscription Date"]).dt.year
  plt.hist(df["Subscription Year"])
  plt.xlabel("Subscription Year")
  plt.ylabel("Number of Customers")
  plt.title("Distribution of Subscription Year")
  plt.show()

process_data("customers-1000.csv")
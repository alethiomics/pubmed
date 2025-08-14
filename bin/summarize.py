#!/usr/bin/env python3

"""
This script processes two CSV files provided as command-line arguments. It reads the first CSV file into a DataFrame called `combined` and the second CSV file into a DataFrame called `genes_hash_table`. It then creates a mapping between gene identifiers from `genes_hash_table` and uses this mapping to rename the indices of the `combined` DataFrame. The updated DataFrame is sorted by index and saved to a file named `summary.csv`.

Usage:
    ./summarize.py <combined_csv> <genes_hash_table_csv>

Arguments:
    combined_csv: Path to the CSV file containing the combined data.
    genes_hash_table_csv: Path to the CSV file containing the gene hash table.

Outputs:
    summary.csv: A CSV file containing the processed and sorted data without headers.
"""

import sys
import pandas as pd

combined = pd.read_csv(sys.argv[1], index_col=0, header=None)
genes_hash_table = pd.read_csv(sys.argv[2])

gene_map = dict(zip(genes_hash_table['GeneID'].tolist(), genes_hash_table['Symbol'].tolist()))

combined.rename(index=gene_map,inplace=True)
combined = combined.sort_index()

combined.to_csv('summary.csv', header=False)

#!/usr/bin/env python3

"""
This script processes Homo sapiens gene information by performing the following steps:
1. Reads the gene information from 'Homo_sapiens.gene_info' with tab-separated values.
2. Filters the data to include only protein-coding genes.
3. Removes duplicate gene symbols to retain unique 'GeneID' and 'Symbol' pairs.
4. Saves the unique GeneID and Symbol pairs to 'genes_hash_table.csv'.
5. Extracts and saves the list of unique GeneIDs to 'genes.csv'.
"""

from pandas import read_csv

d = read_csv('Homo_sapiens.gene_info', sep = '\t')
d = d[d['type_of_gene'] == 'protein-coding'][['GeneID', 'Symbol']]
d = d[~d['Symbol'].duplicated()].drop_duplicates().reset_index(drop = True)
d.to_csv('genes_hash_table.csv', index=False)
d['GeneID'].to_csv('genes.csv', index=False, header=False)

#!/usr/bin/env python3

"""
This script retrieves the number of PubMed articles associated with a given gene PubMed ID (gene_pmid).
It accesses the PubMed database via a constructed URL, parses the HTML content to find the total number
of related articles, and writes the result to a CSV file named '<gene_pmid>_results.csv'.

Usage:
    python analyze.py <gene_pmid>

Arguments:
    gene_pmid (str): The PubMed ID of the gene to analyze.

Outputs:
    - A CSV file '<gene_pmid>_results.csv' containing the gene_pmid and the number of articles.
    - An error log '<gene_pmid>_errors.txt' if any exceptions occur during execution.
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

gene_pmid = sys.argv[1]

url = "https://pubmed.ncbi.nlm.nih.gov/?filter=dates.1900-2030&filter=hum_ani.humans&linkname=gene_pubmed&from_uid=" + gene_pmid

# create an empty file to store errors
open(gene_pmid + '_errors.txt', 'a').close()

results = None
single = False

try:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all("div", {"class": "results-amount"})
    # if there is only one result, it is in a different tag
    if not results:
        results = soup.find_all("span", {"class": "single-result-redirect-message"})
        single = True
except Exception as e:
    # record all errors in a file
    with open(gene_pmid + '_errors.txt', 'a') as the_file:
        the_file.write(str(e) + '\n')

if single:
    with open(f"{gene_pmid}.csv", "w") as f:
        f.write(f"{gene_pmid},1\n")
else:
    if results[0].find('span') != None:
        with open(f"{gene_pmid}.csv", "w") as f:
            f.write(f"{gene_pmid},{int(results[0].find('span').text.replace(',', ''))}\n")
    else:
        with open(f"{gene_pmid}.csv", "w") as f:
            f.write(f"{gene_pmid},0\n")

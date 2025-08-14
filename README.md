# Nextflow template pipeline for webscraping by genes

This repo can be used as a template Nextflow pipeline that parallelise processes by gene IDs.

At the same time this repo contains a pipeline to webscrape a number of gene specific publications from Pubmed.

In the `prepare` step genes are downloaded from `Ensembl biomart`.

## Pipeline

The template pipeline consists of three steps:

![](pubmed.png)

where `analyze` step is parallalised by gene names/ids.

### maxForks in `analyze` process

The allowed request rate to the NCBI Entrez programming utilities (E-utilities), which PubMed uses, is 3 requests per second without an API key. With an API key, the default rate is 10 requests per second, and higher rates are available by request according to the National Institutes of Health (NIH).

To avoid hitting the rate limit, the `analyze` process in this pipeline is configured with a reduced `maxForks` value of 5. This means that at most 5 requests will be made concurrently, which should help to stay within the allowed request rate.
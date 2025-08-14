nextflow.enable.dsl=2

process prepare {
  label 'process_single'

  publishDir params.outdir + '/' + '/prepare', mode: 'copy'

  output:
    path 'genes.csv', emit: genes
    path 'genes_hash_table.csv', emit: genes_hash_table
  
  script:
  """
  curl --output Homo_sapiens.gene_info.gz "https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz"
  gunzip Homo_sapiens.gene_info.gz
  prepare.py
  """
}

process analyze {
  tag "${gene}"
  label 'process_single'
  maxForks 5

  // publishDir params.outdir + '/' + '/predict', mode: 'copy'

  input:
    val gene

  output:
    path '*.csv', emit: results, optional: true
    path '*_errors.txt'
  
  script:
  """
  analyze.py "${gene}"
  """
}

process summarize {
  label 'process_low'

  publishDir params.outdir + '/' + '/summarize', mode: 'copy'

  input:
    path results
    path genes_hash_table

  output:
    path 'summary.csv'

  script:
  """
  summarize.py ${results} ${genes_hash_table}
  """
}

workflow {
  
  prepare()

  genes = prepare
    .out
    .genes
    .splitCsv()
    .map { it[0] }

  if (params.env == 'test') genes = genes.take( 20 ) // for testing

  analyze(
    genes
  )

  summarize(
    analyze.out.results.collectFile(name: 'metafile.txt'),
    prepare.out.genes_hash_table
  )
}
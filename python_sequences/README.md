# summarize_fasta.py
Read a fasta file and summarize the header in a .csv file. 

## Usage
Read a fasta file and summarizes the headers in a .csv file.
```
usage: summarize_fasta [-h] [--header [HEADER ...]] [--progress | --no-progress] fasta_fp out_fp

Read a fasta file and summarizes the headers in a .csv file.

positional arguments:
  fasta_fp              fasta file path
  out_fp                csv output file

optional arguments:
  -h, --help            show this help message and exit
  --header [HEADER ...]
                        Column names. If not given, no header is written.
  --progress, --no-progress
                        show progress bar (default: True)
```

## Example 
Assume we have a file `sequences.fasta` : 
```
>gene1|Phlox_pilosaPilosa|Phlox_pilosa_pilosa_1718_20|Allele_2
GGTCATTTTTGCCAAAAAGAATGGGTAATTTACAGTTTATACCCCTGGGAGATGGCAAATGTGCACCGCGTACCCNNNNN
>gene1|Phlox_subulata|Phlox_subulata_OPGC-4030|Allele_1
ATGGGTAATTTACAGTTTATACCCCTGGGAGATGGCAAATGTGCACCGCGTACCCCTGTTGTTTGGAAAACTTAACCGAT
>gene1|Phlox_subulata|Phlox_subulata_OPGC-4030|Allele_2
GCGAGGTCATTTTTGCCAAAAAGAATGGGTAATTTACAGTTTATACCCCTGGGAGATGGCAAATGTGCACCGCGTACCCC
>gene2|Phlox_subulata|Phlox_subulata_OPGC-4061|Allele_1
GCGAGGTCATTTTTGCCAAAAAGAATGGGTAATTTACAGTTTATACCCCTGGGAGATGGCAAATGTGCACCGCGTACCCC
>gene2|Phlox_subulata|Phlox_subulata_OPGC-4061|Allele_2
GCGAGGTCATTTTTGCCAAAAAGAATGGGTAATTTACAGTTTATACCCCTGGGAGATGGCAAATGTGCACCGCGTACCCC
```
Let us run
```sh
python summarize_fasta.py ./sequences.fasta ./summary.csv --header id_seq gene taxa individual allele
```

It generates a file `summary.csv` 

|     | id_seq | gene  | taxa               | individual                  | allele   |
| --- | ------ | ----- | ------------------ | --------------------------- | -------- |
| 0   | 0      | gene1 | Phlox_pilosaPilosa | Phlox_pilosa_pilosa_1718_20 | Allele_2 |
| 1   | 1      | gene1 | Phlox_subulata     | Phlox_subulata_OPGC-4030    | Allele_1 |
| 2   | 2      | gene1 | Phlox_subulata     | Phlox_subulata_OPGC-4030    | Allele_2 |
| 3   | 3      | gene2 | Phlox_subulata     | Phlox_subulata_OPGC-4061    | Allele_1 |
| 4   | 4      | gene2 | Phlox_subulata     | Phlox_subulata_OPGC-4061    | Allele_2 |


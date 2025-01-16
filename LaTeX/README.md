# clean_biblio
Clean and check a bibtex file for a `LaTeX` document. 

## Features:
* removes unused fields (`files`,`groups`,`abstract`, `comment`, `hal_id`,`hal_version`)
* for articles: keep only some fields (author, date, journal, title, doi, number, volume, pages) and check for missing fields
* check for journal ambiguous names (from the journal list `journalList.txt`) or missing journal names. 
* remove the months from the dates (generates a biblatex warning)
* sort by alphabetical order of the keyword 
* (optional) abbreviate the journal names.

## Syntax 
```bash
python ./cleanBiblio.py --input biblio.bib OPTIONS
```
### Arguments:
* `--input`, `-i` (req.) input file (a `.bib.` file)
* `--output`, `-o` (opt., default to `cleanbib.bib`) output file (a `.bib.` file)
### Options
* `--abbreviate`, `-a` abbreviate the journal names (for instance "Journal of Evolutionary Biology" becomes "J. Evolution. Biol.")
* `--dotless` if the journal names are abbreviated, remove the dots (for instance "J Evolution Biol").


## Examples:
`biblio.bib` is:
```
@Book{Giraud2020,
  author    = {Tatiana Giraud and Olivier Tenaillon},
  date      = {2020},
  title     = {Biodiversité et Écologie},
  location  = {Palaiseau, France},
  publisher = {École polytechnique, département de biologie},
  file      = {:Giraud2020.pdf:PDF},
  groups    = {Ecology},
}

@InBook{Lessios1998,
  author     = {Harilaos Lessios},
  booktitle  = {Endless Forms: Species and Speciation},
  date       = {1998},
  title      = {The first stage of speciation as seen in organisms separated by the Isthmus of Panama},
  bookauthor = {Daniel J. Howard and Stewart H. Berlocher},
  pages      = {186--201},
  publisher  = {Oxford University Press Oxford},
  file       = {:Lessios1998.pdf:PDF},
  groups     = {Speciation},
}

@Article{Wu2004,
  author       = {Chung-I Wu and Chau-Ti Ting},
  date         = {2004},
  journaltitle = {Nature Reviews Genetics},
  title        = {Genes and speciation},
  doi          = {10.1038/nrg1269},
  number       = {2},
  pages        = {114--122},
  volume       = {5},
  abstract     = {It is only in the past five years that studies of speciation have truly entered the molecular era. },
  file         = {:Wu2004.pdf:PDF},
  groups       = {Genetics / pop gen / mutations, Speciation},
  publisher    = {Springer Science and Business Media {LLC}},
}
```
Now running
```bash
python ./cleanBiblio.py --input biblio.bib --output cleanbib.bib --abbreviate --dotless
```
prints 
```
Bibliography cleaned and stored to cleanbib.bib

3 entries analyzed including:
     1 for the type book
     1 for the type inbook
     1 for the type article

8 removed fields (for non-article entries)

For 1 article(s):
     0 missing field(s)
     0 unreferenced journal name(s)
     100.0 % journal coverage
     0.0 % ambiguous journal names
     0 months removed from dates
```
and creates a file `cleanbib.bib`
```
@Book{Giraud2020,
  author          = {Tatiana Giraud and Olivier Tenaillon},
  date            = {2020},
  title           = {Biodiversité et Écologie},
  location        = {Palaiseau, France},
  publisher       = {École polytechnique, département de biologie},
}

@InBook{Lessios1998,
  author          = {Harilaos Lessios},
  booktitle       = {Endless Forms: Species and Speciation},
  date            = {1998},
  title           = {The first stage of speciation as seen in organisms separated by the Isthmus of Panama},
  bookauthor      = {Daniel J. Howard and Stewart H. Berlocher},
  pages           = {186--201},
  publisher       = {Oxford University Press Oxford},
}

@Article{Wu2004,
  author          = {Chung-I Wu and Chau-Ti Ting},
  date            = {2004},
  journaltitle    = {Nat Rev Genet},
  title           = {Genes and speciation},
  doi             = {10.1038/nrg1269},
  number          = {2},
  volume          = {5},
  pages           = {114--122},
}
```
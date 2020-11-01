# CV

Arjun Savel's CV, [linked with Overleaf](https://www.overleaf.com/). See the compiled version on the [corresponding website](https://arjunsavel.github.io/).

The formatting of this CV is based on @davidwhogg's, and the implementation of continuous integration was inspired by that of @dfm.

## Process
Every 12 hours, the `add_review_nums` workflow is run. This scrapes JOSS for the number of reviews I've conducted, writes this number to the main tex file, and commits the changes. 

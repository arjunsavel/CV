# CV
[![Update publications](https://github.com/arjunsavel/CV/actions/workflows/update_pubs.yml/badge.svg)](https://github.com/arjunsavel/CV/actions/workflows/update_pubs.yml) [![Add JOSS Reviews](https://github.com/arjunsavel/CV/actions/workflows/add_review_nums.yml/badge.svg)](https://github.com/arjunsavel/CV/actions/workflows/add_review_nums.yml)   [![Build CV](https://github.com/arjunsavel/CV/actions/workflows/cv_add.yml/badge.svg)](https://github.com/arjunsavel/CV/actions/workflows/cv_add.yml) [![Tests](https://github.com/arjunsavel/CV/actions/workflows/run_tests.yml/badge.svg)](https://github.com/arjunsavel/CV/actions/workflows/run_tests.yml) [![codecov](https://codecov.io/gh/arjunsavel/CV/branch/main/graph/badge.svg?token=NNNDPIX60U)](https://codecov.io/gh/arjunsavel/CV) [![docstr_coverage](data/docstring_badge.svg)](https://github.com/HunterMcGushion/docstr_coverage) ![CV Actions](https://api.meercode.io/badge/arjunsavel/CV?type=ci-score&lastDay=14) [![Maintainability](https://api.codeclimate.com/v1/badges/aa2a03c7484e824c75ff/maintainability)](https://codeclimate.com/github/arjunsavel/CV/maintainability) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


My CV, [linked with Overleaf](https://www.overleaf.com/). See the compiled version on [my website](https://arjunsavel.github.io/).

The formatting of my CV is based on @davidwhogg's, and the implementation of continuous integration was inspired by @dfm's. Other design components adapted from Sourabh Bajaj and Amlaan Bhoi.

## Process
Every 24 hours (midnight UTC), the `add_review_nums` workflow is run. This scrapes JOSS for the number of reviews I've conducted, writes this number to the main tex file, and commits the changes.

Additionally, `scrape_ads` is run, which pulls my publications & their citations from [NASA ADS](https://ui.adsabs.harvard.edu/). These are aggregated, formatted, and written to a tex file.

Finally, a new tag is created for this repository.


Also...adds CV metadata for SEO snippet purposes.

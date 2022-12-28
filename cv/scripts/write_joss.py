"""
Module to write the JOSS numbers.

author: @arjunsavel
"""
import inspect
import os

import numpy as np

import cv

cv_root = inspect.getfile(cv).split("cv")[0]
data_path = os.path.join(cv_root, "data")


def main():
    # read in lines from tex file
    f = open(os.path.join(cv_root, "main.tex"), "r")
    f1 = f.readlines()
    f.close()

    # assume scrape_joss.py has already been run
    num_reviewed = int(np.loadtxt(os.path.join(data_path, "num_joss_reviews.txt")))

    if num_reviewed == 1:
        project_word = "project"
    else:
        project_word = "projects"

    # reviewed_line = f'\\item Reviewer, Journal of Open Source Software ({num_reviewed} {project_word} reviewed) (2020)\n'

    reviewed_line = (
        "\\resumeItem{}{Reviewer, Journal of Open Source Software "
        + f"({num_reviewed} {project_word} reviewed) "
        + "(2020--present)}\n"
    )

    for i, line in enumerate(f1):
        if "Reviewer, Journal of Open Source Software" in line:
            f1[i] = reviewed_line
            break

    # write back to file
    f = open(os.path.join(cv_root, "main.tex"), "w")
    f.writelines(f1)
    f.close()


if __name__ == "__main__":
    main()

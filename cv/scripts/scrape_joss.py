"""
Module to scrape the public JOSS reviewers sheet.

author: @arjunsavel
"""
import inspect
import os
import sys

import numpy as np
import pandas as pd
from gsheets import Sheets

import cv

cv_root = inspect.getfile(cv).split("cv")[0]
data_path = os.path.join(cv_root, "data")


def get_joss_table(data):
    """
    Gets a JOSS table, using the necessary secret.

    Inputs
    ------
        :data: (str) a secret for gsheets.

    Outputs
    -------
        :joss_table: (pd.DataFrame) the JOSS table containing all the JOSS reviewers.
    """

    sheets = Sheets.from_developer_key(data)

    joss_reviews_id = "1PAPRJ63yq9aPC1COLjaQp8mHmEq3rZUzwUYxTulyu78"

    s = sheets[joss_reviews_id]

    s.sheets[0].to_csv("test.csv")

    joss_table = pd.read_csv("test.csv")

    return joss_table


def count_num_reviews(joss_table):
    """
    Counts the number of reviews I've completed.
    todo: make username an arg.

    Inputs
    ------
        :joss_table: (pd.DataFrame) the JOSS table containing all the JOSS reviewers.

    Outputs
    -------
        :num_reviews: (int) number of reviews.
    """
    my_username = "arjunsavel"

    review_col = "Review count(all time)"
    num_reviews = int(
        joss_table[joss_table.username == my_username][review_col].values[0]
    )
    return num_reviews


if __name__ == "__main__":
    data = sys.argv[1]

    joss_table = get_joss_table(data)

    num_reviews = count_num_reviews(joss_table)

    np.savetxt(os.path.join(data_path, "num_joss_reviews.txt"), [num_reviews])

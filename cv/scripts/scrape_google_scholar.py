"""
Module to scrape google scholar information. Inspired by dfm/cv/update-astro-pubs

author: @arjunsavel
"""
import inspect
import json
import os
import time

import numpy as np
import requests
from bs4 import BeautifulSoup

import cv

cv_root = inspect.getfile(cv).split("cv")[0]
data_path = os.path.join(cv_root, "data")


def clean_citation(citation):
    """
    cast the citation to an int.
    """
    if citation != "":
        citation = eval(citation)
    else:
        citation = 0
    return citation


def clean_authors(authors):
    """
    Reorders them like ADS.
    """
    # turn into a list
    authors = authors.split(",")

    # flip them
    for i, author in enumerate(authors):
        # split into initials and last name
        split_author_name = author.split()
        author = split_author_name[-1] + ", " + split_author_name[0]
        authors[i] = author

    return authors


def clean_journal_info(journal_info):
    """
    Separates the string containing journal info into a dictionary containing the parameters as ADS does.

    Inputs
    ------
        :journal_info: (str) information about the journal, e.g. its name and the page

    Outputs
    -------
        :journal_info_split_cleaned:  (list of strs) all the info from the journal but split up.
    """
    journal_info_split_cleaned = {}
    journal_info_split = journal_info.split(", ")
    year = eval(journal_info_split[-1])  # the year is always the last

    journal_info_split_cleaned["page"] = None
    journal_info_split_cleaned["volume"] = None
    journal_info_split_cleaned["journal"] = journal_info_split[0]

    if len(journal_info_split) == 3:  # just journal and year
        journal_info_split_cleaned["page"] = journal_info_split[1]

    # todo: get volume in there

    journal_info_split_cleaned["year"] = year
    return journal_info_split_cleaned


def get_scrape_google_scholar(author):
    """
    Does the main google scholar scraping for all pubs for an author.

    Inputs
    -------
        :author: (str) name of author. lastname, firstname midddlename.

    Outputs
    -------
        :cleaned_articles: list of dict of publications.
    """
    author = reverse_name(author)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    }
    url = f"""https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={author.replace(' ', '+')}&btnG="""
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find_all("table")

    try:
        personal_url = table[0].findAll("a")[0]["href"]
    except IndexError:  # if there are no results!
        return []

    full_url = "https://scholar.google.com/" + personal_url

    response = requests.get(full_url, headers=headers)
    new_soup = BeautifulSoup(response.content, features="html.parser")

    citations = []
    cleaned_articles = []
    for s in new_soup.find_all("tbody"):
        articles = s.findAll("tr", {"class": "gsc_a_tr"})
        for article in articles:
            cleaned_article = {}
            citation = article.findAll("a")[1].text
            citation = clean_citation(citation)

            citations += [citation]
            cleaned_article["citations"] = citation

            cleaned_article["title"] = article.findAll("a")[0].text

            authors = article.findAll("div")[0].text

            authors = clean_authors(authors)

            cleaned_article["authors"] = authors

            journal_info = article.findAll("div")[1].text
            journal_info = clean_journal_info(journal_info)

            cleaned_article["journal"] = journal_info["journal"]
            cleaned_article["page"] = journal_info["page"]
            cleaned_article["volume"] = journal_info["volume"]
            cleaned_article["year"] = journal_info["year"]

            cleaned_article["url"] = None
            cleaned_article["doi"] = None
            cleaned_article["pubdate"] = None
            cleaned_article["arxiv"] = None

            # todo: OSF!
            # todo: get this in the preprint checking func :)
            if cleaned_article["journal"] == "PsyArXiv":
                cleaned_article["doctype"] = "eprint"
            else:
                cleaned_article["doctype"] = "article"

            cleaned_articles += [cleaned_article]

    citations.sort()

    citations = np.array(citations)

    h_index = np.arange(len(citations))[np.arange(len(citations)) > citations[::-1]][0]

    print(h_index)
    return cleaned_articles


def reverse_name(author):
    """
    goes from lastname, firstname middlename to firstname, lastname.
    todo: multiple middle names?
    """

    author_names = author.replace(",", "").split(" ")

    if len(author_names) == 3:
        return " ".join([author_names[1], author_names[2], author_names[0]])
    else:
        return " ".join([author_names[1], author_names[0]])


if __name__ == "__main__":

    name = "McDanal, Riley"

    try:
        paper_dict = get_scrape_google_scholar(name)
    except requests.Timeout as err:
        print("Timeout error")
        print(err)
        time.sleep(60)
        paper_dict = get_scrape_google_scholar(name)

    with open("../data/google_scholar_scrape.json", "w") as f:
        json.dump(paper_dict, f, sort_keys=True, indent=2, separators=(",", ": "))

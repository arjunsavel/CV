"""
Module to scrape google scholar information. Inspired by dfm/cv/update-astro-pubs

author: @arjunsavel
"""
import inspect
import json
import os
import pdb
import time

import numpy as np
import requests
from bs4 import BeautifulSoup

# import cv
#
# cv_root = inspect.getfile(cv).split("cv")[0]
# data_path = os.path.join(cv_root, "data")


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
    authors = authors.split(", ")

    # flip them
    for i, author in enumerate(authors):
        # split into initials and last name
        if author in ["...", " "]:
            break
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
    if "arxiv" in journal_info:
        journal_info_split_cleaned["arxiv"] = journal_info.split(":")[-1]
        journal_info_split_cleaned["journal"] = "arxiv"
        return

    journal_info_split = journal_info.split(", ")
    # pdb.set_trace()
    year = eval(journal_info_split[-1])  # the year is always the last

    journal_info_split_cleaned["page"] = None
    journal_info_split_cleaned["volume"] = None
    journal_info_split_cleaned["arxiv"] = None
    journal_info_split_cleaned["journal"] = journal_info_split[0]

    if len(journal_info_split) == 3:  # just journal and year
        journal_info_split_cleaned["page"] = journal_info_split[1]

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
    # author = reverse_name(author)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    }
    # url = f"""https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={author.replace(' ', '+')}&pagesize=80"""
    url = "https://scholar.google.com/citations?user=e6T8gFsAAAAJ&hl=en&oi=ao&cstart=0&pagesize=80"

    response = requests.post(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find_all("table")

    title_list = table[1].findAll("a", class_="gsc_a_at")
    title_list = [t.text for t in title_list]

    rest_info = table[1].findAll("div", class_="gs_gray")
    rest_info = [r.text for r in rest_info]
    authors_list = rest_info[::2]
    pub_info = rest_info[1::2]

    pub_years = table[1].findAll("span", class_="gs_oph")
    pub_years = [p.text for p in pub_years]

    citations = table[1].findAll("a", class_="gsc_a_ac gs_ibl")
    citations_list = [c.text for c in citations]

    citations = []
    cleaned_articles = []
    for i, title in enumerate(title_list):
        cleaned_article = {}
        citation = citations_list[i]
        citation = clean_citation(citation)

        citations += [citation]
        cleaned_article["citations"] = citation

        cleaned_article["title"] = title

        authors = authors_list[i]
        cleaned_article["authors"] = clean_authors(authors)

        journal_info = pub_info[i]
        journal_info = clean_journal_info(journal_info)

        cleaned_article["journal"] = journal_info["journal"]
        cleaned_article["page"] = journal_info["page"]
        cleaned_article["volume"] = journal_info["volume"]
        cleaned_article["arxiv"] = journal_info["arxiv"]

        cleaned_article["year"] = pub_years[i]

        cleaned_article["url"] = None
        cleaned_article["doi"] = None
        cleaned_article["pubdate"] = None

        # todo: OSF!
        # todo: get this in the preprint checking func :)
        if cleaned_article["journal"] == "PsyArXiv":
            cleaned_article["doctype"] = "eprint"
        else:
            cleaned_article["doctype"] = "article"

        cleaned_articles += [cleaned_article]

    citations.sort()

    citations = np.array(citations)
    # pdb.set_trace()
    # citations[citations==6] = 7
    h_index = calc_h_index(citations)
    # h_index = np.arange(len(citations))[np.arange(len(citations)) > citations[::-1]][0]
    first_author_pubs = [a for a in cleaned_articles if author in a["authors"][0]]
    first_author_citations = np.array([a["citations"] for a in first_author_pubs])
    n_first_author_citations = np.sum(first_author_citations)

    first_author_citations.sort()
    first_author_h_index = np.arange(len(first_author_citations))[np.arange(len(first_author_citations)) > first_author_citations[::-1]][0]
    print(h_index)
    # pdb.set_trace()
    n_citations = np.sum(citations)
    print(n_citations)
    return cleaned_articles, n_citations, h_index, n_first_author_citations, first_author_h_index


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


def calc_h_index(citations):
    """
    Calculates the h-index from a list of citations.

    Inputs
    -------
        :citations: (list of ints) list of citations for each paper.

    Outputs
    -------
        :h_index: (int) h-index.
    """
    citations.sort()
    h_index = 0
    while True:
        H_citations = citations[citations >= h_index]

        # is this valid? For h index of N, I need at least N papers with N citations. H_ciations is the list of papers with them.
        if len(H_citations) >= h_index:
            pass
        else:
            h_index -= 1
            break

        h_index += 1
    return h_index

if __name__ == "__main__":

    name = "McDanal, R"

    try:
        paper_dict,  n_citations, h_index, n_first_author_citations, first_author_h_index = get_scrape_google_scholar(name)
    except requests.Timeout as err:
        print("Timeout error")
        print(err)
        time.sleep(60)
        paper_dict = get_scrape_google_scholar(name)

    with open("data/google_scholar_scrape.json", "w") as f:
        json.dump(paper_dict, f, sort_keys=True, indent=2, separators=(",", ": "))
    np.savetxt("data/n_citations.txt", [n_citations])
    np.savetxt("data/h_index.txt", [h_index])
    np.savetxt("data/n_first_author_citations.txt", [n_first_author_citations])
    np.savetxt("data/first_author_h_index.txt", [first_author_h_index])

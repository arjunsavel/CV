"""
Heavily inspired by dfm/cv/update-astro-pubs
"""

import importlib.util
import inspect
import json
import os
import time
from operator import itemgetter

import ads
import requests

import cv

cv_path = os.path.dirname(inspect.getfile(cv))  # .../src/cv
cv_root = os.path.dirname(cv_path)  # .../src
data_path = os.path.join(cv_root, "data")
here = os.path.join(cv_path, "scripts")
# here = os.path.abspath("")
spec = importlib.util.spec_from_file_location(
    "utf8totex", os.path.join(here, "utf8totex.py")
)
utf8totex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utf8totex)

# need to add ADS token as env variable


def get_papers(author):
    """
    Gets all the papers for a given author from NASA/ADS.

    Inputs
    ------
        :author: (str) name of author. Lastname, firstname middle

    Outputs
    -------
        :dicts: (list of dictionaries) the sorted dictionaries corresponding to the author's publications.
    """
    papers = list(
        ads.SearchQuery(
            author=author,
            fl=[
                "id",
                "title",
                "author",
                "doi",
                "year",
                "pubdate",
                "pub",
                "volume",
                "page",
                "page_range",
                "page_count",
                "identifier",
                "doctype",
                "citation_count",
                "bibcode",
            ],
            max_pages=100,
        )
    )

    dicts = []
    for paper in papers:
        
        # one set of conferences proceedings snuck in!
        if "AASTCS 11" in paper.pub:
            continue
        aid = [
            ":".join(t.split(":")[1:])
            for t in paper.identifier
            if t.startswith("arXiv:")
        ]
        for t in paper.identifier:
            if len(t.split(".")) != 2:
                continue
            try:
                list(map(int, t.split(".")))
            except ValueError:
                pass
            else:
                aid.append(t)
        page = paper.page[0] if paper.page else None
        if page is not None and page.startswith("arXiv:"):
            aid.append(":".join(page.split(":")[1:]))
            page = None
        # check for mentee name, if so, prepend a * before last name
        author_list = list(map(utf8totex.utf8totex, paper.author))
        mentee_map = {'Arnold, Kenneth E.': '*Triantafillides, Anastasia',
                      'Triantafillides, Anastasia': '*Triantafillides, Anastasia'}

        author_list = [mentee_map.get(author, author) for author in author_list]
        dicts.append(
            dict(
                doctype=paper.doctype,
                authors=author_list,
                year=paper.year,
                pubdate=paper.pubdate,
                doi=paper.doi[0] if paper.doi is not None else None,
                title=utf8totex.utf8totex(paper.title[0]),
                pub=paper.pub,
                volume=paper.volume,
                page=page,
                page_range=getattr(paper, "page_range", None),
                page_count=getattr(paper, "page_count", None),
                arxiv=aid[0] if len(aid) else None,
                citations=(
                    paper.citation_count if paper.citation_count is not None else 0
                ),
                url="https://ui.adsabs.harvard.edu/abs/" + paper.bibcode,
            )
        )
    return sorted(dicts, key=itemgetter("pubdate"), reverse=True)


if __name__ == "__main__":
    # tries once more if there's a timeout error
    try:
        paper_dict = get_papers("Savel, Arjun Baliga")
        paper_dict += get_papers("Baliga Savel, Arjun")
    except requests.Timeout as err:
        print("Timeout error")
        print(err)
        time.sleep(60)
        paper_dict = get_papers("Savel, Arjun Baliga")
        paper_dict += get_papers("Baliga Savel, Arjun")
    # the two name queries overlap; keep one record per bibcode
    paper_dict = list({p["url"]: p for p in paper_dict}.values())
    paper_dict = sorted(paper_dict, key=itemgetter("pubdate"), reverse=True)
    with open(os.path.join(data_path, "ads_scrape.json"), "w") as f:
        json.dump(paper_dict, f, sort_keys=True, indent=2, separators=(",", ": "))

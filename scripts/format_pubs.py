"""
Heavily inspired by dfm/cv/scripts/render.py
"""

import ads
from datetime import date
from operator import itemgetter
import json
import importlib.util
import os

here = os.path.abspath('')
spec = importlib.util.spec_from_file_location(
    "utf8totex", os.path.join(here, "utf8totex.py")
)
utf8totex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utf8totex)


JOURNAL_MAP = {
    "ArXiv e-prints": "ArXiv",
    "arXiv e-prints": "ArXiv",
    "Monthly Notices of the Royal Astronomical Society": "\\mnras",
    "The Astrophysical Journal": "\\apj",
    "The Astronomical Journal": "\\aj",
    "Publications of the Astronomical Society of the Pacific": "\\pasp",
    "IAU General Assembly": "IAU",
    "Astronomy and Astrophysics": "\\aanda",
    "American Astronomical Society Meeting Abstracts": "AAS",
}


def format_pub(args):
    ind, pub = args
    fmt = "\\item[{{\\color{{numcolor}}\\scriptsize{0}}}] ".format(ind)
    n = [
        i
        for i in range(len(pub["authors"]))
        if "Savel" in pub["authors"][i]
    ][0]
    pub["authors"][n] = "\\textbf{Savel, Arjun}"
    
    pub_title = pub["title"].replace('{\\&}amp;', '\&') # for latex literal interp.
    
    if len(pub["authors"]) > 5:
        fmt += "; ".join(pub["authors"][:4])
        fmt += "; \\etal"
        if n >= 4:
            others = len(pub['authors']) - 4
            fmt += "\\ ({{{0}}} other co-authors, ".format(others)
            fmt += "incl.\\ \\textbf{Savel, Arjun})"
    elif len(pub["authors"]) > 1:
        fmt += "; ".join(pub["authors"][:-1])
        fmt += "; \\& " + pub["authors"][-1]
    else:
        fmt += pub["authors"][0]

    fmt += ", {0}".format(pub["year"])

    if pub["doi"] is not None:
        fmt += ", \\doi{{{0}}}{{{1}}}".format(pub["doi"], pub_title)
    else:
        fmt += ", \\emph{{{0}}}".format(pub_title)

    if not pub["pub"] in [None, "ArXiv e-prints"]:
        fmt += ", " + JOURNAL_MAP.get(
            pub["pub"].strip("0123456789# "), pub["pub"]
        )

    if pub["volume"] is not None:
        fmt += ", \\textbf{{{0}}}".format(pub["volume"])

    if pub["page"] is not None:
        fmt += ", {0}".format(pub["page"])

    if pub["arxiv"] is not None:
        fmt += " (\\arxiv{{{0}}})".format(pub["arxiv"])
        
    if pub["url"] is not None and pub["citations"] == 1:
        fmt += " [\\href{{{0}}}{{{1} citation}}]".format(
            pub["url"], pub["citations"]
        )
        
    elif pub["url"] is not None and pub["citations"] > 1:
        fmt += " [\\href{{{0}}}{{{1} citations}}]".format(
            pub["url"], pub["citations"]
        )
        
    elif pub["url"] is not None and pub["citations"] == 0: 
        fmt += " [\\href{{{0}}}]".format(
                pub["url"]
        )

    return fmt


if __name__ == "__main__":
    with open("../data/ads_scrape.json", "r") as f:
        pubs = json.load(f)
    

    pubs = sorted(pubs, key=itemgetter("pubdate"), reverse=True)
    
    pubs = [
        p
        for p in pubs
        if (
            p["doctype"] in ["article", "eprint"]
            and p["pub"] != "Zenodo Software Release"
        )
    ]
    
    ref = [p for p in pubs if p["doctype"] == "article"]
    unref = [p for p in pubs if p["doctype"] == "eprint"]

    # Compute citation stats
    npapers = len(ref)
    nfirst = sum(1 for p in pubs if "Savel" in p["authors"][0])
    cites = sorted((p["citations"] for p in pubs), reverse=True)
    ncitations = sum(cites)
    hindex = sum(c > i for i, c in enumerate(cites))

#     summary = (
#         "refereed: {1} / first author: {2} / citations: {3} / "
#         "h-index: {4} ({0})"
#     ).format(date.today(), npapers, nfirst, ncitations, hindex)
    summary = (
        "citations: {1} / "
        "h-index: {2} ({0})"
    ).format(date.today(), ncitations, hindex)
    with open("../supp_tex/pubs_summary.tex", "w") as f:
        f.write(summary)

    ref = list(map(format_pub, zip(range(len(ref), 0, -1), ref)))
    unref = list(map(format_pub, zip(range(len(unref), 0, -1), unref)))

    with open("../supp_tex/pubs_ref.tex", "w") as f:
        f.write("\n\n".join(ref))
    with open("../supp_tex/pubs_unref.tex", "w") as f:
        f.write("\n\n".join(unref))
        

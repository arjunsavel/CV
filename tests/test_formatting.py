import unittest

from cv.scripts.format_pubs import *


class TestFormatStudent(unittest.TestCase):
    def test_format_student_not_in_pub(self):
        pub = {
            "arxiv": None,
            "authors": ["Savel, Arjun B."],
            "citations": 0,
            "doctype": None,
            "doi": None,
            "page": None,
            "pub": None,
            "pubdate": "2022-12-00",
            "title": None,
            "url": None,
            "volume": None,
            "year": "2022",
        }
        pub_copy = pub.copy()
        pub_copy = format_for_students(pub_copy)
        self.assertTrue(pub == pub_copy)

    def test_format_student_in_pub(self):
        pub = {
            "arxiv": None,
            "authors": ["Savel, Arjun B.", "Arnold, Kenneth"],
            "citations": 0,
            "doctype": None,
            "doi": None,
            "page": None,
            "pub": None,
            "pubdate": "2022-12-00",
            "title": None,
            "url": None,
            "volume": None,
            "year": "2022",
        }
        pub_copy = pub.copy()
        pub_copy = format_for_students(pub_copy)
        self.assertTrue("*" == pub_copy["authors"][1][0])


class TestFormatInpress(unittest.TestCase):
    def test_format_inpress_known(self):
        pub = {"title": "SImMER: A Pipeline for Reducing and Analyzing Images of Stars", "doctype": "eprint", "arxiv": None, "volume": None}

        res = check_inpress(pub)

        self.assertTrue(res)

    def test_format_inpress_unknown(self):
        pub = {"arxiv": "2209.11506", "title": "notinpress!", "doctype": "eprint", "volume": None}

        res = check_inpress(pub)

        self.assertTrue(res)


class TestFormatTitle(unittest.TestCase):
    def test_title_no_change(self):
        title = "eee"
        formatted = format_title(title)
        self.assertTrue(title == formatted)

    def test_title_latex_ampersand(self):
        FORMAT_STYLE = "latex"
        title = "something {\\&}amp; else"
        shouldbe = "something \& else"

        self.assertTrue(format_title(title) == shouldbe)

    # def test_title_ampersand(self):
    #     FORMAT_STYLE = "ee"
    #     title = "something {\\&}amp; else"
    #     shouldbe = "something & else"
    #
    #     self.assertTrue(format_title(title) == shouldbe)


class TestFormatAuthors(unittest.TestCase):
    def test_short_authors_single_author(self):
        fmt = ""
        authors = ["Savel, Arjun"]
        short = True
        n = 0
        res = format_authors(fmt, authors, short, n)

        self.assertTrue(res == "Savel, Arjun")

    def test_short_authors_four_authors(self):
        fmt = ""
        authors = [
            "Savel, Arjun",
            "othername, otherfirst",
            "yetanother, name",
            "onemore, name",
        ]
        short = True
        n = 0
        res = format_authors(fmt, authors, short, n)
        self.assertTrue(res == "Savel, Arjun \\etal{}")

    def test_short_authors_four_authors_user_after(self):
        fmt = ""
        authors = [
            "othername, otherfirst",
            "Savel, Arjun",
            "yetanother, name",
            "onemore, name",
        ]
        short = True
        n = 1
        res = format_authors(fmt, authors, short, n)

        fmt = (
            "othername, otherfirst \\etal{}"  # + "\\ ({{{0}}} other co-authors, ".format(3)
        )
        # fmt += 'f"incl. Savel, Arjun)"'
        self.assertTrue(res == fmt)


class TestFormatPub(unittest.TestCase):
    def test_simple_pub(self):
        pub = {
            "arxiv": None,
            "authors": ["Savel, Arjun B."],
            "citations": 0,
            "doctype": None,
            "doi": None,
            "page": None,
            "pub": "Big Journal",
            "pubdate": "2022-12-00",
            "title": "Arjun has a paper",
            "url": None,
            "volume": None,
            "year": "2022",
        }
        short = True
        ind = 0
        args = (ind, pub, short)

        res = format_pub(args)
        expected = r"\item[{\color{numcolor}\scriptsize0}] \textbf{Savel}, \textbf{Arjun} 2022, \emph{Arjun has a paper}, Big Journal"
        self.assertTrue(res == expected)


def _pub(title, pub, first="Savel, Arjun", citations=0, arxiv=None, volume=None):
    return {
        "title": title, "pub": pub, "authors": [first, "Other, Person"],
        "citations": citations, "arxiv": arxiv, "volume": volume, "page": None,
        "doi": None, "pubdate": "2026-01-00", "doctype": "article",
    }


class TestMergeDuplicates(unittest.TestCase):
    def test_latex_math_in_preprint_title(self):
        journal = _pub("Detection of CO<SUB>2</SUB> in WASP-52b", "AJ", volume=172)
        preprint = _pub("Detection of $\\rm CO_2$ in WASP-52b", "arXiv e-prints", arxiv="2609.21810")
        merged = merge_duplicates([journal, preprint])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["pub"], "AJ")
        self.assertEqual(merged[0]["arxiv"], "2609.21810")

    def test_copyedited_title(self):
        journal = _pub("Limb Asymmetries on WASP-39b: A Multi-GCM Comparison of Chemistry, Clouds, and Hazes", "ApJ")
        preprint = _pub("Limb asymmetries on WASP-39b: a multi-GCM comparison of chemistry, clouds and haze", "arXiv e-prints")
        self.assertEqual(len(merge_duplicates([journal, preprint])), 1)

    def test_series_papers_stay_separate(self):
        one = _pub("The TESS Grand Unified Hot Jupiter Survey. III. Thirty More Giant Planets", "ApJS", first="Yee, S")
        two = _pub("The TESS Grand Unified Hot Jupiter Survey. II. Twenty New Giant Planets", "arXiv e-prints", first="Yee, S")
        self.assertEqual(len(merge_duplicates([one, two])), 2)

    def test_different_first_author_stays_separate(self):
        a = _pub("A study of hot Jupiter clouds with JWST", "AJ", first="Savel, Arjun")
        b = _pub("A study of hot Jupiter clouds with JWST data", "arXiv e-prints", first="Smith, Jane")
        self.assertEqual(len(merge_duplicates([a, b])), 2)

    def test_citations_not_double_counted(self):
        journal = _pub("A Stellar magnesium to silicon ratio", "Nature Communications", citations=8)
        preprint = _pub("A Stellar Magnesium to Silicon ratio", "arXiv e-prints", citations=8)
        self.assertEqual(merge_duplicates([journal, preprint])[0]["citations"], 8)


def _citer(bibcode, title, pub, first="Smith, Jane", ids=()):
    return {"bibcode": bibcode, "title": title, "pub": pub,
            "authors": [first], "ids": sorted(set(ids) | {bibcode.lower()})}


class TestDistinctCiters(unittest.TestCase):
    def test_citing_preprint_and_journal_count_once(self):
        citing = [
            _citer("2026arXiv260100001S", "TSD: a survey of hot Jupiters", "arXiv e-prints", ids=["2601.00001"]),
            _citer("2026AJ....172....1S", "TSD: A Survey of Hot Jupiters", "The Astronomical Journal"),
            _citer("2025ApJ...900....2D", "Something else entirely", "The Astrophysical Journal", first="Doe, John"),
        ]
        self.assertEqual(count_distinct_citers(citing), 2)

    def test_shared_identifier_counts_once_even_if_titles_differ(self):
        citing = [
            _citer("2026arXiv260100001S", "Old preprint title", "arXiv e-prints", ids=["10.3847/xyz"]),
            _citer("2026AJ....172....1S", "Completely retitled journal paper", "The Astronomical Journal", ids=["10.3847/xyz"]),
        ]
        self.assertEqual(count_distinct_citers(citing), 1)

    def test_merge_uses_union_of_citers(self):
        shared = _citer("2026AJ....172....1S", "Citing paper A", "The Astronomical Journal")
        only_j = _citer("2026ApJ...901....3K", "Citing paper B", "The Astrophysical Journal", first="Kim, Lee")
        only_a = _citer("2026MNRAS.540....4P", "Citing paper C", "MNRAS", first="Patel, Ravi")
        journal = _pub("Peering into the Black Box", "The Astronomical Journal", citations=2)
        preprint = _pub("Peering into the Black Box", "arXiv e-prints", citations=2)
        journal["citing"], preprint["citing"] = [shared, only_j], [shared, only_a]
        merged = merge_duplicates([journal, preprint])
        self.assertEqual(merged[0]["citations"], 3)  # union; sum would be 4, max 2
        self.assertNotIn("citing", merged[0])

    def test_falls_back_to_max_without_citing_lists(self):
        journal = _pub("Same paper", "AJ", citations=4)
        preprint = _pub("Same paper", "arXiv e-prints", citations=1)
        self.assertEqual(merge_duplicates([journal, preprint])[0]["citations"], 4)

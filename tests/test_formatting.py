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
        pub = {"title": "SImMER: A Pipeline for Reducing and Analyzing Images of Stars"}

        res = check_inpress(pub)

        self.assertTrue(res)

    def test_format_inpress_unknown(self):
        pub = {"arxiv": "2209.11506", "title": "notinpress!"}

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
        self.assertTrue(res == "Savel, Arjun\etal")

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
            "othername, otherfirst\etal"  # + "\\ ({{{0}}} other co-authors, ".format(3)
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

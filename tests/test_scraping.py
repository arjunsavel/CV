import unittest

import gsheets

from cv.scripts.scrape_ads import *
from cv.scripts.scrape_google_scholar import *
from cv.scripts.scrape_joss import *


class TestGoogleScholar(unittest.TestCase):
    def test_clean_null_citation(self):
        citation = ""

        self.assertTrue(clean_citation(citation) == 0)

    def test_clean_int_citation(self):
        citation = "42"

        self.assertTrue(clean_citation(citation) == 42)

    def test_scholar_against_ads(self):
        author = "Savel, Arjun Baliga"
        scholar_results = get_scrape_google_scholar(author)
        ads_results = get_papers(author)

        ads_pubs = [ads_result["title"] for ads_result in ads_results]
        scholar_pubs = [scholar_result["title"] for scholar_result in scholar_results]

        np.testing.assert_array_equal(ads_pubs, scholar_pubs)


class TestADS(unittest.TestCase):
    def test_catch_bad_authorname(self):
        bad_authorname = "blblblblblblblblblblblblbl, blblblblblblblblblblblblbl blblblblblblblblblblblblbl"
        paper_dict = get_papers(bad_authorname)
        self.assertTrue(len(paper_dict) == 0)


class TestJOSS(unittest.TestCase):
    def test_correct_sheet(self):
        """
        There are specific columns expected in this sheet. Let's check one!
        todo: recast this as a function.
        """
        sheet_key = os.environ["SHEETS_SECRET"]
        joss_table = get_joss_table(sheet_key)
        self.assertTrue("Preferred Programming Languages" in joss_table.columns)

    def test_correct_counting(self):
        input_val = 2
        fake_joss_sheet = pd.DataFrame(
            {"username": ["arjunsavel"], "Review count(all time)": [input_val]}
        )
        num_reviews = count_num_reviews(fake_joss_sheet)
        self.assertTrue(num_reviews == input_val)

    def test_correct_counting_int(self):
        input_val = 2.0
        fake_joss_sheet = pd.DataFrame(
            {"username": ["arjunsavel"], "Review count(all time)": [input_val]}
        )
        num_reviews = count_num_reviews(fake_joss_sheet)
        self.assertTrue(type(num_reviews) == int)

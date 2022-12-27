import unittest

from cv.scrape_google_scholar import *
from cv.scrape_joss import *
from cv.scrape_ads import *

class TestGoogleScholar(unittest.TestCase):

    def test_clean_null_citation(self):
        citation = ''

        self.assertTrue(clean_citation(citation) == 0)

    def test_clean_int_citation(self):
        citation = '42'

        self.assertTrue(clean_citation(citation) == 42)

class TestADS(unittest.TestCase):
    def test_catch_bad_authorname(self):
        bad_authorname = 'blblblblblblblblblblblblbl, blblblblblblblblblblblblbl blblblblblblblblblblblblbl'
        paper_dict = get_papers(bad_authorname)
        self.assertTrue(len(paper_dict) == 0)


class TestJOSS(unittest.TestCase):

    def test_correct_sheet(self):
        """
        There are specific columns expected in this sheet. Let's check one!
        todo: recast this as a function.
        """
        sheet_key = os.environ['SHEETS_SECRET']
        joss_table = get_joss_table(sheet_key)
        self.assertTrue('Preferred Programming Languages' in joss_table.columns)

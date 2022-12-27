import unittest
from cv.scripts.format_pubs import *
class TestFormatStudent(unittest.TestCase):

    def test_format_student_not_in_pub(self):
        pub = {
                "arxiv": None,
                "authors": [
                  "Savel, Arjun B."
                ],
                "citations": 0,
                "doctype": None,
                "doi":  None,
                "page": None,
                "pub": None,
                "pubdate": "2022-12-00",
                "title": None,
                "url": None,
                "volume": None,
                "year": "2022"
              }
        pub_copy = pub.copy()
        pub_copy = format_for_students(pub_copy)
        self.assertTrue(pub==pub_copy)

    def test_format_student_in_pub(self):
        pub = {
                "arxiv": None,
                "authors": [
                  "Savel, Arjun B.",
                    "Arnold, Kenneth"
                ],
                "citations": 0,
                "doctype": None,
                "doi":  None,
                "page": None,
                "pub": None,
                "pubdate": "2022-12-00",
                "title": None,
                "url": None,
                "volume": None,
                "year": "2022"
              }
        pub_copy = pub.copy()
        pub_copy = format_for_students(pub_copy)
        self.assertTrue('*' == pub_copy['authors'][1][0])

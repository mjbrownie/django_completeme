from django.test import TestCase
from completeme.parser import Parser
import os
BASE_DIR = os.path.dirname(__file__)


class ParserTestCase(TestCase):

    """ Test cases for the completeme.parser.Parser Class"""

    def test_parser_load(self):
        """ checks return values for given positions on a test template  """
        filename = os.path.join(BASE_DIR, 'templates/completeme/test_parser_load.html')

        # point expexts {% load %} completes
        load_line, load_col = 10, 14
        parser = Parser(filename, load_line, load_col)

    def test_all_completion_types(self):

        filename = os.path.join(BASE_DIR, 'templates/completeme/test_parser_load.html')

        # point expexts {% load %} completes
        load_line, load_col = 10, 14
        parser = Parser(filename, load_line, load_col)

        print('staticfiles')
        print parser._staticfiles()

        print('tags')
        print parser._tags()

        print('filters')
        print parser._filters()

        print('templates')
        print parser._templates()

        print('blocks')
        print parser._blocks()

        print('urls')
        print parser._urls()


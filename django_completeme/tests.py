from django.test import TestCase
from django_completeme.parser import TemplateInspector, LineParser
import os
BASE_DIR = os.path.dirname(__file__)


class ParserTestCase(TestCase):

    """ Test cases for the django_completeme.inspector.Parser Class"""

    def test_parser_load(self):
        """ checks return values for given positions on a test template  """
        filename = os.path.join(BASE_DIR, 'templates/django_completeme/test_parser_load.html')

        # point expexts {% load %} completes
        load_line, load_col = 10, 14
        inspector = TemplateInspector(filename, load_line, load_col)

    def test_all_completion_types(self):

        filename = os.path.join(BASE_DIR, 'templates/django_completeme/test_parser_load.html')

        # point expexts {% load %} completes
        load_line, load_col = 10, 14
        inspector = TemplateInspector(filename, load_line, load_col)

        self.assertIsNotNone(inspector._staticfiles())
        self.assertIsNotNone(inspector._tags())
        self.assertIsNotNone(inspector._filters())
        self.assertIsNotNone(inspector._templates())
        self.assertIsNotNone(inspector._blocks())
        self.assertIsNotNone(inspector._urls())

    def test_line_parser(self):

        line = "    {{ }}"
        colno = 6
        self.assertNotEqual(LineParser(line, colno).in_a_var_tag(), None)
        self.assertEqual(LineParser(line, colno).is_variable(), True)
        self.assertNotEqual(LineParser(line, colno).is_filter(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_variables')

        line = "    {{ varname|  }} "
        colno = 15
        self.assertEqual(LineParser(line, colno).is_filter(), True)
        self.assertNotEqual(LineParser(line, colno).in_a_var_tag(), None)
        self.assertNotEqual(LineParser(line, colno).is_variable(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_filters')

        line = "    {% load "" %}"
        colno = 13
        self.assertEqual(LineParser(line, colno).is_load(), True)
        self.assertNotEqual(LineParser(line, colno).is_block(), True)
        self.assertNotEqual(LineParser(line, colno).is_url(), True)
        self.assertNotEqual(LineParser(line, colno).is_staticfile(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_loads')

        line = "    {% block  %}"
        colno = 13
        self.assertEqual(LineParser(line, colno).is_block(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_blocks')


        line = "    {%   %} "
        colno = 6
        self.assertEqual(LineParser(line, colno).is_tag(), True)
        self.assertNotEqual(LineParser(line, colno).is_block(), True)
        self.assertNotEqual(LineParser(line, colno).is_url(), True)
        self.assertNotEqual(LineParser(line, colno).is_staticfile(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_tags')


        line = "    {% url "" %} "
        colno = 12
        self.assertEqual(LineParser(line, colno).is_url(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_urls')

        line = "    {% static "" %} "
        colno = 15
        self.assertEqual(LineParser(line, colno).is_staticfile(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_staticfiles')


        line = "    {% extends "" %} "
        colno = 16
        self.assertEqual(LineParser(line, colno).is_template(), True)
        self.assertNotEqual(LineParser(line, colno).is_block(), True)
        self.assertNotEqual(LineParser(line, colno).is_url(), True)
        self.assertNotEqual(LineParser(line, colno).is_staticfile(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_templates')

        line = "    {% include "" %} "
        colno = 16
        self.assertEqual(LineParser(line, colno).is_template(), True)
        self.assertNotEqual(LineParser(line, colno).is_block(), True)
        self.assertNotEqual(LineParser(line, colno).is_url(), True)
        self.assertNotEqual(LineParser(line, colno).is_staticfile(), True)
        self.assertEqual(LineParser(line, colno).get_type(), '_templates')

        # some no matches
        line = "    {% include ""  "
        colno = 16
        self.assertNotEqual(LineParser(line, colno).is_template(), True)
        self.assertNotEqual(LineParser(line, colno).is_block(), True)
        self.assertNotEqual(LineParser(line, colno).is_url(), True)
        self.assertNotEqual(LineParser(line, colno).is_staticfile(), True)
        self.assertEqual(LineParser(line, colno).get_type(), None)

        line = "    }} ""  "
        colno = 16
        self.assertNotEqual(LineParser(line, colno).is_template(), True)
        self.assertNotEqual(LineParser(line, colno).is_block(), True)
        self.assertNotEqual(LineParser(line, colno).is_url(), True)
        self.assertNotEqual(LineParser(line, colno).is_staticfile(), True)
        self.assertEqual(LineParser(line, colno).get_type(), None)

    def test_context_detection(self):
        """ Context detection determines the completion type to be sent back to
        the client
        """
        filename = os.path.join(BASE_DIR, 'templates/django_completeme/test_parser_load.html')

        inspector = TemplateInspector(filename, 12, 14)

        self.assertIsNotNone(inspector.completions(12, 14))
        self.assertIsNotNone(inspector.completions(16, 14))
        self.assertIsNotNone(inspector.completions(21, 7))
        self.assertIsNotNone(inspector.completions(25, 16))
        self.assertIsNotNone(inspector.completions(25, 16))
        self.assertIsNotNone(inspector.completions(29, 11))
        self.assertIsNotNone(inspector.completions(33, 16))


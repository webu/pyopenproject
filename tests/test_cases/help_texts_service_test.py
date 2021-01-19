import json
import unittest

from business.service_factory import ServiceFactory
from model.help_text import HelpText


class HelpTextsServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.helpSer = ServiceFactory.get_help_texts_service()
        with open('../data/help_text.json') as f:
            self.help_text = HelpText(json.load(f))

    def test_find(self):
        self.assertNotNull(self.helpSer.find(self.help_text))

    def test_find_all(self):
        self.assertNotNull(self.helpSer.find_all())
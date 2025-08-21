import unittest

from crew_brief.model import Scraper
from crew_brief.model import ScraperStepTypeEnum
from crew_brief.model.scraper.scraper import validate_step

class DummyStep:

    def __init__(self, type_id, position=0, id=None):
        self.type_id = type_id
        self.position = position
        self.id = id


class TestScraperSteps(unittest.TestCase):

    def make_step(self, step_type, position=0):
        return DummyStep(step_type, position)

    def test_single_regex_and_schema(self):
        scraper = Scraper(name='test')
        regex = self.make_step(ScraperStepTypeEnum.REGEX, position=0)
        schema = self.make_step(ScraperStepTypeEnum.SCHEMA, position=2)
        func = self.make_step(ScraperStepTypeEnum.FUNCTION, position=1)

        scraper.steps = [regex, func, schema]

        # Should not raise
        for step in scraper.steps:
            validate_step(scraper, step)

    def test_function_order_violation(self):
        scraper = Scraper(name='test2')
        regex = self.make_step(ScraperStepTypeEnum.REGEX, position=1)
        schema = self.make_step(ScraperStepTypeEnum.SCHEMA, position=2)
        # Wrong position
        func = self.make_step(ScraperStepTypeEnum.FUNCTION, position=0)

        scraper.steps = [regex, func, schema]

        with self.assertRaises(ValueError):
            for step in scraper.steps:
                validate_step(scraper, step)

        raise ValueError


if __name__ == '__main__':
    unittest.main()

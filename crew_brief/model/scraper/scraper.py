from itertools import pairwise

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from crew_brief.model.base import Base
from crew_brief.model.mixin import ByMixin
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin
from crew_brief.util import load_from_path

from .scraper_step import ScraperStepTypeEnum

class Scraper(
    Base,
    ByMixin,
    NonEmptyStringMixin,
    TimestampMixin,
):
    """
    Object that scrapes files for data to produce LegIdentifier objects.
    """

    human_description = (
        'Scrape filename with regexes until success'
        ' and deserialize with schema.'
    )

    __tablename__ = 'scraper'

    id = Column(Integer, primary_key=True)

    name = Column(
        String,
        nullable = False,
        unique = True,
    )

    description = Column(
        Text,
        nullable = True,
    )

    _steps = relationship(
        'ScraperStep',
        back_populates = 'scraper',
        collection_class = ordering_list('position'),
        order_by = 'ScraperStep.position',
    )

    @hybrid_property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, steps):
        """
        Validate scraper steps are ordered correctly.
        """
        # Raise for missing required types. Comparing model to enum member.
        for required_member in ScraperStepTypeEnum.__required__:
            if not any(step.type_id == required_member for step in steps):
                raise ValueError(
                    f'Required StepType {required_member} not found')

        for step1, step2 in pairwise(steps):
            if step2.step_type.member < step1.step_type.member:
                raise ValueError(f'{step1} must come before {step2}')

        self._steps = steps

    regexes = relationship(
        'Regex',
        back_populates = 'scraper',
        foreign_keys = 'Regex.scraper_id',
        order_by = 'Regex.position',
        doc =
            'Regex objects produce capture groups for the associated schema to'
            ' process. First regex to succeed is used.',
    )

    postmatch_handler = Column(
        String,
        nullable = True,
        doc = 'Dotted path to a callable that processes the file after first successful regex.',
    )

    schema_id = Column(Integer, ForeignKey('schema.id'))

    schema_object = relationship(
        'Schema',
    )

    def compiled_regexes(self):
        regexes = {}
        for regex_object in self.regexes:
            regexes[regex_object] = regex_object.compile_pattern()
        return regexes

    def first_match(self, path):
        for regex_object, regex in self.compiled_regexes().regexes.items():
            match = regex.match(path)
            if match:
                return (regex_object, regex, match)

    def get_postmatch_handler(self):
        return load_from_path(self.postmatch_handler)

    def __html__(self):
        return self.name

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

from crew_brief.model.base import Base
from crew_brief.model.mixin import ByMixin
from crew_brief.model.mixin import NonEmptyStringMixin
from crew_brief.model.mixin import TimestampMixin
from crew_brief.util import load_from_path

class Scraper(
    Base,
    ByMixin,
    NonEmptyStringMixin,
    TimestampMixin,
):
    """
    Object that scrapes files for data to produce LegIdentifier objects.
    """

    human_description = 'Scrape filename with regexes until success and deserialize with schema.'

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

    steps = relationship(
        'ScraperStep',
        back_populates = 'scraper',
        collection_class = ordering_list('position'),
        order_by = 'ScraperStep.position',
    )

    @validates('steps')
    def validate_steps(self, key, step):
        """
        Enforce:
        1. At least one Regex step must exist.
        2. At least one Schema step must exist.
        3. Function steps (if any) must come after Regex but before Schema.
        """
        from .scraper_step import ScraperStepTypeEnum

        # Gather all current + new steps (after flush)
        all_steps = [s for s in self.steps if s is not None]

        # Check type counts
        regex_steps = [s for s in all_steps if s.type_id == ScraperStepTypeEnum.REGEX]
        schema_steps = [s for s in all_steps if s.type_id == ScraperStepTypeEnum.SCHEMA]
        function_steps = [s for s in all_steps if s.type_id == ScraperStepTypeEnum.FUNCTION]

        # Must have exactly one regex and one schema
        if len(regex_steps) > 1:
            raise ValueError('Scraper may only have one Regex step')

        if len(schema_steps) > 1:
            raise ValueError('Scraper may only have one Schema step')

        # If both regex + schema exist, enforce ordering
        if regex_steps and schema_steps:
            regex_order = regex_steps[0].position
            schema_order = schema_steps[0].position
            if regex_order >= schema_order:
                raise ValueError('Regex step must come before Schema step')

            for funcstep in function_steps:
                if not (regex_order < funcstep.position < schema_order):
                    raise ValueError(
                        f"Function step {funcstep.id or '?'} must be ordered after Regex and before Schema"
                    )

        return step

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


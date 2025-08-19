import datetime
import logging
import os

import sqlalchemy as sa

from marshmallow import ValidationError

from crew_brief.model import Airline
from crew_brief.model import Airport
from crew_brief.model import FlightNumber
from crew_brief.model import LegFile
from crew_brief.model import LegIdentifier
from crew_brief.model import OFPVersion
from crew_brief.model import OSWalk
from crew_brief.model import OriginDate
from crew_brief.model import Scraper
from crew_brief.query import select_leg_files_for_walker
from crew_brief.query import select_unparsed_leg_files_for_walker

logger = logging.getLogger(__name__)

def objects_from_data(session, data):
    # Airline and Airport objects must exist.
    airline = Airline.one_by_iata(session, data['airline_iata'])
    departure_airport = Airport.one_by_iata(session, data['departure_iata'])
    destination_airport = Airport.one_by_iata(session, data['destination_iata'])

    # Get or create objects.
    flight_number = FlightNumber.get_or_create_by_flight_number(session, data['flight_number'])
    origin_date = OriginDate.get_or_create_by_origin_date(session, data['origin_date'])
    ofp_version_object = OFPVersion.get_or_create_by_dict(session, data['ofp_version'])

    datetime_value = data.get('datetime')

    objects = {
        'airline': airline,
        'departure_airport': departure_airport,
        'destination_airport': destination_airport,
        'flight_number': flight_number,
        'origin_date': origin_date,
        'ofp_version_object': ofp_version_object,
        'datetime_value': datetime_value,
    }
    return objects

def leg_identifier_from_objects(session, objects):
    leg_identifier = LegIdentifier.get_or_create_from_parse(
        session,
        objects['airline'],
        objects['flight_number'],
        objects['origin_date'],
        objects['departure_airport'],
        objects['destination_airport'],
        objects['ofp_version_object'],
        objects['datetime_value'],
    )
    return leg_identifier

def parse_leg_identifiers(session, os_walk_name, scraper_name, force=False, silent=True):
    """
    Parse existing file objects created from named OSWalk object with named
    Scraper object.
    :param force:
        Process all files for OSWalk object and Scraper.
    """
    # Load objects from arguments.
    os_walk = OSWalk.by_name(session, os_walk_name)
    scraper = Scraper.by_name(session, scraper_name)

    # Make schema instance.
    schema_class = scraper.schema_object.schema_class()
    schema = schema_class()

    # Build regex from os_walk and command line args.
    regexes = scraper.compiled_regexes()

    # LegFile objects generated from the stated os_walk object.
    if force:
        stmt = select_leg_files_for_walker(os_walk)
    else:
        stmt = select_unparsed_leg_files_for_walker(os_walk)
    leg_files = session.scalars(stmt)

    for leg_file in leg_files:
        # Clear the force parse flag if set.
        if leg_file.force_parse:
            action = 'force_parse'
            leg_file.force_parse = False
        else:
            action = 'parse'

        # Try all regexes associated with scraper.
        for regex_object, regex in regexes.items():
            # Parse filename with regex.
            match = regex.match(leg_file.path)
            if not match:
                continue

            # Load data from filename strings.
            string_data = match.groupdict()

            # Run extra parsing, like reading the file for more data.
            if scraper.postmatch_handler:
                handler = scraper.get_postmatch_handler()
                string_data.update(handler(leg_file.path))

            try:
                data = schema.load(string_data)
            except ValidationError:
                logger.exception('An exception occured during schema load.')
                if not silent:
                    raise
                continue

            # Get or create database objects from data.
            objects = objects_from_data(session, data)

            # Get or create LegIdentifier object.
            leg_identifier = leg_identifier_from_objects(session, objects)
            leg_identifier.scraped_by = scraper

            # Update LegFile object.
            leg_file.leg_identifier = leg_identifier
            leg_file.parse_exception_at = None
            leg_file.parse_regex = regex_object

            logger.debug('%s %s -> %s', action, os.path.normpath(leg_file.path), data)
            # break on first regex to match, go to next leg_file
            break
        else:
            # No break in regex loop. All regexes failed. Mark file to avoid parsing again.
            leg_file.parse_exception_at = datetime.datetime.now()
            leg_file.parse_regex = None
            logger.debug('no regex match %s', os.path.normpath(leg_file.path))

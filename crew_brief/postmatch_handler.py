import contextlib
import os
import re

import pdfplumber

ofp_header_re = re.compile(
    r'(?P<airline_iata>[A-Z]{2})'
    r' (?P<flight_number>[A-Z\d]{1,6})'
    r'/(?P<origin_date>\d{1,2}[A-Z][a-z]{2}\d{2})'
    r'/(?P<departure_iata>[A-Z]{3})'
    r'-(?P<destination_iata>[A-Z]{3})'
    r' Reg:(?P<aircraft_registration>[A-Z\d]{2,8})'
    r' OFP:(?P<ofp_version>\d+/\d+/\d+)'
)

def scrape_lcb_pdf(path):
    """
    Scrape contents of LBC PDF and return dict.
    """
    # Silence pdfplumber
    with contextlib.redirect_stderr(open(os.devnull, 'w')):
        with pdfplumber.open(path) as pdf:
            match = None
            for page in pdf.pages:
                page_text = page.extract_text() or ''
                for line in page_text.splitlines():
                    match = ofp_header_re.match(line)
                    if match:
                        return match.groupdict()

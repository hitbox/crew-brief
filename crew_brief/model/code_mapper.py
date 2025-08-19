import csv

from crew_brief.util import invert_dict
from crew_brief.util import is_one

class CodeMapper:
    """
    Convert IATA to ICAO and vice verse.
    """

    def __init__(self, *, iata_to_icao=None, icao_to_iata=None):
        if not is_one(iata_to_icao, icao_to_iata):
            raise ValueError(
                'Must provide exactly one of "iata_to_icao" or "icao_to_iata".')

        # Save the one given and invert the other strictly, raising for
        # duplicate keys.
        self.iata_to_icao = iata_to_icao or invert_dict(icao_to_iata, strict=True)
        self.icao_to_iata = icao_to_iata or invert_dict(iata_to_icao, strict=True)

    @classmethod
    def from_csv(cls, filename, iata_fieldname, icao_fieldname):
        """
        Load conversions from CSV file with a header.
        """
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            iata_to_icao = {row[iata_fieldname]: row[icao_fieldname] for row in reader}

        return cls(iata_to_icao=iata_to_icao)

    def iata(self, icao):
        """
        Get IATA code from ICAO.
        """
        return self.icao_to_iata[icao]

    def icao(self, iata):
        """
        Get ICAO code from IATA.
        """
        return self.iata_to_icao[iata]

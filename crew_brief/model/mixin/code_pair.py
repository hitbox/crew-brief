import sqlalchemy as sa

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import declared_attr

class CodePairMixin:
    """
    Mixin IATA and ICAO codes.
    """

    @declared_attr
    def iata_code(cls):
        return Column(
            String,
            nullable = False,
            unique = True,
            info = {
                'label': 'IATA',
            },
        )

    @declared_attr
    def icao_code(cls):
        return Column(
            String,
            nullable = False,
            unique = True,
            info = {
                'label': 'ICAO',
            },
        )

    @classmethod
    def one_by_iata(cls, session, iata_code):
        return session.scalars(sa.select(cls).where(cls.iata_code == iata_code)).one()

    @classmethod
    def one_by_icao(cls, session, icao_code):
        return session.scalars(sa.select(cls).where(cls.icao_code == icao_code)).one()

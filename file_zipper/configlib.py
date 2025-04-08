import configparser

import sqlalchemy as sa

from .sql_function import register_functions

APPNAME = 'file_zipper'

def config_from_args(args):
    configs = args.config or []
    if not args.config:
        configs.append('instance/config/file_zipper.ini')

    cp = configparser.ConfigParser()
    cp.read(configs)

    return cp

def url_from_config(cp):
    return sa.URL.create(**cp['database.' + cp[APPNAME]['database']])

def session_from_config(cp):
    url = url_from_config(cp)
    engine = sa.create_engine(url)
    sa.event.listen(engine, 'connect', register_functions)
    Session = sa.orm.sessionmaker(bind=engine)
    session = Session()
    return session

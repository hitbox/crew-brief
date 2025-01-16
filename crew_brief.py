import argparse
import configparser
import glob
import json
import os
import re
import zipfile

from operator import itemgetter

import jinja2
import openpyxl

NAME = os.path.splitext(os.path.basename(__file__))[0]

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        'templates',
    ),
    autoescape = jinja2.select_autoescape(),
)

class Glob:

    def __init__(self, pathname, recursive=False):
        self.pathname = pathname
        self.recursive = recursive

    def __iter__(self):
        path_iter = glob.iglob(
            self.pathname,
            recursive = self.recursive,
        )
        yield from path_iter


class UserEvents:

    def __init__(self, data):
        self.data = data

    def to_rows(self):
        rows = []

        first_fields = ('eventTimeStamp', 'status', 'eventType')
        get_first = itemgetter(*first_fields)

        for user_event in self.data['userEvents']:
            first = get_first(user_event)
            remaining = user_event.get('eventDetails', {}).items()
            remaining = tuple(val for key, val in remaining if key not in first_fields)
            rows.append(first + remaining)
        return rows


class UserFriendlyCrewBrief:

    def __init__(self, sources, members):
        """
        :param sources: List of iterables of source paths to zip files.
        :param members: List of patterns for members of zips.
        """
        self.sources = sources
        self.members = members

    @classmethod
    def from_config(cls, cp, name):
        section = cp[f'process.{name}']

        sources = split_sections(section['sources'])
        sources = [instance_from_config(cp, name, 'source.') for name in sources]

        members = split_sections(section['members'])
        members = [re.compile(member) for member in members]

        instance = cls(sources, members)
        return instance

    def iter_zip_paths(self):
        for source in self.sources:
            for zip_path in source:
                yield zip_path

    def iter_zip_members(self, zip_file):
        for member_name in zip_file.namelist():
            for member_pattern in self.members:
                if member_pattern.match(member_name):
                    yield member_name

    def __call__(self):
        html_template = template_env.get_template('crew_brief_table.html')
        for zip_path in self.iter_zip_paths():
            with zipfile.ZipFile(zip_path) as zip_file:
                import sys
                print(zip_path, file=sys.stderr)
                for member_name in self.iter_zip_members(zip_file):
                    with zip_file.open(member_name) as member_file:
                        from pprint import pprint
                        member_json = member_file.read()
                        member_data = json.loads(member_json)
                        if 'eventDetails' in member_data and member_data['eventDetails']:
                            html = html_template.render(**member_data)
                            print(html)
                            raise
                        #user_events = UserEvents(member_data)
                        #rows = user_events.to_rows()
                        #pprint(rows)
                        #raise


def instance_from_config(cp, secname, prefix, globals=None, locals=None):
    """
    Eval to instantiate from config.
    """
    section = cp[f'{prefix}{secname}']
    class_ = eval(section['class'], globals, locals)
    args = eval(section.get('args', 'tuple()'), globals, locals)
    kwargs = eval(section.get('kwargs', 'dict()'), globals, locals)
    return class_(*args, **kwargs)

def split_sections(string):
    return string.split()

def main(argv=None):
    parser = argparse.ArgumentParser(
        description =
            'Rewrite crew brief JSON files as more user friendly Excel files.',
    )
    parser.add_argument(
        '--config',
        help = 'Path to configuration.',
    )
    args = parser.parse_args(argv)

    config_path = args.config or os.getenv(f'{NAME.upper()}_CONFIG') or []

    cp = configparser.ConfigParser()
    cp.read(config_path)

    appsec = cp['crew_brief']

    processes = split_sections(appsec['processes'])
    processes = [UserFriendlyCrewBrief.from_config(cp, secname) for secname in processes]
    for process in processes:
        process()

if __name__ == '__main__':
    main()

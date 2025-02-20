import json
import re
import zipfile

import jinja2

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        'templates',
    ),
    autoescape = jinja2.select_autoescape(),
)

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

    def iter_bare(self):
        for zip_path in self.iter_zip_paths():
            with zipfile.ZipFile(zip_path) as zip_file:
                for member_name in self.iter_zip_members(zip_file):
                    with zip_file.open(member_name) as member_file:
                        member_json = member_file.read()
                        member_data = json.loads(member_json)
                        yield dict(
                            zip_path = zip_path,
                            zip_file = zip_file,
                            member_name = member_name,
                            member_file = member_file,
                            member_json = member_json,
                            member_data = member_data,
                        )

    def __call__(self):
        html_template = template_env.get_template('crew_brief_table.html')

        crew_briefs = []
        for zip_path in self.iter_zip_paths():
            if len(crew_briefs) == 20:
                break
            with zipfile.ZipFile(zip_path) as zip_file:
                for member_name in self.iter_zip_members(zip_file):
                    with zip_file.open(member_name) as member_file:
                        member_json = member_file.read()
                        member_data = json.loads(member_json)
                        template_context = dict(
                            zip_namelist = zip_file.namelist(),
                            zip_path = zip_path,
                            member_name = member_name,
                            member_data = member_data,
                            show_data = False,
                        )
                        crew_briefs.append(template_context)
        html = html_template.render(crew_briefs=crew_briefs)
        print(html)

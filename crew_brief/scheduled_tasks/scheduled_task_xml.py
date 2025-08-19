import datetime
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import win32security

from xml.dom import minidom

class SchtasksXML:
    """
    Create XML element trees for creating scheduled tasks.
    """

    def __init__(self, element_maker):
        self.E = element_maker

    def trigger_every_minutes(
        self,
        interval_minutes,
        start_boundary = None
    ):
        calendar = self.E('CalendarTrigger')

        repetition = self.E('Repetition')
        repetition.append(self.E('Interval', text=f'PT{interval_minutes}M'))
        repetition.append(self.E('Duration', text='P1D'))
        repetition.append(self.E('StopAtDurationEnd', text='false'))
        calendar.append(repetition)

        if start_boundary is None:
            start_boundary = midnight()
        calendar.append(self.E('StartBoundary', text=start_boundary.strftime('%Y-%m-%dT%H:%M:%S')))

        calendar.append(self.E('Enabled', text='true'))
        schedule_by_day = self.E('ScheduleByDay')
        schedule_by_day.append(self.E('DaysInterval', text='1'))
        calendar.append(schedule_by_day)

        return calendar

    def create_task_xml(
        self,
        task_name,
        script_path,
        python_path,
        interval_minutes,
        working_dir = None,
        description = None,
        trigger_type = 'Logon',
        run_as_user = None,
    ):
        ET.register_namespace('', ns)
        E = NSElementMaker(namespace=ns)

        task = self.E('Task', attrib={'version': '1.2'})

        registration_info = self.E('RegistrationInfo')
        if description:
            registration_info.append(self.E('Description', text=description))
        task.append(registration_info)

        principals = self.E('Principals')
        # TODO
        # - Support service account.
        # - Will need admin privileges.
        # - Decide what LogonType should be.
        principal = self.E('Principal', attrib={'id': 'Author'})
        if run_as_user:
            principal.append(self.E('UserId', text=run_as_user))
        #
        #principal.append(self.E('LogonType', text='None'))
        principal.append(self.E('RunLevel', text='LeastPrivilege'))
        principals.append(principal)
        task.append(principals)

        triggers = self.E('Triggers')
        calendar = self.trigger_every_minutes(interval_minutes)
        triggers.append(calendar)
        task.append(triggers)

        settings = self.E('Settings')
        settings.append(self.E('MultipleInstancesPolicy', 'IgnoreNew'))
        settings.append(self.E('StartWhenAvailable', 'true'))
        settings.append(self.E('Enabled', 'true'))
        settings.append(self.E('Hidden', 'false'))
        settings.append(self.E('ExecutionTimeLimit', 'PT0S'))
        task.append(settings)

        actions = self.E('Actions', attrib={'Context': 'Author'})
        exec_elem = self.E('Exec')
        exec_elem.append(self.E('Command', python_path))
        exec_elem.append(self.E('Arguments', script_path))
        if working_dir:
            exec_elem.append(self.E('WorkingDirectory', working_dir))
        actions.append(exec_elem)
        task.append(actions)

        return ET.ElementTree(task)

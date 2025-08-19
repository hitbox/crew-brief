import datetime
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import win32security

from xml.dom import minidom

def register_task(
    task_name,
    script_path,
    python_path,
    interval_minutes,
    working_dir = None,
    description = None,
    remove_exists = False,
    run_as_user = None,
):
    """
    Create scheduled task to run every N minutes.
    """
    schtaskxml = SchtasksXML(NSElementMaker(ns))
    xml_tree = schtaskxml.create_task_xml(
        task_name,
        script_path,
        python_path,
        interval_minutes,
        working_dir = working_dir,
        description = description,
        run_as_user = run_as_user,
    )

    # Write XML to temporary file without deleting.
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as xml_file:
        xml_tree.write(xml_file, encoding='utf-16', xml_declaration=True)
        temp_xml_path = xml_file.name

    # Build subprocess command.
    cmd = ['schtasks', '/create', '/TN', task_name, '/XML', temp_xml_path]

    # Create scheduled task, removing if exists and configured to do so.
    # Finally, remove temporary file.
    try:
        if task_exists(task_name):
            if not remove_exists:
                raise ValueError('Task already exists.')
            delete_task(task_name)
        run(cmd)
    finally:
        os.remove(temp_xml_path)

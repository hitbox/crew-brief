import datetime
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import win32security

from xml.dom import minidom

def run(cmd, **kwargs):
    """
    Convenience for running commands silently.
    """
    kwargs.setdefault('check', True)
    kwargs.setdefault('capture_output', True)
    return subprocess.run(cmd, **kwargs)

def change_task(task_name, command):
    assert command in set(['/disable', '/enable'])
    cmd = ['schtasks', '/change', '/tn', task_name, command]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(result.stdout)

def disable_task(task_name):
    return change_task(task_name, '/disable')

def enable_task(task_name):
    return change_task(task_name, '/enable')

def delete_task(task_name):
    return run(['schtasks', '/delete', '/tn', task_name, '/f'])

def task_exists(task_name):
    """
    Return if a task name exists.
    """
    cmd = ['schtasks', '/query', '/tn', task_name]
    try:
       run(cmd)
       return True
    except subprocess.CalledProcessError:
       return False

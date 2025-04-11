"""
Styling for Excel workbooks.
"""
import pickle

from crew_brief.model import Styling

def from_workbook(args):
    filename = args.file
    prefix = args.prefix
    styling = Styling.from_workbook(filename, prefix)
    with open('test.pickle', 'wb') as pickle_file:
        pickle.dump(styling, pickle_file)

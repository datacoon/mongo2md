from copy import copy
import os
import csv
import sys
import json
from random import randint
from pymongo import MongoClient
from ..scheme import generate_scheme
from pprint import pprint
from bson.json_util import loads, dumps

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def _load_fields(filename):
    dr = csv.DictReader(open(filename, 'r', encoding='utf8'), delimiter=';')
    field_values = {}
    all = []
    for r in dr:
        all.append(r)
        if len(r['description']) > 0:
            key = r['name'].rsplit('.')[-1]
            if key in field_values.keys():
                field_values[key].append(r['description'])
            else:
                field_values[key] = [r['description'], ]
    return field_values

class Suggester:
    def __init__(self, fields_file):
        self.fieldmap = _load_fields(fields_file)
        pass

    def suggester(self, projpath):
        tab_file = open(os.path.join(projpath, 'tables.csv'), 'r', encoding='utf8')
        reader = csv.DictReader(tab_file, delimiter=';')
        tables = []
        for table in reader:
            tables.append(table)
        tab_file.close()

        for table in tables:
            all_records = []
            f = open(projpath + '/%s_fields.csv' % table['name'], 'r', encoding='utf8')
            dr = csv.DictReader(f, delimiter=';')
            dw = csv.DictWriter(open(projpath + '/%s_fields.csv' % table['name'] + '.temp', 'w', encoding='utf8'), delimiter=';', fieldnames=dr.fieldnames)
            dw.writeheader()
            for r in dr:
                if len(r['description']) == 0:
                    key = r['name'].rsplit('.')[-1]
                    if key in self.fieldmap.keys():
                        for value in self.fieldmap[key]:
                            answer = query_yes_no('Suggestion: ' + r['name'] + ' = ' + value)
                            if answer:
                                r['description'] = value
                                break
                dw.writerow(r)
            f.close()

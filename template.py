"""
File: template.py
Description: Template management
"""

import requests
import csv
import re
import clipboard
import argparse
import pickle
from termcolor import colored


pattern_re = re.compile(r"(\[.*\])")
variable_re = re.compile(r"(\{[^}]*\})")

csv_url      = 'https://docs.google.com/spreadsheets/d/1H5QDqLZ2g774wmZ4A_Xq5Hx88yJHi8eB2dNxDX-KuHQ/pub?output=csv'
pkl_filename = '/home/driquet/perso/reviewing/templates.pkl'
csv_filename = '/home/driquet/perso/reviewing/templates.csv'


class Template:
    def __init__(self, value, score):
        self.value = value
        self.score = score


class TemplateContext:
    def __init__(self):
        self.templates = {}
        self.patterns = {}

    def add_template(self, name, value, score=0):
        self.templates[name] = Template(value, score)

    def add_pattern(self, name, value):
        self.patterns[name] = value

    def list_templates(self):
        max_len = max([len(key) for key in self.templates.keys()])

        for key, tpl in sorted(self.templates.items(), key=lambda x: x[1].score):
            txt = tpl.value.replace('\n', '')
            print('%s%s%s%s' % (
                    colored('%4d:' % tpl.score, 'yellow'),
                    colored('%s' % key, 'red', attrs=['bold']),
                    colored(':', 'yellow'),
                    colored('%s' % txt[:120 - len(key)], 'white', attrs=['dark'])
                ))

    def expand_template(self, key):
        content = self.templates[key].value
        match = pattern_re.search(content)

        while True:
            occ = False
            for m in pattern_re.finditer(content):
                pattern_name = m.group(1)
                if pattern_name in self.patterns:
                    occ = True
                    content = content.replace(pattern_name, self.patterns[pattern_name])
            if not occ:
                break

        return content

    def expand_variables(self, template):
        while True:
            occ = False
            m = variable_re.search(template)
            if m is not None:
                var_name = m.group(1)[1:-1]
                value = input("--> %s = " % var_name)
                template = template[:m.start()] + value + template[m.end():]
            else:
                break
        return template


    def get_template(self, key):
        if key in self.templates:
            template = self.expand_template(key)
            template = self.expand_variables(template)
            self.templates[key].score += 1
            return template
        return None

def fetch_templates(url, filename, cert=False):
    """ Fetch online a csv combining available templates and store it locally """
    r = requests.get(url, verify=False)
    if r.status_code != 200:
        return -1

    # Decode the csv content
    content = r.text.encode('iso-8859-1').decode('utf-8')

    with open(filename, 'w') as f:
        f.write(content)

    return filename

def load_templates_from_csv(filename):
    with open(filename) as csvfile:
        templates = csv.reader(csvfile)
        context = TemplateContext()

        for key, value in templates:
            key = key.strip()
            value = value.strip()

            if key.startswith('['):
                context.add_pattern(key, value)
            else:
                context.add_template(key, value)

        return context
    return None

def load_context(filename):
    try:
        with open(filename, 'rb') as pklfile:
            return pickle.load(pklfile)
    except FileNotFoundError:
        return None

def save_context(context, filename):
    with open(filename, 'wb') as pklfile:
        pickle.dump(context, pklfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Template expension process")
    parser.add_argument('--refresh', '-r', action="store_true", help='Fetch online the csv to update local template')
    parser.add_argument('--clipping', '-c', action="store_true", help='Copy the result into the clipboard')
    parser.add_argument('--list', '-l', action="store_true", help='List available templates')
    parser.add_argument('name', nargs='?', help='Name of the template')
    args = parser.parse_args()

    # Load the context
    context = load_context(pkl_filename)
    if context is None:
        context = load_templates_from_csv(csv_filename)

    if args.refresh:
        fetch_templates(csv_url, csv_filename)
        context = load_templates_from_csv(csv_filename)
        save_context(context, pkl_filename)

    if args.list:
        context.list_templates()

    if args.name is not None:
        template = context.get_template(args.name)
        if args.clipping:
            clipboard.copy(template)
        else:
            print(template)

        save_context(context, pkl_filename)



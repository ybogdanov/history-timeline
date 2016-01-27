#!/usr/bin/python

import sys
import json
import re
import argparse
from operator import itemgetter

parser = argparse.ArgumentParser(description='Imports dataset from Pantheon.')
parser.add_argument('-d', '--debug', default=None,
                   help='shows debug redirect information on a given name (default: None)')
parser.add_argument('redirects', nargs=argparse.REMAINDER)
args = parser.parse_args()

pantheon_data = json.load(sys.stdin)
redirects = {}
dups = {}
result = []

types = {
  "SPORTS": {
    "*": "sports",
  },
  "ARTS": {
    "MUSICIAN":  "music",
    "SINGER":    "music",
    "COMPOSER":  "music",
    "CONDUCTOR": "music",
    "*":         "arts",
  },
  "SCIENCE & TECHNOLOGY": {
    "INVENTOR": "invention",
    "*":        "science",
  },
  "PUBLIC FIGURE": {
    "MAFIOSO": "criminal",
    "*":       "public",
  },
  "ART": {
    "*": "arts",
  },
  "PHIL": {
    "*": "science", # Really?
  },
  "MUSIC": {
    "*": "music",
  },
  "INSTITUTIONS": {
    "DIPLOMAT":           "politics",
    "POLITICIAN":         "politics",
    "MILITARY PERSONNEL": "military",
    "RELIGIOUS FIGURE":   "religion",
    "NOBLEMAN":           "public",   # Really?
    "PILOT":              "military", # Really?
    "PUBLIC WORKER":      "public",
    "*":                  "other",
  },
  "HUMANITIES": {
    "PHILOSOPHER": "science", # Really?
    "WRITER":      "arts",
    "HISTORIAN":   "science", # Really?
    "LINGUIST":    "science",
    "*":           "other",
  },
  "BUSINESS & LAW": {
    "PRODUCER":       "other",
    "LAWYER":         "business", # m?
    "BUSINESSPERSON": "business",
    "*":              "other",
  },
  "EXPLORATION": {
    "*": "explorer",
  },
  "SCIENCE": {
    "*": "science",
  },
  "LIT": {
    "*": "other",
  },
}

for f in args.redirects:
  with open(f) as fd:
    redirects.update(json.load(fd))

for input_person in pantheon_data:
  name = input_person['name']
  if name.lower() in redirects and redirects[name.lower()] != name:
    name = redirects[name.lower()]

  if args.debug is not None and args.debug.lower() in input_person['name'].lower():
    sys.stderr.write("[DEBUG] %s -> %s \n" % (input_person['name'], name))

  # TODO: process names like "Ziegler, Karl" -> "Karl Ziegler"?

  if name in dups: continue
  dups[name] = True

  person = {
    'name': name,
    'type': types[input_person['domain']]['*'],
    'rating': 1.0 / 32.0 * input_person.get('HPI', 0), # =0..1 (max HPI is 32.0)
    'country': input_person['countryName'].title(),
    'from': input_person['birthyear']
  }

  if input_person['occupation'] in types[input_person['domain']]:
    person['type'] = types[input_person['domain']][input_person['occupation']]

  if person['from'] == 'Unknown' or person['from'] == '':
    continue

  if isinstance(person['from'], basestring):
    digits = [int(y) for y in re.findall(r'\d+', person['from'])]
    if len(digits) == 0:
      sys.stderr.write('Cannot parse birth year for %s: %s\n' % (person['name'], person['from']))
      continue
    person['from'] = digits[0]

  result.append(person)

sorted_result = sorted(result, key=itemgetter('name'))

print json.dumps(sorted_result, indent=4, separators=(',', ': '))


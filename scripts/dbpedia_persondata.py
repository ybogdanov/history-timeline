#!/usr/bin/env python

"""
Here I don't use RDF lib because it is tricky to compile and therefore not good for
an open-source project. Since the document is very simple, I parse it as strings.

See http://wiki.dbpedia.org/Downloads2015-04
The input file is Persondata_en.nt

Direct download link: http://downloads.dbpedia.org/2015-04/core-i18n/en/persondata_en.nt.bz2
"""

import sys
import urllib
import re
import json
import dateutil.parser
from operator import itemgetter

pref = "http://dbpedia.org/resource/"

def parseDate(line):
  ds = line[1:line.index('"', 1)]

  # skip dates like "--09-21", a lot of them
  if re.match(r'^\-\-\d{2}\-\d{2}', ds):
    return None
  
  m = re.match(r'^(\-)?(\d{4}\-\d{2}\-\d{2}|\d{4})$', ds)

  if not m:
    sys.stderr.write("Cannot parse date: %s\n" % ds)
    return None

  # Handle dates like "0031"
  if re.match(r'^\-?00\d{2}$', ds):
    year = int(ds)
  else:
    try:
      year = dateutil.parser.parse(ds).year
    except:
      sys.stderr.write("Cannot parse date: %s, error %s\n" % (ds, sys.exc_info()[0]))
      return None

  if m.group(1) != None:
    year *= -1

  return year


people = {}
total = 8397083.0

for i, line in enumerate(sys.stdin):
  parts = line.split(" ")
  name = urllib.unquote(parts[0][len(pref)+1:len(parts[0])-1]).decode('utf8').replace("_", " ")

  # if i == 30000: break

  if not name in people:
    people[name] = {"name": name}

  if i % 100000 == 0:
    sys.stderr.write("%d/%d (%0.0f%%)\n" % (i, total, 100 / total * i))

  if "birthDate" in parts[1]:
    year = parseDate(parts[2])
    if year is not None:
      people[name]["from"] = year

  if "deathDate" in parts[1]:
    year = parseDate(parts[2])
    if year is not None:
      people[name]["to"] = year

result = []

for name in people:
  if "from" in people[name] or "to" in people[name]:
    result.append(people[name])

sorted_result = sorted(result, key=itemgetter('name'))

print json.dumps(sorted_result, indent=4, separators=(',', ': '))





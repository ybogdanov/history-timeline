#!/usr/bin/python

import sys
import json
import argparse
from operator import itemgetter

curr_year = 2016
max_age = 150
result = []
dups = {}
missing = []

parser = argparse.ArgumentParser(description='Finalizes the dataset, sorts by rating.')
parser.add_argument('--limit', default=None, type=int,
                   help='limits the number of resulting people (default: None)')

args = parser.parse_args()

for p in json.load(sys.stdin):

  if 'to' not in p:
    p['to'] = 0
  
  if p['from'] == 0 or p['from'] == None:
    p['missing_reason'] = "missing birth year (from)"
    missing.append(p)
    continue

  if p['to'] == 0 and curr_year-p['from'] > max_age:
    p['missing_reason'] = "is older then %d years and is missing death year" % max_age
    missing.append(p)
    continue

  age = p['to'] - p['from']
  if age > max_age:
    p['missing_reason'] = "is too old (%d years)" % age
    missing.append(p)
    continue

  if age == 0:
    p['missing_reason'] = "age is 0"
    missing.append(p)
    continue

  # Avoid dups
  # TODO: merge useful stuff from dups?
  if p['name'] in dups: continue
  dups[p['name']] = True

  p['link'] = "https://en.wikipedia.org/wiki/" + p['name'].replace(" ", "_")
  result.append(p)

sorted_result = sorted(result, key=itemgetter('rating'), reverse=True)

if args.limit is not None:
  sorted_result = sorted_result[:args.limit]

print json.dumps(sorted_result, indent=4, separators=(',', ': '))

sys.stderr.write("Written %d people, %d are missing\n" % (len(sorted_result), len(missing)))

if len(missing) > 0:
  sorted_missing = sorted(missing, key=itemgetter('rating'), reverse=True)

  sys.stderr.write("Top 20 people missing:\n")
  for nf in sorted_missing[:20]:
    sys.stderr.write("%s (rating %f), reason: %s\n" % (nf['name'], nf['rating'], nf['missing_reason']))


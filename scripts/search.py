#!/usr/bin/env python

import sys
import json
import argparse
from bisect import bisect_left

parser = argparse.ArgumentParser(description='Searches a person in a dataset, case insensitive.')
parser.add_argument('-n', '--name', help='search by person name')
args = parser.parse_args()

data = json.load(sys.stdin)
keys = [item['name'].lower() for item in data]

k = args.name.lower()
i = bisect_left(keys, k)
if i < len(data) and data[i]['name'].lower() == k:
  print json.dumps(data[i], indent=4, separators=(',', ': '))
else:
  print "{}"
  sys.exit(1)


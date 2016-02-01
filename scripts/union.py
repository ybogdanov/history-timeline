#!/usr/bin/python

import sys
import json
from bisect import bisect_left

result = []
keys = []

# Parse initial result if stdin given
if not sys.stdin.isatty():
  result = json.load(sys.stdin)
  keys = [item['name'] for item in result]

def insert(seq, keys, item):
  k = item['name']
  i = bisect_left(keys, k)
  if i < len(seq) and seq[i]['name'] == k:
    seq[i] = merge(seq[i], item)
  else:
    keys.insert(i, k)
    seq.insert(i, item)

def merge(a, b):
  r = a.copy()
  for k in ['from', 'to', 'rating', 'type', 'country']:
    if is_present(k, b): r[k] = b[k]
  return r

def is_present(key, dic):
  return key in dic and dic[key] != "" and dic[key] != None

for i in xrange(1, len(sys.argv)):
  with open(sys.argv[i]) as fp:
    for (k, item) in enumerate(json.load(fp)):
      if k % 1000 == 0:
        sys.stderr.write("%d\n" % (k))
      insert(result, keys, item)

print json.dumps(result, indent=4, separators=(',', ': '))


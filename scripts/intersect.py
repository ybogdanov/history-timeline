#!/usr/bin/python

import sys
import json
from bisect import bisect_left
from operator import itemgetter

result = []
wiki = []
keys = []
not_found = []

def insert(seq, result, keys, item):
  global not_found
  k = item['name']
  i = bisect_left(keys, k)
  if i < len(seq) and seq[i]['name'] == k:
    result.append(merge(seq[i], item))
  else:
    not_found.append(item)

def merge(a, b):
  r = a.copy()
  for k in ['from', 'to', 'rating', 'type', 'country']:
    if is_present(k, b): r[k] = b[k]
  return r

def is_present(key, dic):
  return key in dic and dic[key] != "" and dic[key] != None

with open(sys.argv[1]) as fd:
  wiki = json.load(fd)
  keys = [item['name'] for item in wiki]

for item in json.load(sys.stdin):
  insert(wiki, result, keys, item)

sorted_result = sorted(result, key=itemgetter('name'))
print json.dumps(sorted_result, indent=4, separators=(',', ': '))

sys.stderr.write('Written %d people, %d not found\n' % (len(result), len(not_found)))

sorted_not_found = sorted(not_found, key=itemgetter('rating'), reverse=True)

sys.stderr.write("Top 20 people not found:\n")
for nf in sorted_not_found[:20]:
  sys.stderr.write("%s (rating %f)\n" % (nf['name'], nf['rating']))


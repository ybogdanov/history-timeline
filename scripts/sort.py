#!/usr/bin/python

import sys
import json
import re
from operator import itemgetter

comment_line = re.compile(r"^\s*(?:#.*)?$")

re_line = re.compile(
  r'''
    ^\s*
    (?P<name>[^:]+)        # Person name
    (?:
      \s*:\s*
      (?P<properties>.+)?  # Properties
    )?
  ''',
  re.VERBOSE
  )

regex = re.compile(
  r'''
      (?P<key>\w+) \s* = \s*      # Key consists of only alphanumerics
      (?P<quote>["']?)            # Optional quote character.
      (?P<value>.*?)              # Value is a non greedy match
      (?P=quote)                  # Closing quote equals the first.
      ($|\s+)                     # Entry ends with comma or end of string
  ''',
  re.VERBOSE
  )

input_data = []

for i, line in enumerate(sys.stdin):
  if comment_line.match(line): continue

  m = re_line.match(line)

  if not m:
    sys.stderr.write("Cannot parse line #%d: %s" % (i+1, line))
    continue

  person = {
    "name": m.group("name").strip()
  }

  if m.group("properties"):
    props = {match.group('key'): match.group('value') for match in regex.finditer(m.group("properties"))}

    if "from" in props: props["from"] = int(props["from"])
    if "to" in props: props["to"] = int(props["to"])
    if "rating" in props: props["rating"] = float(props["rating"])

    person.update(props)
  
  input_data.append(person)

sorted_result = sorted(input_data, key=itemgetter('name'))

print json.dumps(sorted_result, indent=4, separators=(',', ': '))


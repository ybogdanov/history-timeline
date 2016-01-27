#!/usr/bin/python

import sys
import json
from operator import itemgetter

input_data = json.load(sys.stdin)
sorted_result = sorted(input_data, key=itemgetter('name'))

print json.dumps(sorted_result, indent=4, separators=(',', ': '))


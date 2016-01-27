
# .PHONY: public/data/data_1000.js

data/redirects_wiki.json:
	bzip2 -dk data/redirects_wiki.json.bz2

data/wiki.json:
	bzip2 -dk data/wiki.json.bz2

data/sources/pantheon.json:
	bzip2 -dk data/sources/pantheon.json.bz2

data/intermediate/pantheon.json: scripts/import-pantheon.py data/sources/pantheon.json data/redirects_wiki.json data/redirects_manual.json
	cat data/sources/pantheon.json | scripts/import-pantheon.py data/redirects_wiki.json data/redirects_manual.json > data/intermediate/pantheon.json

data/intermediate/manual.json: scripts/sort.py data/sources/manual.json
	cat data/sources/manual.json | scripts/sort.py > data/intermediate/manual.json

data/intermediate/merged.json: scripts/union.py data/intermediate/pantheon.json data/intermediate/manual.json
	cat data/intermediate/pantheon.json | scripts/union.py data/intermediate/manual.json > data/intermediate/merged.json

data/intermediate/mapped.json: scripts/intersect.py data/intermediate/merged.json data/wiki.json
	cat data/intermediate/merged.json | scripts/intersect.py data/wiki.json > data/intermediate/mapped.json

public/data/data_1000.js: scripts/final.py data/intermediate/mapped.json
	cat data/intermediate/mapped.json | scripts/final.py --limit 1000 | scripts/wrap_jsonp.py > public/data/data_1000.js

public/data/data_5000.js: scripts/final.py data/intermediate/mapped.json
	cat data/intermediate/mapped.json | scripts/final.py --limit 5000 | scripts/wrap_jsonp.py > public/data/data_5000.js

public/data/data_10000.js: scripts/final.py data/intermediate/mapped.json
	cat data/intermediate/mapped.json | scripts/final.py --limit 10000 | scripts/wrap_jsonp.py > public/data/data_10000.js

data: public/data/data_1000.js public/data/data_5000.js public/data/data_10000.js

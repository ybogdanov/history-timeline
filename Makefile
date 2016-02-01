all:
	@echo Make what?

data/redirects_wiki.json:
	bzip2 -dk data/redirects_wiki.json.bz2

data/wiki.json:
	bzip2 -dk data/wiki.json.bz2

data/dbpedia_dates.json:
	bzip2 -dk data/dbpedia_dates.json.bz2

data/wiki_dbpedia_dates.json: scripts/union.py data/wiki.json data/dbpedia_dates.json
	cat data/dbpedia_dates.json | scripts/union.py data/wiki.json > data/wiki_dbpedia_dates.json

data/sources/pantheon.json:
	bzip2 -dk data/sources/pantheon.json.bz2

data/intermediate/pantheon.json: scripts/import_pantheon.py data/sources/pantheon.json data/redirects_wiki.json data/redirects_manual.json
	cat data/sources/pantheon.json | scripts/import_pantheon.py data/redirects_wiki.json data/redirects_manual.json > data/intermediate/pantheon.json

data/intermediate/manual.json: scripts/txt_to_json.py data/sources/manual.txt
	cat data/sources/manual.txt | scripts/txt_to_json.py > data/intermediate/manual.json

data/intermediate/merged.json: scripts/union.py data/intermediate/pantheon.json data/intermediate/manual.json
	cat data/intermediate/pantheon.json | scripts/union.py data/intermediate/manual.json > data/intermediate/merged.json

data/intermediate/mapped.json: scripts/intersect.py data/intermediate/merged.json data/wiki_dbpedia_dates.json
	cat data/intermediate/merged.json | scripts/intersect.py data/wiki_dbpedia_dates.json > data/intermediate/mapped.json

public/data/data_1000.js: scripts/final.py data/intermediate/mapped.json
	cat data/intermediate/mapped.json | scripts/final.py --limit 1000 | scripts/wrap_jsonp.py > public/data/data_1000.js

public/data/data_5000.js: scripts/final.py data/intermediate/mapped.json
	cat data/intermediate/mapped.json | scripts/final.py --limit 5000 | scripts/wrap_jsonp.py > public/data/data_5000.js

public/data/data_10000.js: scripts/final.py data/intermediate/mapped.json
	cat data/intermediate/mapped.json | scripts/final.py --limit 10000 | scripts/wrap_jsonp.py > public/data/data_10000.js

data: public/data/data_1000.js public/data/data_5000.js public/data/data_10000.js

clean:
	rm data/intermediate/*.json public/data/data*.js data/redirects_wiki.json data/wiki.json data/sources/pantheon.json

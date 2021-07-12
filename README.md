# Birdmap - ebird visualizer/searcher

This is a utility to search local birds / search by species / search by recent sightings / search rare birds using the ebird api.

## Requirements to run:
 - Python 3.* / flask
 - Register for an ebird API key: https://ebird.org/api/keygen
 - Create file /ebird-api/config.py:
	 `ebird_api_key = '{{api_key}}'` 
 - from /ebird-api/ `flask-run`
 - open /ebird-api-js/speciesSearch.html and search

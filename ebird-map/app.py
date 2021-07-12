from flask import Flask,jsonify, request
from flask_cors import CORS, cross_origin

import folium
import requests
import requests_cache
from ebirdapi import localSpecies

app=Flask(__name__)
CORS(app)

requests_cache.install_cache('ebird_cache', backend='sqlite', expire_after=1800)


@app.route("/")
def index():
    return render_template('base.html')

@app.route("/sightings/<string:mode>/")
def show_species(mode):
    print('mode: ' + mode) 
    species_code = request.args.get('species', None)
    lat = request.args.get('lat', None)
    lng = request.args.get('lng', None)

    renderHtml = localSpecies(mode, species_code, lat, lng, 25)

    response = jsonify(renderHtml)
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #return jsonify(renderHtml)
    return response


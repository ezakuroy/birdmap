var map;
var mapMarkers = [];

window.onload=function() {
	const lat = 40.72;
	const lng = -74.04;

	map = L.map('speciesMap').setView([lat, lng], 10);

	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
 		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1,
		accessToken: 'pk.eyJ1IjoiZXpha3Vyb3kiLCJhIjoiY2txeW5sbjRuMGpsNjJ2bzdzenFwOGJmayJ9.jVWXThSXgeOZ03WZrtoPdg'

	}).addTo(map);

	this.circle = L.circle([lat, lng], {
		  radius: 25000,
		  color: '#3a542d',
		  fillColor: '#71eb34',
		  fillOpacity: 0.2,
		  opacity: 0.8,
		  title: "test"   
	}).addTo(this.map);

	// Set circle always centered when map is moved.
	this.map.on("moveend", (s) => {
	   this.circle.setLatLng(this.map.getCenter());
	   });
	
	   // todo: Set circle always centered when map is zoom in/out
	   this.map.on("zoomend", (s) => {
	     this.circle.setLatLng(this.map.getCenter());
	   });

};

function submitSearch() {

	fetchData();

	/*
	fetchData().then((data) => {
		parseData(data)
	})
	.catch(error => {
		console.log(error);
	});
	*/
}

async function fetchData() {
	var speciesCode = document.getElementById("speciesCode").value;
	console.log(speciesCode);

	var mode = document.getElementById("mode").value;
	var currentLocation = map.getBounds().getCenter();

	var url = 'http://127.0.0.1:5000/sightings/';
	if(mode === 'species') {
		url += 'species?species=' + speciesCode + '&lat=';
	}
	else if (mode === 'notable') {
		url += 'notable?lat=';
	}
	else {
		url += 'recent?lat=';
	}

	
	url+= currentLocation.lat + '&lng=' + currentLocation.lng;

	const response = await fetch(url);
	const species = await response.json();
	await parseData(species);

	return species;
}

function parseData(data) {
	console.log(data);
	
	var mode = document.getElementById("mode").value;

	for(var i = 0; i < this.mapMarkers.length; i++) {
		this.map.removeLayer(this.mapMarkers[i]);
	}

	const uniqueSpecies = new Map();
	data.forEach(function(sighting) {
		var marker = L.marker([sighting.lat, sighting.lng]).addTo(map);	
		var popupText = '';	
		if(sighting.comName !== null) {
			popupText += "<span class='speciesName'><a href='https://ebird.org/species/" + sighting.speciesCode + "' target='_blank'>" + sighting.comName + "</a></span></br>";
		}
		if(sighting.locName != null) {
			popupText += "<span class='locationName'>" + sighting.locName + "</span>";
		}
		if(sighting.obsDt != null) {
			popupText += "</br><span class='dateSighted'>" + sighting.obsDt + "</span>";
		}

		if(sighting.subId != null) {
			popupText += "</br><a href='https://ebird.org/checklist/" + sighting.subId + "' target='_blank'>Checklist</a>";
		}

		uniqueSpecies.set(sighting.speciesCode, sighting.comName)

		marker.bindPopup(popupText);

		this.mapMarkers.push(marker);	
	});
	
	document.getElementById("gallery").innerHTML = "";
	var gallery = document.getElementById("gallery");
	for (let[key, value] of uniqueSpecies) {
		var newDiv = document.createElement("div");
		newDiv.className = 'col-md-4 gx-0';
		newDiv.innerHTML = '<img src="./static/images/image-' + key + '.png"/><div>' + value + '</div>';

		gallery.appendChild(newDiv);
	}
}


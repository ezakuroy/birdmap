function submitSearch() {
	var speciesCode = document.getElementById("speciesCode").value;
	document.getElementById("map").src="/species/" + speciesCode;
}

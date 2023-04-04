
// get the current weather info
function getWeather() {
    // fetch the weather info
    fetch("http://127.0.0.1:5000/weather")
        .then((response) => response.json())  //parsing the response body text as JSON
        .then((data) => {
            console.log("fetch response:", typeof data)
            addWeather(data);
        });
}
function addWeather(weatherJson) {
    var weatherStr = "Current Weather"
    parsedObjWeather = JSON.parse(weatherJson);
    var weather_main = parsedObjWeather.weather_main
    var temp = parsedObjWeather.temp
    var temp_feel = parsedObjWeather.temp_feel
    var wind_speed = parsedObjWeather.wind_speed
    weatherData = "weather: " + weather_main + "tempurature°: " + temp + "°" + "     RealFeel°:" + temp_feel+ "     wind speed:" + wind_speed
    weatherStr = weatherStr + weatherData
    document.getElementById("weather").innerHTML = weatherStr;
}









// Callback init function
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        // The maps default view (Dublin)
        center: { lat: 53.3515, lng: -6.27527},
        zoom: 14,
        mapId: "DBH_maps"
    });
    //test marker
    // new google.maps.marker.AdvancedMarkerView({
    //     map,
    //     position: { lat: 53.3515, lng: -6.25527 },
    //     title: "Test Marker",
    // });
    // invoke
    getStationsList(map);
}
window.initMap = initMap;


// get the static station list
function getStationsList(map) {
    // fetch the Json file which contains the coordinates of each station
    fetch("http://127.0.0.1:5000/stations")
        .then((response) => response.json())  //parsing the response body text as JSON
        .then((data) => {
            console.log("fetch response:", typeof data)
            addMarkers(data, map);
        });
}

function addMarkers(stationsJson, map) {
    // Create an info window to share between markers.
    const infoWindow = new google.maps.InfoWindow();
    // Traverse the json file to access each bike station
    var i = 0;
    stationsJson.forEach(station => {
        // need to pass the map obj as the parameter so that this function can use map to construct the maker
        if ( map instanceof google.maps.Map) {
            i = i+1;
            const pinView = new google.maps.marker.PinView({
                glyph: `${i + 1}`,
            });
            // Add a new marker
            const marker = new google.maps.marker.AdvancedMarkerView({
                position: {
                    lat: station.location_lat,
                    lng: station.location_lon,
                },
                map,
                title: station.name,
                content: pinView.element,
                // station_number: station.indexNumber,
            });
            // Add a click listener for each marker, and set up the info window.
            marker.addListener("click", ({ domEvent, latLng }) => {
                const { target } = domEvent;
                infoWindow.close();
                var Content = getAvailableInfo(station.indexNumber)
                infoWindow.setContent(marker.title + "\n" + Content);
                infoWindow.open(marker.map, marker);
            });
        }
    });
}


// get the available stations and bikes. (Input station index number)
function getAvailableInfo(indexnumber) {
    // fetch the Json file which contains the coordinates of each station
    fetch(`http://127.0.0.1:5000/availableInfo/${indexnumber}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));

    // return the available bike station info from the reponse file
    return "xxx"
}

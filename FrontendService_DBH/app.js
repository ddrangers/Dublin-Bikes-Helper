

// Callback init function
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        // The maps default view (Dublin)
        center: { lat: 53.3515, lng: -6.27527},
        zoom: 14,
    });
    // test maker
    // const myLatLng = { lat: 53.3515, lng: -6.25527 };
    // new google.maps.Marker({
    //     position: myLatLng,
    //     map,
    //     title: "Test: Hello World!",
    // });

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
    stationsJson.forEach(station => {
        // need to pass the map obj as the parameter so that this function can use map to construct the maker
        if ( map instanceof google.maps.Map) {
            new google.maps.Marker({
                position: {
                    lat: station.location_lat,
                    lng: station.location_lon,
                },
                map: map,
                title: station.name,
                station_number: station.indexNumber,
            });
        }
    });
}
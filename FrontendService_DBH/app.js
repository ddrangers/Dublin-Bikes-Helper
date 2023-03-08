

function addMarkers(stationsJson) {
    stationsJson.forEach(station => {
        new google.maps.Marker({
            position: {
                lat: station.position_lat,
                lng: station.position_lng,
            },
            map: map,
            title: station.name,
            station_number: station.number,
        });
    });
}

// get the static station list
function getStationsList() {
    // fetch the Json file which contains the coordinates of each station
    fetch("/stations")
        .then((response) => response.json())  //parsing the response body text as JSON
        .then((data) => {
            console.log("fetch response:", typeof data)
            addMarkers(data);
        });
}

// Callback init function
function initMap() {
    const myLatLng = { lat: 53.3515, lng: -6.25527 };
    const map = new google.maps.Map(document.getElementById("map"), {
        // The maps default view (Dublin)
        center: { lat: 53.3515, lng: -6.25527},
        zoom: 12,
    });

    new google.maps.Marker({
        position: myLatLng,
        map,
        title: "Test: Hello World!",
    });

    getStationsList();
}

window.initMap = initMap;



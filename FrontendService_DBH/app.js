// 定义全局变量parsedObjInfo以便在多个函数中使用
var parsedObjInfo;
// 定义当前bike station id
var current_bike_station_id;
// 定义找回来的station data
var stationData;
// 定义全局map方便多个函数进行饮用
let markers = [];


// get the current weather info
function getWeather() {
    // fetch the weather info
    fetch("http://3.88.162.45/weather")
        .then((response) => response.json())  //parsing the response body text as JSON
        .then((data) => {
            console.log("fetch current weather info response:", typeof data)
            console.log(data)
            addWeather(data);
        });
}

function addWeather(weatherJson) {
    var weatherStr = "<br>Current Weather<br>"
    var weather_main = weatherJson.weather_main
    var temp = weatherJson.temp
    var temp_feel = weatherJson.temp_feel
    var wind_speed = weatherJson.wind_speed
    weatherData = "Weather: " + weather_main + " &nbsp;&nbsp;&nbsp;&nbsp;Temperature: " + temp + "°C" + "&nbsp;&nbsp;&nbsp;&nbsp;Feels Like: " + temp_feel+ "°C"+ "&nbsp;&nbsp;&nbsp;&nbsp;Wind Speed: " + wind_speed + "m/s"
    weatherStr = weatherStr + weatherData
    document.getElementById("weather").innerHTML = weatherStr;
}


// Callback init function
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        // The maps default view (Dublin)
        center: { lat: 53.3515, lng: -6.27527},
        zoom: 14,
        mapId: "DBH_maps",
    });
    // invoke the default function
    getStationsList(map);
    getWeather();
}
window.initMap = initMap;


// get the static station list
function getStationsList(map) {
    // fetch the Json file which contains the coordinates of each station
    fetch("http://3.88.162.45/stations")
        .then((response) => response.json())  //parsing the response body text as JSON
        .then((data) => {
            console.log("fetch static station list response:", typeof data)
            console.log(data)
            stationData = data;
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
                background: "#FFBF00",
                // 00FFFF green
                // FFBF00 yellow
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
            });
            markers.push(marker);

            // Add a click listener for each marker, and set up the info window.
            marker.addListener("click", ({ domEvent, latLng }) => {
                const { target } = domEvent;
                infoWindow.close();
                current_bike_station_id = station.indexNumber;
                console.log("The current selected marker is:", current_bike_station_id);
                // detail info
                infoWindow.setContent(marker.title);
                // invoke function
                console.log("invoke markers listener function");
                setAiandDetail(current_bike_station_id)
                infoWindow.open(marker.map, marker);
            });
        }
    });
}

function setAiandDetail(indexnumber) {
    console.log("invoke set Ai and Detail");
    setBarInfo(indexnumber);
    setAiPlot(indexnumber);
}

// set the available stations and bikes on the left bar.
function setBarInfo(stationId) {
    console.log("invoke setBarInfo");
    // fetch the Json file which contains the coordinates of each station
    fetch(`http://3.88.162.45/stations/${stationId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then((data) => {
            console.log("Fetch get station detail availableInfo response:", typeof data, data);
            var displayString = "<p style=\"margin: 8px;color: grey;display: inline;\">Station ID:</p>"+ data.index + "<br>";
            displayString = displayString +  "<p style=\"margin: 8px;color: grey;display: inline;\">Station Name:</p>"+ data.name+ "<br>";
            displayString = displayString +  "<p style=\"margin: 8px;color: grey;display: inline;\">Address:</p>"+ data.address+ "<br>";
            displayString = displayString +  "<p style=\"margin: 8px;color: grey;display: inline;\">Status (Open/Closed):</p>"+ data.status+ "<br>";
            displayString = displayString +  "<p style=\"margin: 8px;color: grey;display: inline;\">Total Bike Stands:</p>"+ data.bike_stand+ "<br>";
            displayString = displayString +  " <p style=\"margin: 8px; color: grey;color:green;display: inline;\">-----------------------------------------------------------</p>\n"+ "<br>";
            displayString = displayString +  "<p style=\"margin: 8px; color: grey;color:green;display: inline;\">Current Bike Availability:</p>"+ data.bike_available+ "<br>";
            displayString = displayString +  "<p style=\"margin: 8px; color: grey;color:green;display: inline;\">Current Parking Availability:</p>"+ data.bike_stand_available+ "<br>";
            document.getElementById("barDetail").innerHTML = displayString;
            console.log("barDetail displayString:" ,displayString);
        })
        .catch(error => console.error(error));
}

// set the AI predictions on the left bar.
function setAiPlot(current_bike_station_id) {
    console.log("invoke setAiPlot");
    // fetch the Json file which contains the coordinates of each station
    fetch(`http://3.88.162.45/stationsPredict/${current_bike_station_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then((data) => {
            console.log("Fetch get AI plot data response:", typeof data, data);
            // bike: determine whether the backend is returning null value
            if (data.bike_predictions[0] == "C")
            {
                // display the missing AI message
                const p = document.getElementById('bikePlotMissingNotice');
                p.textContent = 'Sorry, the AI bike predictions is currently unavailable.';
                // delete the under lying graph
                const div = document.getElementById('ChartBike');
                div.innerHTML = '';
                // print message
                console.log("bike predictions is null");
            } else {
                console.log("bike predictions is available");
                const p = document.getElementById('bikePlotMissingNotice');
                p.textContent = '';
                drawChart1(data);
            }
            // station: determine whether the backend is returning null value
            if (data.park_predictions[0] == "C")
            {
                // display the missing AI message
                const p = document.getElementById('parkPlotMissingNotice');
                p.textContent = 'Sorry, the AI park predictions is currently unavailable.';
                // delete the under lying graph
                const div = document.getElementById('ChartStation');
                console.log("station predictions is null");
            } else {
                console.log("station predictions is available");
                const p = document.getElementById('parkPlotMissingNotice');
                p.textContent = '';
                drawChart2(data);
            }
        })
        .catch(error => console.error(error));

    // delete the default bike img
    const img = document.querySelector('img[src="db2.png"]');
    img.style.display = 'none';

    // delete the default suggestion
    const p = document.getElementById('suggestionAI');
    p.style.display = 'none';
}

// bike chart
function drawChart1(data) {
    var data1 = google.visualization.arrayToDataTable([
        ["Hours", "Available Bikes", { role: "style" } ],
        ["1", data.bike_predictions[0], "gold"],
        ["2", data.bike_predictions[1], "silver"],
        ["3", data.bike_predictions[2], "yellow"],
        ["4", data.bike_predictions[3], "pink"],
        ["5", data.bike_predictions[4], "maroon"],
        ["6", data.bike_predictions[5], "orange"],
        ["7", data.bike_predictions[6], "gold"],
        ["8", data.bike_predictions[7], "silver"],
        ["9", data.bike_predictions[8], "yellow"],
        ["10", data.bike_predictions[9], "pink"],
        ["11", data.bike_predictions[10], "maroon"],
        ["12", data.bike_predictions[11], "orange"],
        ["13", data.bike_predictions[12], "gold"],
        ["14", data.bike_predictions[13], "silver"],
        ["15", data.bike_predictions[14], "yellow"],
        ["16", data.bike_predictions[15], "pink"],
        ["17", data.bike_predictions[16], "maroon"],
        ["18", data.bike_predictions[17], "orange"],
        ["19", data.bike_predictions[18], "gold"],
        ["20", data.bike_predictions[19], "silver"],
        ["21", data.bike_predictions[20], "yellow"],
        ["22", data.bike_predictions[21], "pink"],
        ["23", data.bike_predictions[22], "maroon"],
        ["24", data.bike_predictions[23], "orange"],
    ]);

    var view = new google.visualization.DataView(data1);
    view.setColumns([0, 1, 2]);

    var options = {
        title: "Todays Bike Availability",
        width: 433,
        height: 285,
        bar: {groupWidth: "95%"},
        legend: { position: "none" },
        colors: ['#7FFFD4']
    };
    var chart = new google.visualization.ColumnChart(document.getElementById("ChartBike"));
    chart.draw(view, options);
}

// station chart
function drawChart2(data) {

    var data2 = google.visualization.arrayToDataTable([
        ["Hours", "Available Parking", { role: "style" } ],

        ["1", data.park_predictions[0], "gold"],
        ["2", data.park_predictions[1], "silver"],
        ["3", data.park_predictions[2], "yellow"],
        ["4", data.park_predictions[3], "pink"],
        ["5", data.park_predictions[4], "maroon"],
        ["6", data.park_predictions[5], "orange"],
        ["7", data.park_predictions[6], "gold"],
        ["8", data.park_predictions[7], "silver"],
        ["9", data.park_predictions[8], "yellow"],
        ["10", data.park_predictions[9], "pink"],
        ["11", data.park_predictions[10], "maroon"],
        ["12", data.park_predictions[11], "orange"],
        ["13", data.park_predictions[12], "gold"],
        ["14", data.park_predictions[13], "silver"],
        ["15", data.park_predictions[14], "yellow"],
        ["16", data.park_predictions[15], "pink"],
        ["17", data.park_predictions[16], "maroon"],
        ["18", data.park_predictions[17], "orange"],
        ["19", data.park_predictions[18], "gold"],
        ["20", data.park_predictions[19], "silver"],
        ["21", data.park_predictions[20], "yellow"],
        ["22", data.park_predictions[21], "pink"],
        ["23", data.park_predictions[22], "maroon"],
        ["24", data.park_predictions[23], "orange"],
    ]);

    var view = new google.visualization.DataView(data2);
    view.setColumns([0, 1, 2]);

    var options = {
        title: "Todays Parking Availability",
        width: 433,
        height: 285,
        bar: {groupWidth: "95%"},
        legend: { position: "none" },

    };
    var chart = new google.visualization.ColumnChart(document.getElementById("ChartStation"));
    chart.draw(view, options);
}


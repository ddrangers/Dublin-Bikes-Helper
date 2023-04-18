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
    fetch("http://127.0.0.1:5000/weather")
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
    weatherData = "weather: " + weather_main + " &nbsp;&nbsp;&nbsp;&nbsp;tempurature°: " + temp + "°" + "&nbsp;&nbsp;&nbsp;&nbsp;RealFeel°:" + temp_feel+ "&nbsp;&nbsp;&nbsp;&nbsp;wind speed:" + wind_speed
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
    fetch("http://127.0.0.1:5000/stations")
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
                glyph: `${i + 1}`,
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
                var Content = getAvailableInfo(station.indexNumber);  //Content is a parsed JSON obj
                setAiPlot(station.indexNumber); // set the AIplot
                infoWindow.setContent(marker.title + "<br>" + "Address:" + Content.address);
                setBarInfo(Content);
                // setAiPlot(station.indexNumber);
                current_bike_station_id = station.indexNumber;
                console.log("The current selected marker is:", current_bike_station_id);
                infoWindow.open(marker.map, marker);
            });
        }
    });
    //test marker
    // const marker = new google.maps.marker.AdvancedMarkerView({
    //     map,
    //     position: { lat: 53.3515, lng: -6.25527 },
    //     title: "Test Marker",
    // });
    // markers.push(marker);

}


// get the available stations and bikes. (Input station index number)
function getAvailableInfo(indexnumber) {
    // fetch the Json file which contains the coordinates of each station
    fetch(`http://127.0.0.1:5000/stations/${indexnumber}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then((data) => {
            console.log("Fetch get station detail availableInfo response:", typeof data, data);
            // return the available bike station info from the reponse file
            parsedObjInfo = data;
        })
        .catch(error => console.error(error));

    return parsedObjInfo;
}


// set the available stations and bikes on the left bar.
function setBarInfo(content) {
    console.log("invoke setBarInfo");
    var displayString = "Bike station No.&nbsp;"+ content.index;
    displayString = displayString +  "<br>Station name:&nbsp;"+ content.name;
    displayString = displayString +  "<br>Station status:&nbsp;"+ content.status;
    displayString = displayString +  "<br>Address:&nbsp;"+ content.address;
    displayString = displayString +  "<br>Current bike available:&nbsp;"+ content.bike_available;
    displayString = displayString +  "<br>Current stand available:&nbsp;"+ content.bike_stand_available;
    displayString = displayString +  "<br>Total bike stand:&nbsp;"+ content.bike_stand;
    document.getElementById("barDetail").innerHTML = displayString;
    console.log("displayString:" ,displayString);
}

// set the AI predictions on the left bar.
function setAiPlot(current_bike_station_id) {
    // use the select option as the parameter
    // var showWeekdays = document.getElementById("weekdays");
    // var weekdays = showWeekdays.value;
    // fetch the Json file which contains the coordinates of each station
    fetch(`http://127.0.0.1:5000/stationsPredict/${current_bike_station_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then((data) => {
            console.log("Fetch get AI plot data response:", typeof data, data);
            // return the available plot info
            drawChart1(data);
            drawChart2(data);
        })
        .catch(error => console.error(error));
    // Use drawChart1 and drawChart2 function to generate the prediction plot
    
}


function drawChart1(data) {
    var data1 = google.visualization.arrayToDataTable([
        ["Hours", "Availiable bike num", { role: "style" } ],

        ["1", 11.94, "gold"],
        ["2", 10.49, "gold"],
        ["3", 19.30, "gold"],
        ["4", 21.45, "gold"],
        ["5", 21.85, "gold"],
        ["6", 21.45, "gold"],
        ["7", 20.45, "gold"],
        ["8", 21.85, "gold"],
        ["9", 21.45, "gold"],
        ["10", 21.45, "gold"],
        ["11", 13.45, "gold"],
        ["12", 13.45, "gold"],
        ["13", 2.45, "gold"],
        ["14", 2.45, "gold"],
        ["15", 2.45, "gold"],
        ["16", 3.45, "gold"],
        ["17", 3.45, "gold"],
        ["18", 4.45, "gold"],
        ["19", 7.45, "gold"],
        ["20", 8.45, "gold"],
        ["21", 12.45, "gold"],
        ["22", 12.45, "gold"],
        ["23", 11.45, "gold"],
        ["24", 11.45, "gold"],
    ]);

    var view = new google.visualization.DataView(data1);
    view.setColumns([0, 1,
        { calc: "stringify",
            sourceColumn: 1,
            type: "string",
            role: "annotation" },
        2]);

    var options = {
        title: "Bike availability (next 24 hours)",
        width: 383,
        height: 285,
        bar: {groupWidth: "95%"},
        legend: { position: "none" },
        colors: ['#7FFFD4']
    };
    var chart = new google.visualization.ColumnChart(document.getElementById("ChartBike"));
    chart.draw(view, options);
}

function drawChart2(data) {
    var data2 = google.visualization.arrayToDataTable([
        ["Hours", "Availiable bike num", { role: "style" } ],

        ["1", 11.94, "gold"],
        ["2", 10.49, "gold"],
        ["3", 19.30, "gold"],
        ["4", 21.45, "gold"],
        ["5", 21.85, "gold"],
        ["6", 21.45, "gold"],
        ["7", 20.45, "gold"],
        ["8", 21.85, "gold"],
        ["9", 21.45, "gold"],
        ["10", 21.45, "gold"],
        ["11", 13.45, "gold"],
        ["12", 13.45, "gold"],
        ["13", 2.45, "gold"],
        ["14", 2.45, "gold"],
        ["15", 2.45, "gold"],
        ["16", 3.45, "gold"],
        ["17", 3.45, "gold"],
        ["18", 4.45, "gold"],
        ["19", 7.45, "gold"],
        ["20", 8.45, "gold"],
        ["21", 12.45, "gold"],
        ["22", 12.45, "gold"],
        ["23", 11.45, "gold"],
        ["24", 11.45, "gold"],
    ]);

    var view = new google.visualization.DataView(data2);
    view.setColumns([0, 1,
        { calc: "stringify",
            sourceColumn: 1,
            type: "string",
            role: "annotation" },
        2]);

    var options = {
        title: "Station availability (next 24 hours)",
        width: 383,
        height: 285,
        bar: {groupWidth: "95%"},
        legend: { position: "none" },
    };
    var chart = new google.visualization.ColumnChart(document.getElementById("ChartStation"));
    chart.draw(view, options);
}


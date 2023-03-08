//
// let map;
//
// function initMap() {
//     map = new google.maps.Map(document.getElementById("map"), {
//         center: { lat: 53.3515, lng: -6.25527 },
//         zoom: 12,
//     });
// }
//
// window.initMap = initMap;


function initMap() {
    const myLatLng = { lat: 53.3515, lng: -6.25527 };
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 53.3515, lng: -6.25527 },
        zoom: 12,
    });

    new google.maps.Marker({
        position: myLatLng,
        map,
        title: "Hello World!",
    });
}

window.initMap = initMap;
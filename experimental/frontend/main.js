var mapboxAccessToken = 'pk.eyJ1Ijoidm9kYSIsImEiOiJjanU0bXR6NXIwemxoNDRxdm9wMTc2YTd5In0.Z3LcZt3raPAfcQan-k59XQ';
var mymap = L.map('mapid', {
    minZoom: 3,
    maxZoom: 10,
}).setView([37.8, -96], 4);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 10,
    id: 'mapbox.light',
    accessToken: mapboxAccessToken,
}).addTo(mymap);
function style(feature) {
    return {
        fillColor: '#800026',
        weight: .3,
        opacity: .5,
        color: 'black',
        dashArray: '',
        fillOpacity: 0.7,
    };
}
var geoJson;
function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: "#666",
        dashArray: '',
        fillOpacity: 0.7,
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
    else {
        alert("Sorry! Your browser is not supported!");
    }
}
function resetHighlight(e) {
    geoJson.resetStyle(e.target)
}
function zoomToFeature(e) {
    mymap.fitBounds(e.target.getBounds());
    alert("Summary call would go here!");
}
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}
geoJson = L.geoJson(counties, {
    style: style,
    onEachFeature: onEachFeature,
}).addTo(mymap);

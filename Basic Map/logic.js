// Create a map object
var myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5
});

// Add a tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

// An array containing each city's name, location, and address
var cities = [{
  location: [30.2234, -977697],
  name: "(512) Brewing Company",
  address: "407 Radam, F200, Austin, Texas"
},
{
  location: [37.7825, -122.3930],
  name: "21st Amendment Brewery Cafe",
  address: "563 Second Street, San Francisco, California	94107"
},
{
  location: [41.2225, -77.0369],
  name: "Abbey Wright Brewing/Valley Inn",
  address: "204 Valley Street, Williamsport, Pennsylvania 17702"
},
{
  location: [30.5049, -89.9440],
  name: "Abita Brewing Company",
  address: "PO Box 1510, Abita Springs, Louisiana	70420"
},
{
  location: [41.2603	-96.0903],
  name: "Aksarben Brewing (BOP)",
  address: "11337 Davenport St., Omaha, Nebraska 68130"
}
];

// Loop through the cities array and create one marker for each city, bind a popup containing its name and population add it to the map
for (var i = 0; i < cities.length; i++) {
  var city = cities[i];
  L.marker(city.location)
    .bindPopup("<h1>" + city.name + "</h1> <hr> <h3>Address: " + city.address + "</h3>")
    .addTo(myMap);
}

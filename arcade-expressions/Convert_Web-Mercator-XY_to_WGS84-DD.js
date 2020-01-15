// For use as an Arcade Expression

// Converts Spherical Mercator XY point from EPSG:900913 to lat/lon in WGS84 Datum
// Here we are getting the centroid of our polygon feature
var cen = Centroid($feature);
var originShift = 2 * PI * 6378137 / 2;


var lon = (cen.x / originShift) * 180.0;
var lat = (cen.y / originShift) * 180.0;

var latdd = 180 / PI * (2 * atan( exp( lat * PI / 180.0)) - PI / 2.0);
return latdd + ", " + lon;

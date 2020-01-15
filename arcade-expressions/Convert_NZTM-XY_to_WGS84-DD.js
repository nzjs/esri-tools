// For use as an Arcade Expression

// Converts NZTM XY point from EPSG:2193 to lat/lon in WGS84 Datum
// Here we are getting the centroid of our polygon feature
var cen = Centroid($feature);

//Common variables for NZTM2000
var a       = 6378137;
var f       = 1 / 298.257222101;
var phizero  = 0;
var lambdazero  = 173;
var Nzero   = 10000000;
var Ezero   = 1600000;
var kzero   = 0.9996;            

//input Northing(Y); Easting(X) variables
var N       = cen.y;
var E       = cen.x;

//Calculation: From NZTM to lat/Long

var b = a * (1 - f);
var esq = 2 * f - Pow(f, 2);
var Z0 = 1 - esq / 4 - 3 * Pow(esq, 2) / 64 - 5 * Pow(esq, 3) / 256;
var A2 = 0.375 * (esq + Pow(esq, 2) / 4 + 15 * Pow(esq, 3) / 128);
var A4 = 15 * (Pow(esq, 2) + 3 * Pow(esq, 3) / 4) / 256;
var A6 = 35 * Pow(esq, 3) / 3072;

var Nprime = N - Nzero;
var mprime = Nprime / kzero;
var smn = (a - b) / (a + b);
var G = a * (1 - smn) * (1 - Pow(smn, 2)) * (1 + 9 * Pow(smn, 2) / 4 + 225 * Pow(smn, 4) / 64) * PI/ 180.0;
var sigma = mprime * PI / (180 * G);
var phiprime = sigma + (3 * smn / 2 - 27 * Pow(smn, 3) / 32) * Sin(2 * sigma) + (21 * Pow(smn, 2) / 16 - 55 * Pow(smn, 4) / 32) * Sin(4 * sigma) + (151 * Pow(smn, 3) / 96) * Sin(6 * sigma) + (1097 * Pow(smn, 4) / 512) *Sin(8 * sigma);
var rhoprime = a * (1 - esq) / Pow((1 - esq * Pow((Sin(phiprime)), 2)), 1.5);
var upsilonprime = a / Sqrt(1 - esq * Pow((Sin(phiprime)), 2));

var psiprime = upsilonprime / rhoprime;
var tprime = Tan(phiprime);
var Eprime = E - Ezero;
var chi = Eprime / (kzero * upsilonprime);
var term_1 = tprime * Eprime * chi / (kzero * rhoprime * 2);
var term_2 = term_1 * Pow(chi, 2) / 12 * (-4 * Pow(psiprime, 2) + 9 * psiprime * (1 - Pow(tprime, 2)) + 12 * Pow(tprime, 2));
var term_3 = tprime * Eprime * Pow(chi, 5) / (kzero * rhoprime * 720) * (8 * Pow(psiprime, 4) * (11 - 24 * Pow(tprime, 2)) - 12 * Pow(psiprime, 3) * (21 - 71 * Pow(tprime, 2)) + 15 * Pow(psiprime, 2) * (15 - 98 * Pow(tprime, 2) + 15 * Pow(tprime, 4)) + 180 * psiprime * (5 * Pow(tprime, 2) - 3 * Pow(tprime, 4)) + 360 * Pow(tprime, 4));
var term_4 = tprime * Eprime * Pow(chi ,7) / (kzero * rhoprime * 40320) * (1385 + 3633 * Pow(tprime, 2) + 4095 * Pow(tprime, 4) + 1575 * Pow(tprime, 6));
var term1 = chi * (1 / Cos(phiprime));
var term2 = Pow(chi, 3) * (1 / Cos(phiprime)) / 6 * (psiprime + 2 * Pow(tprime, 2));
var term3 = Pow(chi, 5) * (1 / Cos(phiprime)) / 120 * (-4 * Pow(psiprime, 3) * (1 - 6 * Pow(tprime, 2)) + Pow(psiprime, 2) * (9 - 68 * Pow(tprime, 2)) + 72 * psiprime * Pow(tprime, 2) + 24 * Pow(tprime, 4));
var term4 = Pow(chi, 7) * (1 / Cos(phiprime)) / 5040 * (61 + 662 * Pow(tprime, 2) + 1320 * Pow(tprime, 4) + 720 * Pow(tprime, 6));

var latitude = (phiprime - term_1 + term_2 - term_3 + term_4) * 180 / PI;
var longitude = lambdazero + 180 / PI * (term1 - term2 + term3 - term4);

return latitude + " " + longitude;

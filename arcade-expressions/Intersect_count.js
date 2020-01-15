// Calculate the count of survey123 submissions that spatially intersect the selected feature
var submission = FeatureSetByName($map,"<survey123 submission data>")
var countSubmissions = Count(Intersects(submission,$feature))

// Calculate the count of buildings that spatially intersect the selected feature
var houses = FeatureSetByName($map,"<building outline data>")
var countHouses = Count(Intersects(houses,$feature))

// Calculate percentage completion of survey123 submissions to building count
var percent = (countSubmissions / countHouses) * 100

return round(percent, 2)
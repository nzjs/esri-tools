// Return the sum of a specified field from a relationship class, based on the input PK
// Assumes a one-to-many relationship between the PK and FK.
var aN = $feature.AssessmentNumber;
var sql = "AssessmentNumber = @aN";
var relTable = FeatureSetByName($datastore, "levies");
var relRecords = Filter(relTable, sql);
var c = Count(relRecords);
var s = 0;

if (c > 0){
  for (var r in relRecords){
    s += r.LevyAmount;  
  }
}
return s;


// Return the highest number of a specified field from a relationship class, based on the input PK
// Assumes a one-to-many relationship between the PK and FK.
var aN = $feature.AssessmentNumber;
var sql = "AssessmentNumber = @aN";
var relTable = FeatureSetByName($datastore, "levies");
var relRecords = Filter(relTable, sql);
var c = Count(relRecords);
var mx = -Infinity;

if (c > 0){
  for (var r in relRecords){
    mx = IIF(r.LevyAmount > mx, r.LevyAmount, mx);
  }
}
return mx;


// Return the description field that relates to the highest number for a specified field from a relationship class
// Assumes a one-to-many relationship between the PK and FK.
// This one is probably not that efficient when running.
var aN = $feature.AssessmentNumber;
var sql = "AssessmentNumber = @aN";
var relTable = FeatureSetByName($datastore, "levies");
var relRecords = Filter(relTable, sql);
var c = Count(relRecords);
var mx = -Infinity;
var desc = "";

if (c > 0){
  for (var r in relRecords){
    mx = IIF(r.LevyAmount > mx, r.LevyAmount, mx);
  }
  for (var d in relRecords){
    if (d.LevyAmount == mx){
      desc = d.LevyDescription;
    }
  }
}
return desc;
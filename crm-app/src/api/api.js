// // API connection to Amazon RDS
import { dbCredentials } from "./dbCredentials.js";
import mysql from "mysql"

var con = mysql.createConnection({
  host: dbCredentials.host,
  user: dbCredentials.user,
  password: dbCredentials.password
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
  var sql = "USE " + dbCredentials.dbname
  con.query(sql, function (err) {
    if (err) throw err;
    console.log("Using " + dbCredentials.dbname);
  });
  getRepName(1);
});

export const getRepName = async (id) => {
  var sql = "SELECT * FROM Representative WHERE RepresentativeID = " +  id;
  con.query(sql, function (err, result) {
    if (err) throw err;
    var representative = result[0];
    var representativeName = representative.FirstName + " " + representative.LastName
    console.log(representativeName);
    return representativeName;
  });
}

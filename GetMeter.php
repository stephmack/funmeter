<?php

//include_once("JSON.php");
include("constants.php");

$con=mysqli_connect("localhost", "root", "raspberry", "Utils");
//db = MySQLdb.connect (host = "localhost", user = "root",passwd = "raspberry", db = "Utils")
// Check connection
if (mysqli_connect_errno())
{
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
} else 
{
    //echo "Got Here";
    $NUMBER = $_GET[NUMBER];
    $TYPE = $_GET[TYPE];
    $REQ = array("REQ" => $_GET[REQ]);
    if($TYPE == "1"){//Gets data based on start and stop time
         $START = $_GET[START];
         $STOP = $_GET[STOP];
    //$sql = "SELECT *FROM scm_hist WHERE ID IN ($NUMBER)";
         $sql = "SELECT MIN(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START) AND (DT < $STOP)))
         union all
         SELECT MAX(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START) AND (DT < $STOP)))";

    //echo $sql;
         $result = mysqli_query($con,$sql);
         $json = array();
         $meter = $_GET[METER];
         if(mysqli_num_rows($result)){
             while($row=mysqli_fetch_row($result)){
		//print_r($row);
                     $sql = "SELECT ind, DT,  Reading, M_Usage FROM scm_hist WHERE ind = $row[0]";
		     $result1 = mysqli_query($con,$sql);
    		     if(mysqli_num_rows($result1)){
		   	     while($row1=mysqli_fetch_assoc($result1)){
			 	     $json[]=$row1;
				//print_r($row1);
			     }
		     } 
             }
	     //$json = array_merge($REQ, $json);
         }
    }
    if($TYPE == "0"){ //Resets Databases
         $sql = "UPDATE ctrl SET reset_bit=1 WHERE ind=1";
         //mysqli_query($con,$sql);
         if (mysqli_query($con, $sql)) {
              echo "Record updated successfully";
         } else {
              echo "Error updating record: " . mysqli_error($con);
         }
    }
    if($TYPE == "2"){ //Reads Meter IDs
        $sql = "SELECT * FROM utils_list"; 
        $result1 = mysqli_query($con,$sql);
        if(mysqli_num_rows($result1)){
             while($row1=mysqli_fetch_assoc($result1)){
                  $json[]=$row1;
             }
        }

    }    

    if($TYPE == "3"){ //ADD/Change Meter information
        $meter = $_GET[NUMBER];
        $sql = "SELECT * FROM utils_list WHERE ID=$meter";
        $result1 = mysqli_query($con,$sql);
        if(mysqli_num_rows($result1)){
             while($row1=mysqli_fetch_row($result1)){
                  $json[]=$row1;
             }
        }
	/*if($json) {
            echo "has data";
        } else {
	    echo "No data";
        }*/    
        if (!($json)){
             $UT = $_GET[UT];
             $LABEL = $_GET[LABEL];
	     $timezone = $_GET[timezone];
	     $price = $_GET[price];
	     $STid = $_GET[STid];
             //echo $UT;
             //echo $LABEL;
             //$sql = "INSERT INTO utils_list (UT, MyLabel, ID) VALUES ($UT,$LABEL,$meter)";
             $sql = "INSERT INTO utils_list (UT, MyLabel, ID, price, STid)
             VALUES ('$UT','$LABEL','$meter','$price','$STid')";
             //echo $sql;
             if (mysqli_query($con, $sql)) {
                  echo "New ID created successfully";
             } else {
		  echo "Error: " . $sql . "<br>" . mysqli_error($con);
             }
             //$result1 = mysqli_query($con,$sql);
        } else {
	     $UT = $_GET[UT];
             $LABEL = $_GET[LABEL];
             $timezone = $_GET[timezone];
             $price = $_GET[price];
	     $STid = $_GET[STid];
	     $sql = "UPDATE utils_list SET price='$price', UT='$UT', MyLabel='$LABEL', STid='$STid' WHERE ID='$meter'";
             mysqli_query($con, $sql);
             //echo "Duplicate ID, NOT Added";
        }
        $sql = "UPDATE ctrl SET timezone='$timezone' WHERE ind=1";
         //mysqli_query($con,$sql);
         if (mysqli_query($con, $sql)) {
              //echo "Shutdown";
         } else {
              echo "Error with timezone: " . mysqli_error($con);
         }
    }

    if($TYPE == "4"){ //Delete Meter
         $meter = $_GET[NUMBER];
         $sql = "DELETE FROM utils_list WHERE ID=$meter";
         //echo $sql."     ";
         //mysql_select_db('Utils');
         if (mysqli_query($con, $sql)) {
              echo "ID Removed Successfully";
         } else {
              echo "Error Removing ID: " . mysqli_error($con);
         }
    }
    if($TYPE == "5"){ //Shut Down
         $sql = "UPDATE ctrl SET shutdown=1 WHERE ind=1";
         //mysqli_query($con,$sql);
         if (mysqli_query($con, $sql)) {
              echo "Shutdown";
         } else {
              echo "Error with Shutdown: " . mysqli_error($con);
         }
    }
    if($TYPE == "6"){
       echo "1";
    }

    if($TYPE == "7"){//Gets data based on start and stop time
         $START = $_GET[START];
         $STOP = $_GET[STOP];
	 $START1 = $_GET[START1];
         $STOP1 = $_GET[STOP1];
	 $START2 = $_GET[START2];
         $STOP2 = $_GET[STOP2];
	 $START3 = $_GET[START3];
         $STOP3 = $_GET[STOP3];
    //$sql = "SELECT *FROM scm_hist WHERE ID IN ($NUMBER)";
         $sql = "SELECT MIN(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START) AND (DT < $STOP)))
         union all
         SELECT MAX(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START) AND (DT < $STOP)))";

    //echo $sql;
         $result = mysqli_query($con,$sql);
         $json = array();
         $meter = $_GET[METER];
         if(mysqli_num_rows($result)){
             while($row=mysqli_fetch_row($result)){
                //print_r($row);
                     $sql = "SELECT ind, DT,  Reading, M_Usage FROM scm_hist WHERE ind = $row[0]";
                     $result1 = mysqli_query($con,$sql);
                     if(mysqli_num_rows($result1)){
                             while($row1=mysqli_fetch_assoc($result1)){
                                     $json[]=$row1;
                                //print_r($row1);
                             }
                     }
             }
             $json = array_merge($REQ, $json);
         }
	 $sql = "SELECT MIN(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START1) AND (DT < $STOP1)))
         union all
         SELECT MAX(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START1) AND (DT < $STOP1)))";

    //echo $sql;
         $result = mysqli_query($con,$sql);
         $json1 = array();
         $meter = $_GET[METER];
         if(mysqli_num_rows($result)){
             while($row=mysqli_fetch_row($result)){
                //print_r($row);
                     $sql = "SELECT ind, DT,  Reading, M_Usage FROM scm_hist WHERE ind = $row[0]";
                     $result1 = mysqli_query($con,$sql);
                     if(mysqli_num_rows($result1)){
                             while($row1=mysqli_fetch_assoc($result1)){
                                     $json1[]=$row1;
                                //print_r($row1);
                             }
                     }
             }
             $json = array_merge($json, $json1);
         }
	 $sql = "SELECT MIN(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START2) AND (DT < $STOP2)))
         union all
         SELECT MAX(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START2) AND (DT < $STOP2)))";

    //echo $sql;
         $result = mysqli_query($con,$sql);
         $json2 = array();
         $meter = $_GET[METER];
         if(mysqli_num_rows($result)){
             while($row=mysqli_fetch_row($result)){
                //print_r($row);
                     $sql = "SELECT ind, DT,  Reading, M_Usage FROM scm_hist WHERE ind = $row[0]";
                     $result1 = mysqli_query($con,$sql);
                     if(mysqli_num_rows($result1)){
                             while($row1=mysqli_fetch_assoc($result1)){
                                     $json2[]=$row1;
                                //print_r($row1);
                             }
                     }
             }
             $json = array_merge($json, $json2);
         }
	 $sql = "SELECT MIN(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START3) AND (DT < $STOP3)))
         union all
         SELECT MAX(ind) as ind FROM `scm_hist` WHERE (ID = $NUMBER AND
         ((DT >= $START3) AND (DT < $STOP3)))";

    //echo $sql;
         $result = mysqli_query($con,$sql);
         $json3 = array();
         $meter = $_GET[METER];
         if(mysqli_num_rows($result)){
             while($row=mysqli_fetch_row($result)){
                //print_r($row);
                     $sql = "SELECT ind, DT,  Reading, M_Usage FROM scm_hist WHERE ind = $row[0]";
                     $result1 = mysqli_query($con,$sql);
                     if(mysqli_num_rows($result1)){
                             while($row1=mysqli_fetch_assoc($result1)){
                                     $json3[]=$row1;
                                //print_r($row1);
                             }
                     }
             }
             $json = array_merge($json, $json3);
         }
    }
    if($TYPE == "8"){ //ADD/Change Meter information
        $meter = $_GET[NUMBER];
        $sql = "SELECT * FROM utils_list WHERE ID = $meter";
        $result1 = mysqli_query($con,$sql);
        if(mysqli_num_rows($result1)){
             while($row1=mysqli_fetch_assoc($result1)){
                  $json[]=$row1;
             }
        }
    }
    if ($TYPE != "6") {
    	header('Content-type: application/json');
    	echo json_encode($json, JSON_PRETTY_PRINT);
    } else {
	header('Content-type: text/html');
    }
    mysqli_free_result($result1);
    
}

mysqli_close($con);
?>


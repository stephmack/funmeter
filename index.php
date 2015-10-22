<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<html>
<head>
    <title>Fun Meter</title>
    <link href="/css_file.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div id="shadow-one"><div id="shadow-two"><div id="shadow-three"><div id="shadow-four">
<div id="page">

<div id="title"><div class="right">Utility Meter Monitor System</div><span id="hello">&nbsp;</span></div>

<div id="menu">
    <a href="/index.php">Console</a>
    <a href="/configure.php">Configure</a>
    <a href="/configure.php">Other</a>
</div>
<div id="content">
	<?php
	include("constants.php");

	$con=mysqli_connect("localhost", "root", "raspberry", "Utils");
	$sql = "SELECT * FROM utils_list";
        $result1 = mysqli_query($con,$sql);
        if(mysqli_num_rows($result1)){
             while($row1=mysqli_fetch_assoc($result1)){
                  $json[]=$row1;
		  $ID = $row1["ID"];
		  $UT = $row1["UT"];
		  $MyLab = $row1["MyLabel"];
		  $CurHr = $row1["CurHr"];
		  $LstHr = $row1["LstHr"];
		  $CurDy = $row1["CurDy"];
                  $LstDy = $row1["LstDy"];
		  $hund = 100;
		  $ten = 10;
		  echo '<table style="width:100%">';
		  echo '<tr><td align="center" width="100%"><h1>';
		  echo $MyLab;
		  echo " - ";
		  echo $UT;
		  echo " - Meter #: ";
		  echo $ID;
		  echo '</h1></td></tr></table>';
		  echo '<h3> &nbsp &nbsp HOUR: '.$CurHr/$hund.' kWh';
		  echo '&nbsp &nbsp LAST HOUR: '.$LstHr/$hund.' kWh<br>';
		  echo '&nbsp &nbsp TODAY: '.$CurDy/$hund.' kWh';
                  echo '&nbsp &nbsp YESTERDAY: '.$LstDy/$hund.' kWh</h3>';
		  echo '<table style="width:50%" align="center">';
		  echo '<tr>';
		  echo '<td align="center" width="50%"><img src=';
                  echo "one_hour_".$UT."_".$ID.".png";
                  echo ' alt="one hour"';
                  echo 'style="width:325px;height:250px;"';
		  echo '></td>';
		  echo '<td align="center" width="50%"><img src=';
		  echo "one_day_".$UT."_".$ID.".png";
		  echo ' alt="one day"';
		  echo 'style="width:400px;height:225px;"';
		  echo '></td></tr>';
		  echo '<tr>';
		  echo '<td align="center" width="50%"><img src=';
		  echo "seven_days_".$UT."_".$ID.".png";
		  echo ' alt="seven days"';
		  echo 'style="width:325px;height:250px;"'; 
		  echo  '></td>';
		  echo '<td align="center" width="50%"><img src=';
                  echo "months_".$UT."_".$ID.".png";
                  echo ' alt="months"';
                  echo 'style="width:325px;height:250px;"';
                  echo  '></td></tr>';
		  echo '</table>';
             }
        }
	mysqli_free_result($result1);
	mysqli_close($con);
	?>

</div> <!--content-->
<div class="spacer">&nbsp;</div>
<div id="footer">Copyright &copy; 2015 3AVentures, Inc.</div>
</div></div></div></div></div>
</body>
</html>


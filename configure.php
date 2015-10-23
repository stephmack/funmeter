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
    <a href="/firmware.php">Firmware Update</a>
</div>
<div id="content">

<?php
	echo '&nbsp &nbsp &nbsp &nbsp<table style="width:50%" border= "1">';
	echo '<tr><td colspan="4" align="center" width="25%"><b>My Utility Meters</b></td></tr>';
        echo '<tr>';
        echo '<td align="center" width="25%"><b><i>Utility</i></b></td>';
        echo '<td align="center" width="25%"><b><i>Label</i></b></td>';
        echo '<td align="center" width="25%"><b><i>Meter ID</i></b></td>';
	echo '<td align="center" width="25%"><b><i>Price</i></b></td>';
        echo '</tr>';
        include("constants.php");
        $cnt = 0;
        $con=mysqli_connect("localhost", "root", "raspberry", "Utils");
        $sql = "SELECT * FROM utils_list";
        $result1 = mysqli_query($con,$sql);
        if(mysqli_num_rows($result1)){
             while($row1=mysqli_fetch_assoc($result1)){
                  $json[]=$row1;
                  $ID = $row1["ID"];
                  $UT = $row1["UT"];
                  $MyLab = $row1["MyLabel"];
		  $price = $row1["price"];
                  $CurHr = $row1["CurHr"];
                  $LstHr = $row1["LstHr"];
                  $CurDy = $row1["CurDy"];
                  $LstDy = $row1["LstDy"];
                  $hund = 100;
                  $ten = 10;
                  $cnt = $cnt + 1;
		  echo '<tr>';
		  echo '<td align="center" width="25%">'.$UT.'</td>';
		  echo '<td align="center" width="25%">'.$MyLab.'</td>';
		  echo '<td align="center" width="25%">'.$ID.'</td>';
		  echo '<td align="center" width="25%">'.$price.'</td>';
		  echo '</tr>';
             }
        }
	echo '</table>';
        mysqli_free_result($result1);
        mysqli_close($con);
        ?>

<form action="configure.php" method="post">
<p> &nbsp &nbsp &nbsp &nbsp Meter ID Numbers<br>
&nbsp &nbsp &nbsp &nbsp <select name="listbox">
<option value=" " Option>Select ID...</option>
 
<?php
	{
        include("constants.php");
	$cnt = 0;
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
		  $cnt = $cnt + 1;
		  echo '<option value="'.$ID.'" Option>'.$ID.'</option>';
             }
        }
	$sql = "SELECT * FROM ctrl";
        $result1 = mysqli_query($con,$sql);
        if(mysqli_num_rows($result1)){
             while($row1=mysqli_fetch_assoc($result1)){
	          $timezone = $row1["timezone"];

	     }
	}
        mysqli_free_result($result1);
        mysqli_close($con);
        ?>
</select></p>
<p>&nbsp &nbsp &nbsp &nbsp <input type="submit" value="Delete Meter" /></p>
</form>
<form action="configure.php" method="post">
<p>&nbsp &nbsp &nbsp &nbsp Utility: <select name="UT"><option value="ELC" Option>ELC</option><option value="GAS" Option>GAS</option><option value="WTR" Option>WTR</option></select></p>
<p>&nbsp &nbsp &nbsp &nbsp Meter Label: <input type="text" name="MyLab" /></p>
<p>&nbsp &nbsp &nbsp &nbsp Meter ID: <input type="text" name="ID" /></p>
<p>&nbsp &nbsp &nbsp &nbsp Cost: <input type="text" name="Price" /></p>
<p>&nbsp &nbsp &nbsp &nbsp <input type="submit" value="Add/Update Meter"/></p>
</form>

<form action="configure.php" method="post">
<p>&nbsp &nbsp &nbsp &nbsp Timezone (current <?php echo $timezone?>): <input type="text" name="timezone" /></p>
<p>&nbsp &nbsp &nbsp &nbsp <input type="submit" value="Update Timezone"/></p>
</form>



<?php if ($_POST['listbox'] != NULL){
	//echo htmlspecialchars($_POST['listbox']);
	$meter = htmlspecialchars($_POST['listbox']);
	echo $meter;
        $sql = "DELETE FROM utils_list WHERE ID=$meter";
	echo $sql;
        $con=mysqli_connect("localhost", "root", "raspberry", "Utils");
        if (mysqli_query($con, $sql)) {
             echo "Meter Removed Successfully";
        } else {
             echo "Error Removing ID: " . mysqli_error($con);
        }
}?>
<?php if ($_POST['ID'] != NULL){
        echo '<p>'.htmlspecialchars($_POST['UT']).'</p>';
	echo '<p>'.htmlspecialchars($_POST['MyLab']).'</p>';
	echo '<p>'.htmlspecialchars($_POST['ID']).'</p>';
	echo '<p>'.htmlspecialchars($_POST['Price']).'</p>';
	$meter = htmlspecialchars($_POST['ID']);
        $sql = "SELECT * FROM utils_list WHERE ID=$meter";
	$con=mysqli_connect("localhost", "root", "raspberry", "Utils");
        $result1 = mysqli_query($con,$sql);
	if(mysqli_num_rows($result1)){
             while($row1=mysqli_fetch_row($result1)){
                  $json1[]=$row1;
		  echo "test";
             }
        }
        if (!($json1)){
             $UT = htmlspecialchars($_POST['UT']);
             $LABEL = htmlspecialchars($_POST['MyLab']);
             $price = htmlspecialchars($_POST['Price']);
             echo $UT.',';
             echo $LABEL.',';
	     echo $ID.',';
	     echo $price.',';
             //$sql = "INSERT INTO utils_list (UT, MyLabel, ID) VALUES ($UT,$LABEL,$meter)";
             $sql = "INSERT INTO utils_list (UT, MyLabel, ID, price)
             VALUES ('$UT','$LABEL','$meter','$price')";
             //echo $sql;
             if (mysqli_query($con, $sql)) {
                  echo "New Meter created successfully";
             } else {
                  echo "Error: " . $sql . "<br>" . mysqli_error($con);
             }
             //$result1 = mysqli_query($con,$sql);
        } else {
             $UT = htmlspecialchars($_POST['UT']);
             $LABEL = htmlspecialchars($_POST['MyLab']);
             $price = htmlspecialchars($_POST['Price']);
             $sql = "UPDATE utils_list SET price='$price', UT='$UT', MyLabel='$LABEL' WHERE ID='$meter'";
             mysqli_query($con, $sql);
             echo "Duplicate ID, NOT Added";
        }
}?>

<?php if ($_POST['timezone'] != NULL){
	echo '<p>'.htmlspecialchars($_POST['timezone']).'</p>';
	$timezone = htmlspecialchars($_POST['timezone']);
	$con=mysqli_connect("localhost", "root", "raspberry", "Utils");
	$sql = "UPDATE ctrl SET timezone='$timezone' WHERE ind=1";
	if (mysqli_query($con, $sql)) {
             echo "Timezone update successfully";
        } else {
             echo "Error: " . $sql . "<br>" . mysqli_error($con);
        }
}
}?>

</div> <!--content-->
<div class="spacer">&nbsp;</div>
<div id="footer">Copyright &copy; 2015 3AVentures, Inc.</div>
</div></div></div></div></div>
</body>
</html>

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
	{
	$con=mysqli_connect("localhost", "root", "raspberry", "Utils");
        $sql = "SELECT * FROM ctrl";
        $result1 = mysqli_query($con,$sql);
        if(mysqli_num_rows($result1)){
             while($row1=mysqli_fetch_assoc($result1)){
                  $json[]=$row1;
                  $ver = $row1["ver1"];
	     }
	}
        mysqli_free_result($result1);
        mysqli_close($con);
?>
<form action="firmware.php" method="post">
<p>&nbsp &nbsp &nbsp &nbsp Current Device Firmware Version: <?php echo $ver ?>, select "Yes" to upgrade?: <select name="ver"><option value="No" Option>No</option><option value="Yes" Option>Yes</option></select></p>
<p>&nbsp &nbsp &nbsp &nbsp <input type="submit" value="Update Firmware"/></p>
</form>

<?php if ($_POST['ver'] == 'Yes'){
        echo '<p>'.htmlspecialchars($_POST['timezone']).'</p>';
        $ver = htmlspecialchars($_POST['ver']);
        $con=mysqli_connect("localhost", "root", "raspberry", "Utils");
        $sql = "UPDATE ctrl SET firmup='1' WHERE ind=1";
        if (mysqli_query($con, $sql)) {
             echo "Updateing Firmware successfully";
        } else {
             echo "Error: " . $sql . "<br>" . mysqli_error($con);
        }
        mysqli_free_result($result1);
        mysqli_close($con);
        }
	if ($_POST['ver'] == 'No'){
        echo '<p>'.htmlspecialchars($_POST['timezone']).'</p>';
        $ver = htmlspecialchars($_POST['ver']);
        $con=mysqli_connect("localhost", "root", "raspberry", "Utils");
        $sql = "UPDATE ctrl SET firmup='0' WHERE ind=1";
        if (mysqli_query($con, $sql)) {
             echo "Do Not Upate...";
        } else {
             echo "Error: " . $sql . "<br>" . mysqli_error($con);
        }
        mysqli_free_result($result1);
        mysqli_close($con);
}
}?>
</div> <!--content-->
<div class="spacer">&nbsp;</div>
<div id="footer">Copyright &copy; 2015 3AVentures, Inc.</div>
</div></div></div></div></div>
</body>
</html>

<?php

/**
 * Start session and 
 * direct to login if
 * creds are not set
 */

session_start();

if (empty($_SESSION['username'])) {

   header("location:login.php");

}

?>

<?php

/**
 * DEPRECATED
 * get server side
 * time. Replaced
 * with client side
 * time
 */

function getsystime() {

   return date('Y-m-d H:i:s');

}

?>
	 
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<script type="text/javascript" src="get_time.js"></script>

<head>
	 
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	 
<meta name="description" content="" />

<meta name="keywords" content="" />
 
<meta name="author" content="" />
	 
<link rel="stylesheet" type="text/css" href="style.css" media="screen" />

<title>powerswitch</title>
	 
</head>
	 
<body onload="startTime()">

<!-- wrapper -->

<div id="wrapper">

<!-- header -->

<div id="header">

<h2>SYSTEM VIDLST</h2>

<div id="time"></div>

</div>

<!-- end #header -->

<!-- scrollbar -->

<div id="scroll">

<form id="relay" action="player.php" method="GET">

<?php include('player.php'); ?>

<?php $play = new Player(); $play->get(); ?>

</form>

</div>

<!-- end #scrollbar -->
 
<!-- logout -->

<div id="logout">

<form name="form2" method="post" action="logout.php">

<h3><input type="submit" name="Submit" value="Logout"></h3>

</form>

<!-- end #logout -->

</div>

<!-- end #wrapper -->

</body>
	 
</html>

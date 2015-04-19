<?php

#-- DELETE --#

session_start();

# get the file for deletion #

$del = $_GET['file'];

# delete file #

unlink($del);

# relocate to main #

header("location:homecam.php");

?>

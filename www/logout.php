<?php

/* start the session */

session_start();

/* redirect to login  */

header('location:login.php');

/* logout */

session_destroy();

?>

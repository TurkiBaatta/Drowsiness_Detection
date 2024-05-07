<?php
    $server = "localhost";
    $user = "root";
    $password = "";
    $data_base_name = "drowsiness";

    $connection = new mysqli($server, $user, $password, $data_base_name);
    if ($connection->connect_error){
        die("Error: ".$connection->connect_error);
    }
?>
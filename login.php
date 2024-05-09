<?php

session_start();
include("conn.php");

// Check of connection.
if (!isset($connection)) {
    die('Connection variable is not set');
}

// Get the data from Form.
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["pass"];

    // Security Testing (Manual Testing).
    // Prepared statement to prevent SQL injection.
    $statement = $connection->prepare("SELECT * FROM login WHERE username = ? AND password = ?");
    $statement->bind_param("ss", $username, $password); // we have two s: 'ss' for the two '?' in the query
    $statement->execute();
    $result = $statement->get_result();

    // 0 means not fund the username
    if ($result->num_rows === 0) {
        echo "<script>alert('Invalid username or password');</script>";
        //echo "<h1 style='text-align: center; padding-top: 100px; padding-bottom: 40px; color: red'> Invalid username or password </h1>";
    } else {
        $row = $result->fetch_assoc();

        $_SESSION["username"] = $username;
        $_SESSION["roleID"] = $row["roleID"]; // Save roleID in session for later use if needed.

        // Here you will go to the page depending on the role.
        switch ($row["role"]) {
            case "admin":
                header("location: adminHome.php");
                break;
            case "driver":
                header("location: driverHome.php");
                break;
            case "evaluator":
                header("location: evaluatorHome.php");
                break;
        }
        exit(); // Prevent the script from continuing after a redirect.
    }
    $statement->close();
}

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <title>Login Page</title>
    <link rel="stylesheet" href="login.css">
    <script lang="javascript" type="text/javascript">
        function Mes() {
            alert("Invalid username or password");
        }
        // To prevent back to login page without logout
        window.history.forward();
    </script>
</head>

<body>
    <div class="container">
        <h2>Login Page</h2>
        <form action="login.php" method="post">
            <label for="username">User name</label>
            <input name="username" type="text" placeholder="Enter your username" required>
            <label for="password">Password</label>
            <input name="pass" type="password" placeholder="Enter your password" required>
            <input name="subm" class="submit" type="submit" value="Login">
        </form>
    </div>

</body>

</html>
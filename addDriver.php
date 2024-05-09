<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
    <style>
        body {
            padding: 0;
            margin: 0;
            background: #e8e8e8;
        }

        h3 {
            text-align: center;
        }

        nav {
            top: 0;
            left: 0;
            bottom: 0;
            height: 100%;
            width: 150px;
            position: fixed;
            padding: 15px;
            background: #fefefe;
            color: black;
            text-transform: uppercase;
            border-radius: 6px;
        }

        nav a {
            display: block;
            padding: 8px;
            margin: 1px;
            color: #464646;
            transition: 0.5s;
            text-decoration: none;
        }

        nav a:hover {
            background: #e4e4e4;
        }

        label {
            margin-bottom: 7px;
            font-size: 15px;
        }

        input {
            border: none;
            padding: 8px;
            margin-bottom: 18px;
            font-size: 15px;
            border-radius: 3px;
            box-shadow: 0px 0px 3px 0px rgba(0, 0, 0, 0.1);
        }

        form {
            flex-direction: column;
            display: flex;
        }

        .container {
            display: fixed;
            padding: 15px;
            margin-left: 180px;
            max-width: 1350px;
        }

        .driver-list {
            padding: 15px;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
        }

        .submit {
            color: #fcfcfc;
            font-size: 15px;
            background-color: #0276f2;
            border-radius: 3px;
            border: none;
            cursor: pointer;
            padding: 8px;
            box-shadow: 0px 0px 3px 0px rgba(0, 0, 0, 0.1);
        }

        .submit:hover {
            background-color: #0460c2;
        }
    </style>
</head>

<body>

    <nav><br>
        <h3>ADMIN</h3>
        <br><br>
        <hr>
        <a href="adminHome.php">&#9962; Dashboard</a>
        <hr>
        <a href="#">&#9547; Add Driver</a>
        <hr>
        <a href="adminReport.php">&#128203; Reports</a>
        <hr>
        <a href="adminProfile.php">&#128100; Profile</a>
        <hr>
        <a href="logout.php">&#128168; Log out</a>
        <hr>
    </nav>

    <div class="container">
        <div class="driver-list">
            <h2>Add Driver</h2>
            <form action="" method="post">

                <label for="roleId">Role ID</label>
                <input name="RoleID" type="number" required>
                <hr>

                <label for="userName">Username</label>
                <input name="UserName" type="text" required>
                <hr>

                <label for="password">Password</label>
                <input name="Password" type="text" required>
                <hr>

                <label for="role">Role</label>
                <input name="Role" type="text" required>
                <hr>

                <label for="driverId">Driver ID</label>
                <input name="DriverID" type="number" required>
                <hr>

                <label for="firstName">First Name</label>
                <input name="Fname" type="text" required>
                <hr>

                <label for="lastName">Last Name</label>
                <input name="Lname" type="text" required>
                <hr>

                <label for="phone">Phone</label>
                <input name="Phone" type="text" required>
                <hr>

                <label for="email">Email</label>
                <input name="Email" type="email" required>
                <hr>

                <input name="subm" class="submit" type="submit" value="Submit">
            </form>

            <?php
            session_start();
            if (!isset($_SESSION['username'])) {
                header("location: login.php");
                exit;
            }
            include("conn.php");

            // Get the data from Form.
            if (isset($_POST["subm"])) {
                $roleid = $_POST["RoleID"];
                $username = $_POST["UserName"];
                $password = $_POST["Password"];
                $role = $_POST["Role"];
                $driverid = $_POST["DriverID"];
                $fname = $_POST["Fname"];
                $lname = $_POST["Lname"];
                $phone = $_POST["Phone"];
                $email = $_POST["Email"];

                try {
                    // This test to ensure we have that username and roleID.
                    $test1 = "select COUNT(*) from login where username='$username' OR roleid='$roleid'";
                    $stat1 = $connection->query($test1);
                    $count1 = $stat1->fetch_column();

                    // This test to ensure we have that driver ID.
                    $test2 = "select COUNT(*) from driver where DriverID='$driverid'";
                    $stat2 = $connection->query($test2);
                    $count2 = $stat2->fetch_column();

                    // Insert in tow table
                    $query1 = "insert into login values($roleid, '$username', '$password', '$role')";
                    $query2 = "insert into driver values($driverid, '$fname', '$lname', '$phone', '$email','$roleid')";

                    // Must be both 0 to conforme new data.
                    if ($count1 == 0 && $count2 == 0) {
                        mysqli_query($connection, $query1);
                        mysqli_query($connection, $query2);
                        echo "Driver Added Successfully";
                    } else {
                        echo "ERROR: You enter wronge inputs try again!!!";
                    }
                } catch (Exception $e) {
                    echo "Error in adding: " . $e;
                }
            }

            $connection->close();
            ?>

        </div>
    </div>
</body>

</html>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driver Dashboard</title>
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

        .container {
            display: fixed;
            padding: 15px;
            margin-left: 180px;
        }

        .driver-list {
            padding: 15px;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
        }

        img:hover {
            transform: scale(3.5);
        }

        table {
            width: 100%;
            margin: 20px 0;
            border-radius: 3px 3px 0 0;
            border-collapse: collapse;
        }

        thead {
            color: white;
            background: #34AF6D;
        }

        th,
        td {
            padding: 10px 10px;
            text-align: left;
        }

        tr:nth-child(even) {
            background: #f2f2f2;
        }

        input {
            border: none;
            padding: 8px;
            margin-bottom: 18px;
            font-size: 15px;
            border-radius: 3px;
            box-shadow: 0px 0px 3px 0px rgba(0, 0, 0, 0.1);
        }

        .sub {
            color: #fcfcfc;
            font-size: 15px;
            background-color: #0276f2;
            border-radius: 3px;
            border: none;
            cursor: pointer;
            padding: 8px;
            box-shadow: 0px 0px 3px 0px rgba(0, 0, 0, 0.1);
        }

        .sub:hover {
            background-color: #0460c2;
        }
    </style>
</head>

<body>

    <nav><br>
        <h3>DRIVER</h3>
        <br><br>
        <hr>
        <a href="#">&#9962; Dashboard</a>
        <hr>
        <a href="driverObjection.php">&#128386; Objection</a>
        <hr>
        <a href="driverTransaction.php">&#128203;Transaction</a>
        <hr>
        <a href="driverProfile.php">&#128100; Profile</a>
        <hr>
        <a href="logout.php">&#128168; Log out</a>
        <hr>
    </nav>

    <div class="container">
        <div class="driver-list">
            <h2>Driver's Reports</h2>
            <?php
            session_start();
            if(!isset($_SESSION['username'])) {
                header("location: login.php");
                exit;
             }

            try {
                include("conn.php");

                if (isset($_SESSION['roleID']) && isset($_SESSION["username"])) {
                    $roleID = $_SESSION['roleID'];
                } else {
                    // Handle the case where $roleID is not set, which could indicate that the user is not logged in
                    echo "Access Denied."; // Or redirect to login page
                    exit; // Exit the script
                }
                $temp = "select DriverID from driver where roleID='$roleID'";
                $res = $connection->query($temp);

                if ($res->num_rows > 0) {
                    $row = $res->fetch_assoc();
                    $_SESSION["id"] = $row["DriverID"];
                    $idd = $_SESSION["id"];
                }

                // SQL query to select data from detection table
                $sql = "SELECT * FROM detection where DriverID='$idd'";
                $result = $connection->query($sql);
                // Check if there are results
                if ($result->num_rows > 0) {
                    // Start create the table in HTML
                    echo '<table>';
                    echo '<tr><th>Detectio Number</th><th>Driver ID</th><th>Picture</th><th>Time</th></tr>';

                    // Output data of each row
                    while ($row = $result->fetch_assoc()) {
                        echo '<tr>';
                        echo '<td>' . htmlspecialchars($row["DetectionID"]) . '</td>';
                        echo '<td>' . htmlspecialchars($row["DriverID"]) . '</td>';
                        echo '<td><img class="big" src="data:image/jpeg;base64,' . base64_encode($row['Picture']) . '" height="100px" width="100px"/></td>';
                        echo '<td>' . htmlspecialchars($row["Time"]) . '</td>';
                        echo '</tr>';
                    }
                    echo '</table>';
                } else {
                    echo "0 results";
                }
            } catch (Exception $e) {
                echo $e->getMessage();
            }
            $connection->close();
            ?>

        </div>
    </div>
</body>

</html>
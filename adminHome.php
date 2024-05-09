<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
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
    </style>
</head>

<body>

    <nav><br>
        <h3>ADMIN</h3>
        <br><br>
        <hr>
        <a href="#">&#9962; Dashboard</a>
        <hr>
        <a href="addDriver.php">&#9547;  Add Driver</a>
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
            <h2>Driver's List</h2>
            <?php
            session_start();
            if(!isset($_SESSION['username'])) {
                header("location: login.php");
                exit;
             }
            include("conn.php");

            // SQL query to select data from your table.
            $sql = "SELECT * FROM driver";
            $result = $connection->query($sql);

            // if result > 0 that means we have at least one detection.
            if ($result->num_rows > 0) {
                // Create the table in HTML.
                echo '<table>';
                echo '<tr><th>DriverID</th><th>Fname</th><th>Lname</th><th>Phone</th><th>Email</th></tr>';

                // Output data of each row.
                while ($row = $result->fetch_assoc()) {
                    echo '<tr>';
                    echo '<td>' . htmlspecialchars($row["DriverID"]) . '</td>'; // Converts special characters into HTML entities.
                    echo '<td>' . htmlspecialchars($row["Fname"]) . '</td>';
                    echo '<td>' . htmlspecialchars($row["Lname"]) . '</td>';
                    echo '<td>' . htmlspecialchars($row["Phone"]) . '</td>';
                    echo '<td>' . htmlspecialchars($row["Email"]) . '</td>';
                    echo '</tr>';
                }
                echo '</table>';
            } else {
                echo "0 results";
            }
            $connection->close();
            ?>
        </div>
    </div>
</body>

</html>
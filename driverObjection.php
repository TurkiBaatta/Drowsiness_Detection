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
        <h3>DRIVER</h3>
        <br><br>
        <hr>
        <a href="driverHome.php">&#9962; Dashboard</a>
        <hr>
        <a href="#">&#128386; Objection</a>
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
            <h2>Send Objection</h2>
            <form action="" method="post">
                <label for="detectionId">Detection ID</label>
                <input name="DetectionID" type="number" required>
                <hr>
                <label for="reason">Reason</label>
                <textarea name="Reason" rows="4" cols="50" maxlength="150"></textarea>
                <br>

                <input name="subm" class="submit" type="submit" value="Send">
            </form>

            <?php
            session_start();
            if (!isset($_SESSION['username'])) {
                header("location: login.php");
                exit;
            }
            include("conn.php");

            if (isset($_POST["subm"])) {
                $detectionid = $_POST["DetectionID"];
                $driverid = $_SESSION["id"];
                $status = null;
                $reason = $_POST["Reason"];

                try {
                    $test = "select COUNT(*) from detection WHERE DriverID='$driverid' and DetectionID='$detectionid'";
                    $stat = $connection->query($test);
                    $count = $stat->fetch_column();

                    // preven symbol in Reason
                    $symbols = ",./;?()-!:[]{}~`*&^%$#@\|<>=+_'";

                    // Remove symbol characters
                    $reason = str_replace(str_split($symbols), '', $reason);

                    if ($count != 0) {
                        $query = "insert into objection values('', '$detectionid', '$driverid', '$status', '$reason')";
                        $query2 = "select DetectionID from objection where DetectionID='$detectionid' and DriverID='$driverid'";
                        $check = $connection->query($query2);

                        if ($check->num_rows > 0) {
                            echo "Detection number is already sended, checking your transaction.";
                        } elseif (mysqli_query($connection, $query)) {
                            echo "Objection Added Successfully";
                        }
                    } else {
                        echo "ERROR: There is no detection number like this in your report!!!";
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
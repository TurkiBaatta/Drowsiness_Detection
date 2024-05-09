<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evaluator Dashboard</title>
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

        form {
            flex-direction: column;
            display: flex;
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
            max-width: 1350px;
        }

        .driver-list {
            padding: 15px;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
        }

        .lab {
            margin-bottom: 7px;
            font-size: 15px;
        }

        .inp {
            border: none;
            padding: 8px;
            margin-bottom: 18px;
            font-size: 15px;
            border-radius: 3px;
            box-shadow: 0px 0px 3px 0px rgba(0, 0, 0, 0.1);
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
        <h3>EVALUATOR</h3>
        <br><br>
        <hr>
        <a href="evaluatorHome.php">&#9962; Dashboard</a>
        <hr>
        <a href="#">&#128386; Objection</a>
        <hr>
        <a href="evaluatorReport.php">&#128203; Reports</a>
        <hr>
        <a href="evaluatorProfile.php">&#128100; Profile</a>
        <hr>
        <a href="logout.php">&#128168; Log out</a>
        <hr>
    </nav>

    <div class="container">
        <div class="driver-list">
            <h2>Send Reply</h2>
            <form action="" method="post">
                <label class="lab" for="objectionid">Objection ID</label>
                <input class="inp" name="ObjectionID" type="number" required>

                <p>
                    <label for="approve">Approve
                        <input name="stat" type="radio" value="Approve" required>
                    </label>

                    <label for="declined">Declined
                        <input name="stat" type="radio" value="Declined" required>
                    </label>
                </p>
                <hr>

                <input name="subm" class="submit inp" type="submit" value="Send">
            </form>

            <?php
            session_start();
            if (!isset($_SESSION['username'])) {
                header("location: login.php");
                exit;
            }
            include("conn.php");

            if (isset($_POST["subm"])) {
                $objectionid = $_POST["ObjectionID"];
                $status = $_POST["stat"];

                try {
                    $query = "update objection set status='$status' where ObjID='$objectionid'";
                    $query2 = "select status from objection where ObjID='$objectionid'";
                    // Check if objection Is there or not.
                    $check = $connection->query($query2);

                    if ($check) {
                        $str = $check->fetch_assoc();
                        if ($str) {
                            $stat = $str['status'];
                            if ($stat != "") {
                                // Status has value in database.
                                echo "Status is already sended.";
                            } elseif (mysqli_query($connection, $query)) {
                                // Status will store in database.
                                echo "Reply Sent Successfully";
                            }
                        } else {
                            // if check return false, that means there no objection ID in database.
                            echo "There is no Objection ID like this!!!";
                        }
                    } else {
                        echo "Error in adding: " . $connection->connect_error;
                    }
                } catch (Exception $e) {
                    echo "ERROR: There is no Objection number like this!!!";
                }
            }

            $connection->close();
            ?>

        </div>
    </div>
</body>

</html>
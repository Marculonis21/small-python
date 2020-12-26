<?php 
session_start();
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Filmy</title>
        
        <link rel="stylesheet" href="styles/defStyles.css">
        <link rel="stylesheet" href="styles/homeS.css">

        <script src="https://kit.fontawesome.com/51c469df5d.js" crossorigin="anonymous"></script>
    </head>
    <body>
        <!-- první header--!>
        <div class="start">
            <span class="info">IVT PROJEKT</span>
            <span class="nadpis">Knihovna Filmů</span>
            <span class="info">Marek Bečvář</span>
        </div>

        <!-- tlačítka --!>
        <span id="l" class="topnav">
            <button onclick="location.href='index.php'">Home</button>
            <button onclick="location.href='lib.php'">Knihovna</button>
            <button onclick="location.href='search.php'">Hledat</button>
        </span>
        <span id="r" class="topnav">
            <button onclick="location.href='log.php'">
            <?php 
            if(!isset($_SESSION['userLogin']))
            {
                echo "Login";
            }
            else
            {
                echo $_SESSION['userLogin'];
            }
            ?>
            </button>
            <button onclick="location.href='reg.php'">Registrace</button>
        </span>
        
        <!-- separátor sekce pod tlačítky --!>
        <div id="viz-separátor" style="display:flex; height:75px"></div>

        <!-- ###### TABS ###### --!>

        <!-- HOME --!>
        <div id="Home" class="tabcontent">
            <p>Knihovna filmů</p>
            <p class="text">Projekt: Vytvoření vlastní databáze filmů. 
            <br>Vytvořeno XA IVT 2020.</p>
        </div>

    </body>
    <?php 
        function regBtn()
        {
            $conn = mysqli_connect('localhost', 'movieAdmin', '123456789', 'movieDB');

            if(!$conn)
            {
                die("Connection failed" . mysqli_connect_error());
            }
            else
            {
                $name = $_POST['username'];
                $pass = hash("md5",$_POST['password']);

                $testSql = "SELECT login FROM user_table";
                $testRes = mysqli_query($conn, $testSql);
                $FOUND = false;
                foreach($testRes as $testName)
                {
                    if($testName['login'] === $name)
                    {
                        $FOUND = true;
                        break;
                    }
                }

                if($FOUND)
                {
                    $_SESSION['wantedPage'] = 'Register';
                }
                else
                {
                    $sql = "INSERT INTO user_table (login, password) VALUES ('$name', '$pass')";
                    mysqli_query($conn, $sql); 
                    $_SESSION['userLogin'] = $name; 
                }
            } 

            
            mysqli_close($conn); 

            //POST-REDIRECT-GET
            header("Location: " . $_SERVER['REQUEST_URI']);
            exit();
        }

        function logBtn()
        {
            $conn = mysqli_connect('localhost', 'movieAdmin', '123456789', 'movieDB');

            if(!$conn)
            {
                die("Connection failed" . mysqli_connect_error());
            }
            else
            {
                $name = $_POST['log_username'];
                $pass = hash("md5",$_POST['log_password']);

                $sql = "SELECT * FROM user_table";
                $result = mysqli_query($conn, $sql);

                foreach($result as $item)
                {
                    if($name === $item['login'])
                    {
                        if($pass === $item['password'])
                        {
                            $_SESSION['userLogin'] = $name;
                            break;
                        }
                    }
                }
            }
            mysqli_close($conn);

            //POST-REDIRECT-GET
            header("Location: " . $_SERVER['REQUEST_URI']);
        }
    ?>

</html>

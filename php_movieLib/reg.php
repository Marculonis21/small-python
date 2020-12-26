<?php 
session_start();
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Filmy</title>
        
        <link rel="stylesheet" href="styles/defStyles.css">
        <link rel="stylesheet" href="styles/regS.css">

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

        <div id="Register" class="tabcontent">
            Registrace

            <form method="POST">
                <div class="form">
                    <input type="text" name="username" required autocomplete="off" spellcheck="false">
                    <label for="text" class="label">
                        <span class='labeltext'>Login</span>
                    </label>
                </div>

                <div class="form">
                    <input type="password" name="password" required autocomplete="off" spellcheck="false">
                    <label for="text" class="label">
                        <span class='labeltext'>Heslo</span>
                    </label>
                </div>

                <span class="btnCont">
                    <button type="reset" class="btn"><i class="far fa-times-circle"></i></button>
                    <button type="submit" name="submitbtn" class="btn"><i class="far fa-check-circle"></i></button>
                </span>
            </form>
        </div>


        <?php 
            if(isset($_POST['submitbtn']))
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
                        
                        echo "<p style=\"text-align:center; font-family: 'Righteous'; font-size: 25px;\">Zvolený login se již používá</p>";
                        mysqli_close($conn); 
                    }
                    else
                    {
                        $sql = "INSERT INTO user_table (login, password) VALUES ('$name', '$pass')";
                        mysqli_query($conn, $sql); 
                        $_SESSION['userLogin'] = $name; 

                        mysqli_close($conn); 
                        //POST-REDIRECT-GET
                        header("Location: index.php ");
                        exit();
                    }
                } 
            }
        ?>
    </body>
</html>

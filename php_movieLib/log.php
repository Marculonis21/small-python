<?php 
session_start();
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Filmy</title>
        
        <link rel="stylesheet" href="styles/defStyles.css">
        <link rel="stylesheet" href="styles/logS.css">

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

        <div id="Login" class="tabcontent">
            <?php 
                $logoutbtn = false;
                if(!isset($_SESSION['userLogin']))
                {
                    echo"
                    Přihlášení
                    <form method=\"POST\">
                        <div class=\"form\">
                            <input type=\"text\" name=\"username\" required autocomplete=\"off\" spellcheck=\"false\">
                            <label for=\"text\" class=\"label\">
                                <span class='labeltext'>Login</span>
                            </label>
                        </div>

                        <div class=\"form\">
                            <input type=\"password\" name=\"password\" required autocomplete=\"off\" spellcheck=\"false\">
                            <label for=\"text\" class=\"label\">
                                <span class='labeltext'>Heslo</span>
                            </label>
                        </div>

                        <span class=\"btnCont\">
                            <button type=\"reset\" class=\"btn\"><i class=\"far fa-times-circle\"></i></button>
                            <button type=\"submit\" name=\"submitbtn\" class=\"btn\"><i class=\"far fa-check-circle\"></i></button>
                        </span>
                    </form>
                    ";
                }
                else
                {
                    echo "
                    <form class=\"Log\" method=\"POST\">
                        <span id=\"first\">Uživatel:</span>
                        <span id=\"sec\">Login: " . $_SESSION['userLogin'] . "</span>
                        <span id=\"btn-container\">
                        <button name=\"logoutbtn\" type\"submit\" id=\"btn\">Log-out <i class=\"far fa-times-circle\"></i></button>
                        </span>
                    </form>
                    ";
                }
            ?>
        </div>
        <?php
            if(isset($_POST['logoutbtn']))
            {
                $_SESSION['userLogin'] = "";
                unset($_SESSION['userLogin']);

                //POST-REDIRECT-GET
                header("Location: " . $_SERVER['REQUEST_URI']);
            }
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
    </body>
</html>

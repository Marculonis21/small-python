<?php 
session_start();

$locale='cs_CZ.UTF-8';
setlocale(LC_ALL,$locale);
putenv('LC_ALL='.$locale);
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Filmy</title>
        
        <link rel="stylesheet" href="styles/defStyles.css">
        <link rel="stylesheet" href="styles/libS.css">

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

        <?php
            if(!isset($_SESSION['userLogin']))
            {
                echo"
                <div class=\"tableC\">
                    <div class=\"tRow\">
                        <div class=\"empty-tBlock\">
                            <p>Nejdřív se musíte přihlásit!</p> 
                        </div>
                    </div>
                </div>
                ";
            }
            else
            {
                $conn = mysqli_connect('localhost', 'movieAdmin', '123456789', 'movieDB');
                if(!$conn)
                {
                    die("Connection failed" . mysqli_connect_error());
                }
                else
                {
                    if(isset($_POST["fav_movie_button"]))
                    {
                        $sql_search = "SELECT * from data_table WHERE owner_id=\"".$_SESSION['userLogin']."\";";
                        $query = mysqli_query($conn, $sql_search);

                        $selected_item = $_POST["selected"];

                        $sql_order = $_POST["sql_order"];
                        $sort = $_POST["sort"];

                        foreach($query as $item)
                        {
                            if($item["pic_path"] == $selected_item)
                            {
                                if($item["favourite"] == 1)
                                {
                                    $sql_update = "UPDATE data_table SET favourite = 0 WHERE pic_path=\"".$selected_item."\";";
                                }
                                else
                                {
                                    $sql_update = "UPDATE data_table SET favourite = 1 WHERE pic_path=\"".$selected_item."\";";
                                }
                                break;
                            }
                        }
                        mysqli_query($conn, $sql_update);
                    }
                    else if(isset($_POST["remove_movie_button"]))
                    {
                        $selected_item = $_POST["selected"];

                        $sql_order = $_POST["sql_order"];
                        $sort = $_POST["sort"];

                        $sql_delete = "DELETE from data_table WHERE pic_path=\"".$selected_item."\";";
                        mysqli_query($conn, $sql_delete);
                    }
                    else if(!isset($_POST["sort_button"]))
                    {
                        $sort = "abc-down";
                        $sql_order = "name ASC";
                    }

                    #TEST KOLIK JE FILMŮ V KNIHOVNĚ
                    $sql_search = "SELECT * from data_table WHERE owner_id=\"".$_SESSION['userLogin']."\";";
                    $query = mysqli_query($conn, $sql_search);

                    if(mysqli_num_rows($query) != 0)
                    {
                        if(isset($_POST["sort_button"]))
                        {
                            $sort = $_POST["sort_button"];
                        }

                        echo"
                        <form method=\"POST\" >
                            <div class=\"item_sorting\">
                                <div id=\"sort_group_1\">
                        ";
                        if($sort == "abc-down")
                        {
                            echo "<button type=\"submit\" class=\"selected\" name=\"sort_button\" value=\"abc-down\" ><i class=\"fas fa-sort-alpha-down\"></i></button>";
                            $sql_order = "name ASC";
                        }
                        else
                        {
                            echo "<button type=\"submit\" name=\"sort_button\" value=\"abc-down\" ><i class=\"fas fa-sort-alpha-down\"></i></button>";
                        }

                        if($sort == "abc-up")
                        {
                            echo "<button type=\"submit\" class=\"selected\" name=\"sort_button\" value=\"abc-up\" ><i class=\"fas fa-sort-alpha-up\"></i></button>";
                            $sql_order = "name DESC";
                        }
                        else
                        {
                            echo "<button type=\"submit\" name=\"sort_button\" value=\"abc-up\" ><i class=\"fas fa-sort-alpha-up\"></i></button>";
                        }
                        echo "</div>";
                        echo "<div id=\"sort_group_2\">";
                        if($sort == "rating-down")
                        {
                            echo "<button type=\"submit\" class=\"selected\" name=\"sort_button\" value=\"rating-down\" ><i class=\"fas fa-sort-amount-down\"></i></button>";
                            $sql_order = "score DESC";
                        }
                        else
                        {
                            echo "<button type=\"submit\" name=\"sort_button\" value=\"rating-down\" ><i class=\"fas fa-sort-amount-down\"></i></button>";
                        }

                        if($sort == "rating-up")
                        {
                            echo "<button type=\"submit\" class=\"selected\" name=\"sort_button\" value=\"rating-up\" ><i class=\"fas fa-sort-amount-up\"></i></button>";
                            $sql_order = "score ASC";
                        }
                        else
                        {
                            echo "<button type=\"submit\" name=\"sort_button\" value=\"rating-up\" ><i class=\"fas fa-sort-amount-up\"></i></button>";
                        }

                        if($sort == "fav-sort")
                        {
                            echo "<button type=\"submit\" class=\"selected\" name=\"sort_button\" value=\"fav-sort\" ><i class=\"fas fa-star\"></i></button>";
                            $sql_order = "name ASC";
                        }
                        else
                        {
                            echo "<button type=\"submit\" name=\"sort_button\" value=\"fav-sort\" ><i class=\"fas fas fa-star\"></i></button>";
                        }
                        echo "
                                </div>
                            </div>
                        </form>
                        ";
                    }

                    if($sort != "fav-sort")
                    {
                        $sql_search = "SELECT * from data_table WHERE owner_id=\"".$_SESSION['userLogin']."\" ORDER BY ".$sql_order.";";
                        $query = mysqli_query($conn, $sql_search);
                    }
                    else
                    {
                        $sql_search = "SELECT * from data_table WHERE favourite=1 and owner_id=\"".$_SESSION['userLogin']."\" ORDER BY ".$sql_order.";";
                        $query = mysqli_query($conn, $sql_search);
                    }

                    ### TABLE
                    echo"
                    <div class=\"tableC\">
                        <div class=\"tRow\">
                    ";

                    if(mysqli_num_rows($query) != 0)
                    {
                        foreach($query as $item)
                        {
                            echo"
                            <div class=\"tBlock\">
                                <img src=\"" . $item["pic_path"] . "\" alt=\"None Found\">
                                <form method=\"POST\">
                                    <input type=\"text\" name=\"sql_order\" value=\"".$sql_order."\">
                                    <input type=\"text\" name=\"sort\" value=\"".$sort."\">
                                    <input type=\"text\" name=\"selected\" value=\"".$item["pic_path"]."\">
                                    <button id=\"remove_mov\" type=\"submit\" name=\"remove_movie_button\">Odebrat <i class=\"fas fa-minus-circle\"></i></button>
                                    ";
                                    if($item["favourite"] == 1)
                                    {
                                        echo "<button id=\"fav_mov\" type=\"submit\" name=\"fav_movie_button\"><i class=\"fas fa-star\"></i></button>";
                                    }
                                    else
                                    {
                                        echo "<button id=\"fav_mov\" type=\"submit\" name=\"fav_movie_button\"><i class=\"far fa-star\"></i></button>";
                                    }
                                echo"
                                </form>
                                <div class=\"under\">
                                    <p id=\"head\">" . OWN_DECODE($item["name"]) . "</p>
                                    <p id=\"aka\">aka: " . OWN_DECODE($item["aka"]) . "</p>
                                    <br>
                                    <p id=\"info\">" . OWN_DECODE($item["info"]) . "</p>
                                    <br>
                                    <p id=\"score\">Score: " . $item["score"] . "/10</p>
                                </div>
                            </div>
                            ";

                        }
                    }
                    else
                    {
                        if($sort == "fav-sort")
                        {
                            echo"
                            <div class=\"empty-tBlock\">
                                <p>Zatím nemáte žádné oblíbené filmy.</p> 
                            </div>
                            ";
                        }
                        else
                        {
                            echo"
                            <div class=\"empty-tBlock\">
                                <p>Vaše knihovna je zatím prázdná.</p> 
                            </div>
                            ";
                        }
                    }

                    echo"
                        </div>
                    </div>
                    ";
                    ### TABLE

                }
                
                mysqli_close($conn);
            }


            function OWN_DECODE($text)
            {
                ### CZ STRING FORMATING
                $changeThat = (str_split($text));

                $changed = "";
                for($i = 0; $i < count($changeThat); $i++)
                {
                    if($changeThat[$i] == '.' && $i <= count($changeThat) - 8)
                    {
                        $m = $changeThat; 
                        $s = $m[$i].$m[$i+1].$m[$i+2].$m[$i+3].$m[$i+4].$m[$i+5].$m[$i+6].$m[$i+7];

                        #CZ
                        if($s == ".xc4.x9b")
                        {
                            $s = 'ě';
                        }
                        if($s == ".xc3.xbd")
                        {
                            $s = 'ý';
                        }
                        if($s == ".xc3.xa1")
                        {
                            $s = 'á';
                        }
                        if($s == ".xc4.x8d")
                        {
                            $s = 'č';
                        }
                        if($s == ".xc4.x8f")
                        {
                            $s = 'ď';
                        }
                        if($s == ".xc3.xa9")
                        {
                            $s = 'é';
                        }
                        if($s == ".xc3.xad")
                        {
                            $s = 'í';
                        }
                        if($s == ".xc5.x88")
                        {
                            $s = 'ň';
                        }
                        if($s == ".xc5.x99")
                        {
                            $s = 'ř';
                        }
                        if($s == ".xc5.xa0")
                        {
                            $s = 'š';
                        }
                        if($s == ".xc5.xa5")
                        {
                            $s = 'ť';
                        }
                        if($s == ".xc5.xaf")
                        {
                            $s = 'ů';
                        }
                        if($s == ".xc3.xba")
                        {
                            $s = 'ú';
                        }
                        if($s == ".xc3.x9a")
                        {
                            $s = 'Ú';
                        }
                        if($s == ".xc5.xbe")
                        {
                            $s = 'ž';
                        }

                        $changed .= $s;

                        $i += 7;
                    }
                    else
                    {
                        $changed .= $changeThat[$i];
                    }
                }

                return $changed;
            }
        ?>
    </body>
</html>

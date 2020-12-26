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
        <link rel="stylesheet" href="styles/searchS.css">
        <link rel="stylesheet" href="styles/searchS_loader.css">

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

        <div id="search">
            <form method="POST">
                <div id="userSet">
                    <p>Vyhledávání filmů</p>
                    
                    <div class="tabs">
                        <div class="tab">
                            <input type="radio" id="nameBut" name="radio_group" value="rb1" onclick="checkFunction()" checked />
                            <label for="nameBut" id="nameLabel" >Název Filmu</label>
                        </div>
                        <div class="tabH">
                            <input type="radio" id="authorBut" name="radio_group" value="rb2" onclick="checkFunction()" />
                            <label for="authorBut" id="authorLabel">Autor</label>
                        </div>
                        <div class="tabH">
                            <input type="radio" id="yearBut" name="radio_group" value="rb3" onclick="checkFunction()" />
                            <label for="yearBut" id="yearLabel">Rok Vydání</label>
                        </div>
                    </div>
                </div>

                <div class="form">
                    <div class="opts" id="nameSearch">
                        <input type="text" id="inputName" name="name" autocomplete="off" spellcheck="false" >
                        <label for="text" class="label">
                            <span class='labeltext'>Název Filmu</span>
                            <span class='labeltext-hide'>* v anglickém j.</span>
                        </label>
                    </div>
                    <div class="opts" id="authorSearch">
                        <input type="text" id="inputAuthor" name="author" autocomplete="off" spellcheck="false">
                        <label for="text" class="label">
                            <span class='labeltext'>Jméno Autora</span>
                        </label>
                    </div>
                    <div class="opts" id="yearSearch">
                        <input type="text" id="inputYear" name="date" autocomplete="off" spellcheck="false">
                        <label for="text" class="label">
                            <span class='labeltext'>Rok Vydání</span>
                        </label>
                    </div>

                    <div class="btnCont">
                        <button type="reset" class="btn"><i class="far fa-times-circle"></i></button>
                        <button type="submit" name="find_button" class="btn" onclick="submitFunction()"><i class="far fa-check-circle"></i></button>
                    </div>
                </div>
            </form>
        </div>
        
        <!-- LOADER AND LOADING SCRIPT--!>
        <div id="loader">
            <div class="spinner">
                <div class="rect1"></div>
                <div class="rect2"></div>
                <div class="rect3"></div>
                <div class="rect4"></div>
                <div class="rect5"></div>
                <div class="rect6"></div>
                <div class="rect7"></div>
                <div class="rect8"></div>
                <div class="rect9"></div>
                <div class="rect0"></div>
            </div>
        </div>

        <script>
            document.getElementById("loader").style.display = "none";

            function submitFunction()
            {
                document.getElementById("loader").style.display = "block";
            }
        </script>

        <!-- GET ALL THE MOVIE 101 --!>
        <?php 
            if(isset($_POST['find_button']) 
            || isset($_POST['plus_page']) 
            || isset($_POST['minus_page']) 
            || isset($_POST['add_movie_button']))
            {

                #IF FIND_BUTTON
                # find which radiobutton was used
                if(isset($_POST['radio_group']))
                {
                    switch($_POST['radio_group'])
                    {
                        case "rb1":
                            $searchVar = $_POST["name"];
                            $searchType = "-M";
                            break;

                        case "rb2":
                            $searchVar = $_POST["author"];
                            $searchType = "-A";
                            break;

                        case "rb3":
                            $searchVar = $_POST["date"];
                            $searchType = "-Y";
                            break;
                    }
                }
                else #IF NOT FIND_BUTTON -> PLUS/MINUS/ADD
                {
                    $searchVar = $_POST["name"];
                    $searchType = "-M";
                    $pageNumber = $_POST["number"];
                }

                # PAGE NUMBERING
                if(!isset($pageNumber))
                {
                    $pageNumber = 1;
                }
                if(isset($_POST["plus_page"]))
                {
                    $pageNumber += 1;
                }
                if(isset($_POST["minus_page"]))
                {
                    $pageNumber -= 1;
                }

                # HOW MANY TO LOAD
                $LOADNUMBER = 5;

                #########################
                #########################
                #########################
                
                if(isset($_POST["add_movie_button"])) # MOVIE ADDED
                {
                    $searchVar = $_POST["name"];
                    $searchType = "-M";
                    $pageNumber = $_POST["number"];
                    $raw_out = $_POST["raw_output"];
                    $output = $_POST["output"];
                    $selected = $_POST["selected"];

                    # CHECK FOR USER LOGIN
                    if(!isset($_SESSION['userLogin']))
                    {
                        echo"
                        <div id=\"note\">
                            <p id=\"error\">Nejdřív se musíte přihlásit/zaregistrovat!</p>
                        </div >
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
                            $_raw_out = explode('|', $raw_out);
                            $main = explode(';', $_raw_out[$selected]);

                            $owner = utf8_decode($_SESSION['userLogin']);
                            $pic = $main[2];
                            $name = utf8_decode($main[0]);
                            try
                            {
                                $aka = utf8_decode($main[1]);
                            } 
                            catch (Exception $e)
                            {
                                $aka = "";
                            }

                            try
                            {
                                $info = utf8_decode($main[3]);
                            }
                            catch (Exception $e)
                            {
                                $info = "None";
                            }

                            try
                            {
                                $score = $main[4];
                            }
                            catch (Exception $e)
                            {
                                $score = "None";
                            }
 
                            # CHECK IF ALREADY ADDED
                            $sql_user_test = "SELECT name from data_table WHERE owner_id=\"".$owner."\"";
                            $query = mysqli_query($conn, $sql_user_test);
                            $FOUND = False;

                            foreach($query as $item) 
                            {
                                #print_r($item);
                                #echo"<br>";
                                if($item["name"] == $name)
                                {
                                    $FOUND = True;
                                    break;
                                }
                            }

                            #IF ADDED
                            if($FOUND)
                            {
                                echo"
                                <div id=\"note\">
                                    <p id=\"info\">Film již je ve vaší knihovně!</p>
                                </div >
                                ";
                            }
                            else #IF NOT
                            {
                                echo"
                                <div id=\"note\">
                                    <p id=\"valid\">Film byl přidán do vaší knihovny</p>
                                </div >
                                ";

                                $sql_add = "INSERT into data_table (owner_id,pic_path,name,aka,info,score) VALUES (\"".$owner."\",\"".$pic."\",\"".$name."\",\"".$aka."\",\"".$info."\",\"".$score."\")";
                                mysqli_query($conn, $sql_add);
                            }

                            mysqli_close($conn);
                        }
                    }

                    unset($_POST["add_movie_button"]);
                }

                if(!isset($raw_out)) # NORMAL MODE - SEARCH MOVIES
                {
                    # PYTHON SCRIPT RETURNING IMG AND MOVIE DATA

                    # LANG="cs_CZ.UTF-8" locale
                    # byla potřeba upravit shell_exec
                    
                    $raw_out = shell_exec("python3 pythonS/movieScrape.py " . $searchType . " " . $LOADNUMBER . " " . $pageNumber .  "  \"" . $searchVar . "\" 2>&1");


                    ### CZ STRING FORMATING
                    $changeThatShit = (str_split($raw_out));

                    $changed = "";
                    for($i = 0; $i < count($changeThatShit); $i++)
                    {
                        if($changeThatShit[$i] == "\\")
                        {
                            $m = $changeThatShit; 
                            $s = $m[$i].$m[$i+1].$m[$i+2].$m[$i+3].$m[$i+4].$m[$i+5].$m[$i+6].$m[$i+7];

                            #CZ
                            if($s == '\\xc4\\x9b')
                            {
                                $s = 'ě';
                            }
                            if($s == '\\xc3\\xbd')
                            {
                                $s = 'ý';
                            }
                            if($s == '\\xc3\\xa1')
                            {
                                $s = 'á';
                            }
                            if($s == '\\xc4\\x8d')
                            {
                                $s = 'č';
                            }
                            if($s == '\\xc4\\x8f')
                            {
                                $s = 'ď';
                            }
                            if($s == '\\xc3\\xa9')
                            {
                                $s = 'é';
                            }
                            if($s == '\\xc3\\xad')
                            {
                                $s = 'í';
                            }
                            if($s == '\\xc5\\x88')
                            {
                                $s = 'ň';
                            }
                            if($s == '\\xc5\\x99')
                            {
                                $s = 'ř';
                            }
                            if($s == '\\xc5\\xa0')
                            {
                                $s = 'š';
                            }
                            if($s == '\\xc5\\xa5')
                            {
                                $s = 'ť';
                            }
                            if($s == '\\xc5\\xaf')
                            {
                                $s = 'ů';
                            }
                            if($s == '\\xc3\\xba')
                            {
                                $s = 'ú';
                            }
                            if($s == '\\xc3\\x9a')
                            {
                                $s = 'Ú';
                            }
                            if($s == '\\xc5\\xbe')
                            {
                                $s = 'ž';
                            }

                            $changed .= $s;

                            $i += 7;
                        }
                        else
                        {
                            $changed .= $changeThatShit[$i];
                        }
                    }
                    $output = $changed;


                    ### FORMATING FOR CZ TO SQL - DECODE LATER
                    $_new = (str_split($raw_out));
                    $smallChange = "";
                    for($i = 0; $i < count($_new); $i++)
                    {
                        if($_new[$i] == "\\")
                        {
                            $_new[$i] = '.';
                        }

                        $smallChange .= $_new[$i];
                    }

                    $raw_out = $smallChange;

                    ### STRING FORMATING END
                }

                ### #SAVED
                # PYTHON ENCODING WAS F****** UP MY "INPUT FIELD DATA TRANSFER METHOD"
                $output = explode('|', $output);
                $raw_out_split = explode('|', $raw_out);

                if(strpos($output[0], 'b') !== false)
                {
                    $end = sizeof($output) - 1;

                    $output[0] = substr($output[0], 2);
                    array_pop($output);

                    $raw_out_split[0] = substr($raw_out_split[0], 2);
                    array_pop($raw_out_split);
                }
                ### 
                
                # PARSE OUTPUT FOF FIRST INFO ABOUT HOW MANY MOVIES WERE FOUND 
                # AND HOW MANY PAGES WILL WE HAVE + IF ANOTHER PAGE IS 
                # AVAILABLE
                
                # INFO ABOUT NUMBER OF PAGES AND LOADING
                $fInfo = explode(';', $output[0]);
                $total_size = (int)$fInfo[1];
                $more_to_load = (boolean)$fInfo[2];
                
                #print_r($fInfo);

                if($total_size != 0)
                {
                    # PAGE ARROWS
                    if($more_to_load)
                    {
                        # ceil = round up to int
                        $page_count = ceil($total_size/$LOADNUMBER );
                        if($pageNumber == 1 && $pageNumber == $page_count)
                        {
                            echo"
                            <form method=\"POST\" class=\"pages_form\">
                                <div class=\"count_pages\">
                                    <input type=\"text\" name=\"name\" value=\"".$searchVar."\">
                                    <input type=\"text\" name=\"number\" value=\"".$pageNumber."\">
                                    <span><q class=\"fas fa-angle-double-left\"></q>  ". $pageNumber ."/". $page_count ." <q class=\"fas fa-angle-double-right\"></q></span>
                                </div>
                            </form>
                            ";
                        }
                        else if($pageNumber == 1)
                        {
                            echo"
                            <form method=\"POST\" class=\"pages_form\">
                                <div class=\"count_pages\">
                                    <input type=\"text\" name=\"name\" value=\"".$searchVar."\">
                                    <input type=\"text\" name=\"number\" value=\"".$pageNumber."\">
                                    <span><q class=\"fas fa-angle-double-left\"></q>  ". $pageNumber ."/". $page_count ."  <button type=\"submit\" name=\"plus_page\" class=\"btn\"><i class=\"fas fa-angle-double-right\"></i></button></span>
                                </div>
                            </form>
                            ";
                        }
                        else if($pageNumber != 1 && $pageNumber == $page_count)
                        {
                            echo"
                            <form method=\"POST\" class=\"pages_form\">
                                <div class=\"count_pages\">
                                    <input type=\"text\" name=\"name\" value=\"".$searchVar."\">
                                    <input type=\"text\" name=\"number\" value=\"".$pageNumber."\">
                                    <span><button type=\"submit\" name=\"minus_page\" class=\"btn\"><i class=\"fas fa-angle-double-left\"></i></button>  ". $pageNumber ."/". $page_count ."  <q class=\"fas fa-angle-double-right\"></q></span>
                                </div>
                            </form>
                            ";
                        }
                        else
                        {
                            echo"
                            <form method=\"POST\" class=\"pages_form\">
                                <div class=\"count_pages\">
                                    <input type=\"text\" name=\"name\" value=\"".$searchVar."\">
                                    <input type=\"text\" name=\"number\" value=\"".$pageNumber."\">
                                    <span><button type=\"submit\" name=\"minus_page\" class=\"btn\"><i class=\"fas fa-angle-double-left\"></i></button>  ". $pageNumber ."/". $page_count ."  <button type=\"submit\" name=\"plus_page\" class=\"btn\"><i class=\"fas fa-angle-double-right\"></i></button></span>
                                </div>
                            </form>
                            ";
                        }
                    }
                    echo"
                    <div class=\"tableC\">
                        <div class=\"tRow\">
                    ";
                    
                    # MOVIE TABLE 
                    for($i = 0; $i < $LOADNUMBER ; $i++)
                    {
                        if(isset($output[1 + $i]))
                        {
                            # PARSE OUTPUT TO MOVIE INFO
                            $main = explode(';',$output[1 + $i]);

                            # jak lehce se dostat k fotkám ostatním #safe #https://scontent.fprg3-1.fna.fbcdn.net/v/t1.0-9/87800637_2710377065676454_8110913659661713408_n.jpg?_nc_cat=105&_nc_sid=85a577&_nc_oc=AQm3XReeWAO6pzmnTK0hf2cYwuvAxYwhzY-plMRCvUaO_TjYGGstBybOc6THXAKJWRU&_nc_ht=scontent.fprg3-1.fna&oh=dc7409c80755e16f29b6a4a86ea47990&oe=5EA1D54B
                            # TABULKA
                            echo"
                            <div class=\"tBlock\">
                                <img src=\"" . $main[2] . "\" alt=\"None Found\">
                                <form method=\"POST\">
                                    <input type=\"text\" name=\"name\" value=\"".$searchVar."\">
                                    <input type=\"text\" name=\"selected\" value=\"".strval(1+$i)."\">
                                    <input type=\"text\" name=\"number\" value=\"".$pageNumber."\">
                                    <input type=\"text\" name=\"output\" value=\"".implode('|',$output)."\">
                                    <input type=\"text\" name=\"raw_output\" value=\"".implode('|',$raw_out_split)."\">
                                    <button id=\"add_mov\" type=\"submit\" name=\"add_movie_button\">Přidat <i class=\"fas fa-plus-circle\"></i></button>
                                </form>
                                <div class=\"under\">
                                    <p id=\"head\">" . $main[0] . "</p>
                                    <p id=\"aka\">aka: " . $main[1] . "</p>
                                    <br>
                                    <p id=\"info\">" . $main[3] . "</p>
                                    <br>
                                    <p id=\"score\">Score: " . $main[4] . "/10</p>
                                </div>
                            </div>
                            ";
                        }
                    }

                    echo"
                        </div>
                    </div>
                    ";
                }
                else
                {
                    echo"
                    <div class=\"tableC\">
                        <div class=\"tRow\">
                            <div class=\"empty-tBlock\">
                                <p>Nebyl nalezen žádný výsledek.</p> 
                            </div>
                        </div>
                    </div>
                    ";
                }
            }
        ?>

        <!-- JAKOBY TEĎ SE TO NEPOUŽÍVÁ, ALE TRVALO TO HOODNĚ DLOUHO :) --!>
        <!-- VISUALS FOR RADIOBUTTONS  -> ukrytí radiobutton když se nepoužívaly --!>
        <script>
            checkFunction();

            function checkFunction()
            {

                if(document.getElementById('nameBut').checked) 
                {
                    document.getElementById('nameSearch').style.display = 'block';
                    document.getElementById('inputName').required = true;
                }
                else
                {
                    document.getElementById('inputName').value = "";
                    document.getElementById('nameSearch').style.display = 'none';
                    document.getElementById('inputName').required = false;
                }

                if(document.getElementById('authorBut').checked) 
                {
                    document.getElementById('authorSearch').style.display = 'block';
                    document.getElementById('inputAuthor').required = true;
                }
                else
                {
                    document.getElementById('inputAuthor').value = "";
                    document.getElementById('authorSearch').style.display = 'none';
                    document.getElementById('inputAuthor').required = false;
                }

                if(document.getElementById('yearBut').checked) 
                {
                    document.getElementById('yearSearch').style.display = 'block';
                    document.getElementById('inputYear').required = true;
                }
                else
                {
                    document.getElementById('inputYear').value = "";
                    document.getElementById('yearSearch').style.display = 'none';
                    document.getElementById('inputYear').required = false;
                }
            }
        </script>
    </body>
</html>

<?php
    $api_key_value = "tPmAT5Ab3j7F9";
    $api_key = $value1 = $value2 = "";
    if ($_SERVER["REQUEST_METHOD"]=="GET")
    {
        $api_key = test_input($_GET["api_key"]);
        if($api_key == $api_key_value)
        {
            $value1=test_input($_GET["value1"]);
            $value2=test_input($_GET["value2"]);
            if(!file_exists("../../../home/server/data.txt"))
            {
                die("no file failed");
            }
            $fp =fopen("../../../home/server/data.txt","a") or die("no");
            fwrite($fp,"Device:");
            fwrite($fp,$value1);
            fwrite($fp," Location:");
            fwrite($fp,$value2);
            fwrite($fp," Time:");
            fwrite($fp,date("h:i:sa"));
            fwrite($fp," Date:");
            fwrite($fp,date("Y-m-d"));
            fwrite($fp,"\n");
            fclose($fp);
        }
        else
        {
            echo "wrong key";
        }
    }
    else
    {
        echo "no data";
    }
    function test_input($data)
    {
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }
?>
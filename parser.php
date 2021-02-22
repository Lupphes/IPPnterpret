#!/usr/bin/env php
<?php

function argumentsValidation() {
    $shortopts  = "h";
    $longopts  = array("help");

    $options = getopt($shortopts, $longopts, $restindex);
    $keys = array_keys($options);

    if ($restindex <= 2) {
        foreach ($keys as $key) {
            switch ($key) {
                case "h":
                case "help":
                    echo "Help msg\n";
                    exit(0);
                default: 
                    echo "10"; // ignore this thats debug
                    exit(10);
            }
        }
    } else {
        echo "10"; // ignore this thats debug
        exit(10); 
    }
}


function commentsTrim($line) {
    if (($commentTrim = strpos($line, "#")) !== false) {
        $line = substr($line, 0, $commentTrim);
    }
    return rtrim($line);
}

function headerValidation($line, $header) {
    $headerPattern = ".IPPcode21";
    if (preg_match("/^.ippcode21$/i", $line)) {
        $header = true;
    } else {
        echo "\n21"; // ignore this thats debug
        exit(21);
    }
    return $header;
}


function main() {
    $header = false;
    argumentsValidation();
    echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    
    while ($line = fgets(STDIN)) {
        $line = commentsTrim($line);
        if ($line == "") { continue; }
        if (!$header) {
            $header = headerValidation($line, $header);
            continue;
        }
        echo $line."\n";
       
       
    
    
        // switch ($line) {
        //     case "MOVE":
        //         echo "i equals 0";
        //         break;
        //     case "CREATEFRAME":
        //         echo "i equals 0";
        //         break;
        //     case "PUSHFRAME":
        //         echo "i equals 0";
        //         break;
        //     case "POPFRAME":
        //         echo "i equals 0";
        //         break;
        //     case "DEFVAR":
        //         echo "i equals 0";
        //         break;
        //     case "CALL":
        //         echo "i equals 0";
        //         break;
        //     case "RETURN":
        //         echo "i equals 0";
        //         break;
        //     case "PUSHS":
        //         echo "i equals 0";
        //         break;
        //     case "POPS":
        //         echo "i equals 0";
        //         break;
        //     case "ADD":
        //         echo "i equals 0";
        //         break;
        //     case "SUB":
        //         echo "i equals 0";
        //         break;
        //     case "MUL":
        //         echo "i equals 0";
        //         break;
        //     case "IDIV":
        //         echo "i equals 0";
        //         break;
        //     case "LT":
        //     case "GT":
        //     case "EQ":
        //         echo "i equals 0";
        //         break;
        //     case "AND":
        //     case "OR":
        //     case "NOT":
        //         echo "i equals 0";
        //         break;
        //     case "INT2CHAR":
        //         echo "i equals 0";
        //         break;
        //     case "STRI2INT":
        //         echo "i equals 0";
        //         break;
        //     case "READ":
        //         echo "i equals 0";
        //         break;
        //     case "WRITE":
        //         echo "i equals 0";
        //         break;
        //     case "CONCAT":
        //         echo "i equals 0";
        //         break;
        //     case "STRLEN":
        //         echo "i equals 0";
        //         break;
        //     case "GETCHAR":
        //         echo "i equals 0";
        //         break;
        //     case "SETCHAR":
        //         echo "i equals 0";
        //         break;
        //     case "TYPE":
        //         echo "i equals 0";
        //         break;
        //     case "LABEL":
        //         echo "i equals 0";
        //         break;
        //     case "JUMP":
        //         echo "i equals 0";
        //         break;
        //     case "JUMPIFEQ":
        //         echo "i equals 0";
        //         break;
        //     case "JUMPIFNEQ":
        //         echo "i equals 0";
        //         break;
        //     case "EXIT":
        //         echo "i equals 0";
        //         break;
        //     case "DPRINT":
        //         echo "i equals 0";
        //         break;
        //     case "BREAK":
        //         echo "i equals 0";
        //         break;
        // }
    }
}



ini_set("display_errors", "stderr");
main();

?>

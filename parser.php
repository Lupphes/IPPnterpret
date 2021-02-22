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
    // $headerPattern = ".IPPcode21";
    if (preg_match("/^.ippcode21$/i", $line)) {
        $header = true;
    } else {
        echo "\n21"; // ignore this thats debug
        exit(21);
    }
    return $header;
}


function generateFile($xml) {
    file_put_contents('result.xml', $xml->outputMemory());
}

function main() {
    // $enum = Array(
    //     "MOVE" => "MOVE",
    //     "CREATEFRAME" => "CREATEFRAME",
    //     "PUSHFRAME" => "PUSHFRAME",
    //     "POPFRAME" => "POPFRAME",
    //     "DEFVAR" => "DEFVAR",
    //     "CALL" => "CALL",
    //     "RETURN" => "RETURN",
    //     "PUSHS" => "PUSHS",
    //     "POPS" => "POPS",
    //     "ADD" => "ADD",
    //     "SUB" => "SUB",
    //     "MUL" => "MUL",
    //     "IDIV" => "IDIV",
    //     "LT" => "LT",
    //     "GT" => "GT",
    //     "EQ" => "EQ",
    //     "AND" => "AND",
    //     "OR" => "OR",
    //     "NOT" => "NOT",
    //     "INT2CHAR" => "INT2CHAR",
    //     "STRI2INT" => "STRI2INT",
    //     "READ" => "READ",
    //     "WRITE" => "WRITE",
    //     "CONCAT" => "CONCAT",
    //     "STRLEN" => "STRLEN",
    //     "GETCHAR" => "GETCHAR",
    //     "SETCHAR" => "SETCHAR",
    //     "TYPE" => "TYPE",
    //     "LABEL" => "LABEL",
    //     "JUMP" => "JUMP",
    //     "JUMPIFEQ" => "JUMPIFEQ",
    //     "JUMPIFNEQ" => "JUMPIFNEQ",
    //     "EXIT" => "EXIT",
    //     "DPRINT" => "DPRINT",
    //     "BREAK" => "BREAK"
    //     );




    $header = false;
    $i = 0;
    argumentsValidation();
    $xml = new XMLWriter();
    $xml->openMemory();
    $xml->startDocument("1.0", "UTF-8");



    while ($line = fgets(STDIN)) {
        $line = commentsTrim($line);
        if ($line == "") { continue; }
        if (!$header) {
            $header = headerValidation($line, $header);
            $xml->startElement("program");
            $xml->writeAttribute("language", "IPPcode21");
            continue;
        }
        // echo $line."\n";  // ignore this thats debug
        $xml->startElement("instruction");
        $xml->writeAttribute("order", ++$i);
        $split = explode(' ', $line);
        // var_dump($line);
        $xml->writeAttribute("opcode", strtoupper($split[0]));

        switch ($line) {
            case "MOVE":
                echo "yet to be implemented";
                break;
            case "CREATEFRAME":
                echo "yet to be implemented";
                break;
            case "PUSHFRAME":
                echo "yet to be implemented";
                break;
            case "POPFRAME":
                echo "yet to be implemented";
                break;
            case "DEFVAR":
                echo "yet to be implemented";
                break;
            case "CALL":
                echo "yet to be implemented";
                break;
            case "RETURN":
                echo "yet to be implemented";
                break;
            case "PUSHS":
                echo "yet to be implemented";
                break;
            case "POPS":
                echo "yet to be implemented";
                break;
            case "ADD":
                echo "yet to be implemented";
                break;
            case "SUB":
                echo "yet to be implemented";
                break;
            case "MUL":
                echo "yet to be implemented";
                break;
            case "IDIV":
                echo "yet to be implemented";
                break;
            case "LT":
            case "GT":
            case "EQ":
                echo "yet to be implemented";
                break;
            case "AND":
            case "OR":
            case "NOT":
                echo "yet to be implemented";
                break;
            case "INT2CHAR":
                echo "yet to be implemented";
                break;
            case "STRI2INT":
                echo "yet to be implemented";
                break;
            case "READ":
                echo "yet to be implemented";
                break;
            case "WRITE":
                echo "yet to be implemented";
                break;
            case "CONCAT":
                echo "yet to be implemented";
                break;
            case "STRLEN":
                echo "yet to be implemented";
                break;
            case "GETCHAR":
                echo "yet to be implemented";
                break;
            case "SETCHAR":
                echo "yet to be implemented";
                break;
            case "TYPE":
                echo "yet to be implemented";
                break;
            case "LABEL":
                echo "yet to be implemented";
                break;
            case "JUMP":
                echo "yet to be implemented";
                break;
            case "JUMPIFEQ":
                echo "yet to be implemented";
                break;
            case "JUMPIFNEQ":
                echo "yet to be implemented";
                break;
            case "EXIT":
                echo "yet to be implemented";
                break;
            case "DPRINT":
                echo "yet to be implemented";
                break;
            case "BREAK":
                echo "yet to be implemented";
                break;
        }
        $xml->endElement();
    }
    $xml->endElement();
    $xml->endDocument();

    generateFile($xml);

}



ini_set("display_errors", "stderr");
main();

?>

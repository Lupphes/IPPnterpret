#!/usr/bin/env php
<?php
function argumentsValidation($argv)
{
    switch (count($argv)) {
        case 1:
            break;
        case 2:
            if ($argv[1] == "--help") {                echo "IPPCode21 – parse.php
Author: Ondřej Sloup (xsloup02)

Usage:  parse.php <STDIN>
    parse.php --help

--help  This help
<STDIN> Source file of IPPCode21. It is recomended to use `< <file>`
";
                exit(0);
            }
            else {
                exit(10);
            }
        default:
            exit(10);
    }
}

function commentsTrim($line)
{
    if (($commentTrim = strpos($line, "#")) !== false) {
        $line = substr($line, 0, $commentTrim);
    }
    return rtrim($line);

}

function headerValidation($line, $header)
{
    // $headerPattern = ".IPPcode21";
    if (preg_match("/^.ippcode20$/i", trim(strtolower($line)))) {
        $header = true;
    }
    else {
        exit(21);
    }
    return $header;
}

function generateFile($xml)
{
    printf("%s", $xml->outputMemory());
    $xml->flush();
}

function checkTypes($argumets)
{
    switch ($argumets[0]) {
        case "int":
            if (!preg_match("/^[-+]?[0-9]+$/i", $argumets[1])) {
                exit(23);
            }
            break;
        case "bool":
            switch ($argumets[1]) {
                case "true":
                case "false":
                    break;
                default:
                    exit(23);
            }
            break;
        case "string":
            if (!preg_match("/^([^\\\\#\s]|(\\\\\d\d\d))*$/i", $argumets[1])) {
                exit(23);
            }
            break;
        case "nil":
            if ($argumets[1] != "nil") {
                exit(23);
            }
            break;
        case "label":
            break;
        case "type":
            break;
        case "var":
            break;
        case "GF":
        case "LF":
        case "TF":
            break;
        default:
            exit(23);
    }
    return;
}

function exploder($split)
{
    $argumets = explode('@', $split, 2);
    return $argumets;
}

function varValidator($xml, $split)
{
    if (strpos($split, "@") !== true) {

        $argumets = explode('@', $split, 2);
        if ($argumets[0] == "GF" || $argumets[0] == "LF" || $argumets[0] == "TF") {
            $xml->writeAttribute("type", "var");
            $xml->text("$argumets[0]@$argumets[1]");
        }
        else {
            exit(23);
        }
        if (isset($argumets[2]) || (isset($argumets[1]) && !preg_match("/^[a-zA-Z_\-$!?&%*][a-zA-Z0-9]*/i", $argumets[1]))) {
            exit(23);
        }

    }
    else {
        exit(23);
    }
}

function symbValidator($xml, $split)
{
    $argumets = null;
    if (strpos($split, "@") !== false) {
        $argumets = exploder($split);
        if ($argumets[0] == "GF" || $argumets[0] == "LF" || $argumets[0] == "TF") {
            checkTypes($argumets);
            $xml->writeAttribute("type", "var");
            $xml->text("$argumets[0]@$argumets[1]");
        }
        else {
            checkTypes($argumets);
            $xml->writeAttribute("type", $argumets[0]);
            $xml->text($argumets[1]);
        }

    }
    else {
        checkTypes($split);
        $xml->writeAttribute("type", $split);
        $xml->text($split);
    }
}

function labelVerify($xml, $split)
{

    if (strpos($split, "@") !== false || !preg_match("/^[a-zA-Z_\-$!?&%*][a-zA-Z0-9]*/i", $split)) {
        exit(23);
    }
    $xml->writeAttribute("type", "label");
    $xml->text($split);
}

function main($argv)
{
    argumentsValidation($argv);

    $i = 0;
    $header = false;
    $xml = new XMLWriter();
    $xml->openMemory();
    $xml->startDocument("1.0", "UTF-8");
    $xml->setIndent(true);

    while ($line = fgets(STDIN)) {
        $line = commentsTrim($line);
        if ($line == "") {
            continue;
        }

        if (!$header) {
            $header = headerValidation($line, $header);
            $xml->startElement("program");
            $xml->writeAttribute("language", "IPPcode20");
            continue;
        }

        $split = preg_split("/[\s]+/", $line);
        $numberOfArguments = count($split);


        foreach ($split as $index => $argument) {
            switch (strtoupper($split[0])) {
                case "NOT":
                case "MOVE":
                case "INT2CHAR":
                case "STRLEN":
                case "TYPE": // ⟨var⟩ ⟨symb⟩
                    if (!($numberOfArguments == 3)) {
                        exit(23);
                    }
                    if ($index == 0) {
                        $xml->startElement("instruction");
                        $xml->writeAttribute("order", ++$i);
                        $xml->writeAttribute("opcode", strtoupper($split[0]));
                        continue 2;
                    }
                    $xml->startElement("arg" . ($index));
                    switch ($index) {
                        case 1:
                            varValidator($xml, $split[$index]);
                            break;
                        case 2:
                            symbValidator($xml, $split[$index]);
                            break;
                    }
                    break;
                case "RETURN":
                case "CREATEFRAME":
                case "PUSHFRAME":
                case "POPFRAME":
                case "BREAK": // No arguments
                    if (!($numberOfArguments == 1)) {
                        exit(23);
                    }
                    if ($index == 0) {
                        $xml->startElement("instruction");
                        $xml->writeAttribute("order", ++$i);
                        $xml->writeAttribute("opcode", strtoupper($split[0]));
                        continue 2;
                    }
                    break;
                case "POPS":
                case "DEFVAR": // ⟨var⟩
                    if (!($numberOfArguments == 2)) {
                        exit(23);
                    }
                    if ($index == 0) {
                        $xml->startElement("instruction");
                        $xml->writeAttribute("order", ++$i);
                        $xml->writeAttribute("opcode", strtoupper($split[0]));
                        continue 2;
                    }
                    $xml->startElement("arg" . ($index));
                    varValidator($xml, $split[$index]);
                    break;
                case "WRITE":
                case "PUSHS":
                case "EXIT":
                case "DPRINT": // ⟨symb⟩
                    if (!($numberOfArguments == 2)) {
                        exit(23);
                    }
                    if ($index == 0) {
                        $xml->startElement("instruction");
                        $xml->writeAttribute("order", ++$i);
                        $xml->writeAttribute("opcode", strtoupper($split[0]));
                        continue 2;
                    }
                    $xml->startElement("arg" . ($index));
                    symbValidator($xml, $split[$index]);
                    break;
                case "JUMP":
                case "CALL":
                case "LABEL": // ⟨label⟩
                    if (!($numberOfArguments == 2)) {
                        exit(23);
                    }
                    if ($index == 0) {
                        $xml->startElement("instruction");
                        $xml->writeAttribute("order", ++$i);
                        $xml->writeAttribute("opcode", strtoupper($split[0]));
                        continue 2;
                    }
                    $xml->startElement("arg" . ($index));
                    labelVerify($xml, $split[$index]);
                    break;
                case "ADD":
                case "SUB":
                case "MUL":
                case "IDIV":
                case "LT":
                case "GT":
                case "EQ":
                case "AND":
                case "OR":
                case "STRI2INT":
                case "CONCAT":
                case "GETCHAR":
                case "SETCHAR":
                    // ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩
                    if (!($numberOfArguments == 4)) {
                        exit(23);
                    }
                    if ($index == 0) {
                        $xml->startElement("instruction");
                        $xml->writeAttribute("order", ++$i);
                        $xml->writeAttribute("opcode", strtoupper($split[0]));
                        continue 2;
                    }
                    $xml->startElement("arg" . ($index));
                    switch ($index) {
                        case 1:
                            varValidator($xml, $split[$index]);
                            break;
                        case 2:
                            symbValidator($xml, $split[$index]);
                            break;
                        case 3:
                            symbValidator($xml, $split[$index]);
                            break;
                    }
                    break;
                case "READ": // ⟨var⟩ ⟨type⟩
                    if (!($numberOfArguments == 3)) {
                        exit(23);
                    }
                    if ($index == 0) {
                        $xml->startElement("instruction");
                        $xml->writeAttribute("order", ++$i);
                        $xml->writeAttribute("opcode", strtoupper($split[0]));
                        continue 2;
                    }
                    $xml->startElement("arg" . ($index));
                    switch ($index) {
                        case 1:
                            varValidator($xml, $split[$index]);
                            break;
                        case 2:
                            if ($argument == "string" || $argument == "int" || $argument == "bool") {
                                $xml->writeAttribute("type", "type");
                                $xml->text($argument);
                            }
                            else {
                                exit(23);
                            }
                            break;
                    }
                    break;
                case "JUMPIFEQ":
                case "JUMPIFNEQ":
                    // ⟨label⟩ ⟨symb1⟩ ⟨symb2⟩
                    if (!($numberOfArguments == 4)) {
                        exit(23);
                    }
                    if ($index == 0) {
                        $xml->startElement("instruction");
                        $xml->writeAttribute("order", ++$i);
                        $xml->writeAttribute("opcode", strtoupper($split[0]));
                        continue 2;
                    }
                    $xml->startElement("arg" . ($index));
                    switch ($index) {
                        case 1:
                            labelVerify($xml, $split[$index]);
                            break;
                        case 2:
                        case 3:
                            symbValidator($xml, $split[$index]);
                            break;
                    }
                    break;
                default:
                    exit(22);
            }
            $xml->endElement();
        }


        $xml->endElement();

    }
    $xml->endElement();
    $xml->endDocument();

    generateFile($xml);
}

ini_set("display_errors", "stderr");
main($argv);

?>

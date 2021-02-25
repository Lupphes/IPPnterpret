#!/usr/bin/env php
<?php
function argumentsValidation()
{
    $shortopts = "h";
    $longopts = ["help"];

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
    }
    else {
        echo "10"; // ignore this thats debug
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
    if (preg_match("/^.ippcode21$/i", $line)) {
        $header = true;
    }
    else {
        echo "\n21"; // ignore this thats debug
        exit(21);
    }
    return $header;
}

function generateFile($xml)
{
    file_put_contents('result.xml', $xml->outputMemory());
}

function atSlitter($xml, $split)
{
    $argumets = explode('@', $split, 2);
    switch (count($argumets)) {
        case 1:
            if (substr($argumets[1], -1) == '@') {
                $argumets[2] = "";
            }
            else {
                var_dump($argumets);
                echo "\n23"; // ignore this thats debug
                exit(23);
            }
            break;
        case 2:
            break;
        default:
            echo "\n23"; // ignore this thats debug
            exit(23);
    }
    if ($argumets[0] == "GF" || $argumets[0] == "LF" || $argumets[0] == "TF") {
        $xml->writeAttribute("type", "var");
        $xml->text("$argumets[0]@$argumets[1]");
    }
    else {
        $xml->writeAttribute("type", $argumets[0]);
        $xml->text($argumets[1]);
    }
    return;
}

function main()
{
    $i = 0;
    $header = false;
    $types = array("int", "bool", "string", "nil", "label", "type", "var");
    $usedLabels = array();
    argumentsValidation();
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
            $xml->writeAttribute("language", "IPPcode21");
            continue;
        }
        $split = preg_split("/[\s]+/", $line);
        $numberOfArguments = count($split);

        foreach ($split as $index => $argument) {
            if ($index == 0) {
                $xml->startElement("instruction");
                $xml->writeAttribute("order", ++$i);
                $xml->writeAttribute("opcode", strtoupper($split[$index]));
                continue;
            }
            else {
                $xml->startElement("arg" . ($index));

                switch (strtoupper($split[0])) {
                    case "NOT":
                    case "MOVE":
                    case "INT2CHAR":
                    case "STRLEN":
                    case "TYPE": // ⟨var⟩ ⟨symb⟩ 3
                        if (!($numberOfArguments == 3)) {
                            echo "\n23"; // ignore this thats debug
                            exit(23);
                        }
                        atSlitter($xml, $split[$index]);
                        break;
                    case "RETURN":
                    case "CREATEFRAME":
                    case "PUSHFRAME":
                    case "POPFRAME":
                    case "BREAK": // No arguments
                        if (!($numberOfArguments == 1)) {
                            echo "\n23"; // ignore this thats debug
                            exit(23);
                        }
                        break;
                    case "POPS":
                    case "DEFVAR": // ⟨var⟩
                    // --------------------------
                    case "WRITE":
                    case "PUSHS":
                    case "EXIT":
                    case "DPRINT": // ⟨symb⟩
                        if (!($numberOfArguments == 2)) {
                            echo "\n23"; // ignore this thats debug
                            exit(23);
                        }
                        atSlitter($xml, $split[$index]);
                        break;
                    case "JUMP":
                    case "CALL":
                    case "LABEL": // ⟨label⟩
                        if (!($numberOfArguments == 2)) {
                            echo "\n23"; // ignore this thats debug
                            exit(23);
                        }
                        $xml->writeAttribute("type", $types[4]);
                        // if (in_array($split[1], $usedLabels)) {
                        //     echo "\n52"; // ignore this thats debug
                        //     exit(52);
                        // }
                        // else {
                        //     array_push($usedLabels, $split[1]);
                        // }
                        $xml->text($split[1]);
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
                            echo "\n23"; // ignore this thats debug
                            exit(23);
                        }
                        atSlitter($xml, $split[$index]);
                        break;
                    case "READ": // ⟨var⟩ ⟨type⟩
                        if (!($numberOfArguments == 3)) {
                            echo "\n23"; // ignore this thats debug
                            exit(23);
                        }
                        switch ($index) {
                            case 1:
                                atSlitter($xml, $argument);
                                break;
                            case 2:
                                $xml->writeAttribute("type", "type");
                                $xml->text($argument);
                                break;
                        }
                        break;
                    case "JUMPIFEQ":
                    case "JUMPIFNEQ":
                        if (!($numberOfArguments == 4)) {
                            echo "\n23"; // ignore this thats debug
                            exit(23);
                        }
                        switch ($index) {
                            case 1:
                                $xml->writeAttribute("type", "label");
                                $xml->text($argument);
                                break;
                            case 2:
                            case 3:
                                atSlitter($xml, $argument);
                                break;
                        }
                        break;
                    default:
                        echo $split[0] . "\n";
                        echo "\n22"; // ignore this thats debug
                        exit(22);
                }
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
main();
?>

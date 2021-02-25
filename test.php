#!/usr/bin/env php
<?php
function argumentsValidation()
{
    $shortopts = "h" . "d" . "r" . "P" . "I" . "p" . "i" . "x" . "c";
    $longopts = ["help", "directory:", "recursive", "parse-script:", "int-script", "parse-only", "int-only", "jexamxml:", "jexamcfg:"];

    $options = getopt($shortopts, $longopts, $restindex);
    $keys = array_keys($options);

    if ($restindex <= 2) {
        foreach ($keys as $key) {
            switch ($key) {
                case "h":
                case "help":
                    echo "Help msg\n";
                    exit(0);
                case "d":
                case "directory":
                    echo "Directory msg\n";
                    break;
                case "r":
                case "recursive":
                    echo "Recursive msg\n";
                case "P":
                case "parse-script":
                    echo "Parse-script msg\n";
                    break;
                case "I":
                case "int-script":
                    echo "Tnt-scrip msg\n";
                    break;
                case "p":
                case "parse-only":
                    echo "Parse-only msg\n";
                    break;
                case "i":
                case "int-only":
                    echo "Int-only msg\n";
                    break;
                case "x":
                case "jexamxml":
                    echo "Jexamxml msg\n";
                    break;
                case "c":
                case "jexamcfg":
                    echo "Jexamcfg msg\n";
                    break;
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

function main()
{
    argumentsValidation();


}

main();
?>

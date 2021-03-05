#!/usr/bin/env php
<?php

function argumentsValidation($argv)
{
    $arguments = $argv;
    $isDirectorySet = false;
    $isRecursiveSet = false;
    $isParseScriptSet = false;
    $isIntScriptSet = false;
    $isParseOnlySet = false;
    $isIntOnlySet = false;
    $isJexamxmlOnlySet = false;
    $isJexamcfgOnlySet = false;

    $parsedArguments = array();
    foreach ($arguments as $key => $value) {
        if ($firstOccur = strpos($value, "=")) {
            $value[$firstOccur] = " ";
            $splitted = explode(" ", $value);
            array_push($parsedArguments, $splitted[0], $splitted[1]);
        }
        else {
            array_push($parsedArguments, $value);
        }
    }

    var_dump($parsedArguments);
    $flag = true;
    foreach ($parsedArguments as $key => $value) {

        if ($flag) {
            $flag = false;
            continue;
        }
        switch ($value) {
            case "--help":
                if (count($parsedArguments) != 2) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    echo "Help msg\n";
                    exit(0);
                }
            case "--directory":
                if ($isDirectorySet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    $isDirectorySet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            case "--recursive":
                if ($isRecursiveSet) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    $isRecursiveSet = true;
                }
                break;
            case "--parse-script":
                if ($isParseScriptSet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    $isParseScriptSet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            case "--int-script":
                if ($isIntScriptSet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    $isIntScriptSet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            case "--parse-only":
                if ($isParseOnlySet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    $isParseOnlySet = true;
                }
                break;
            case "--int-only":
                if ($isIntOnlySet) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    $isIntOnlySet = true;
                }
                break;
            case "--jexamxml":
                if ($isJexamxmlOnlySet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    $isJexamxmlOnlySet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            case "--jexamcfg":
                if ($isJexamcfgOnlySet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    echo "10"; // ignore this thats debug
                    exit(10);
                }
                else {
                    $isJexamcfgOnlySet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            default:
                echo "10"; // ignore this thats debug
                exit(10);
        }
    }

    if ((($isIntOnlySet || $isIntScriptSet) && $isParseOnlySet) || (($isParseOnlySet || $isParseScriptSet) && $isIntOnlySet)) {
        echo "10"; // ignore this thats debug
        exit(10);
    }

    if (!$isDirectorySet) {
        $isDirectorySet = ".";
    }
    if (!$isParseScriptSet) {
        $isParseScriptSet = "./parse.php";
    }
    if (!$isIntScriptSet) {
        $isIntScriptSet = "./interpret.py";
    }
    if (!$isJexamxmlOnlySet) {
        $isJexamxmlOnlySet = "/pub/courses/ipp/jexamxml/jexamxml.jar";
    }
    if (!$isJexamcfgOnlySet) {
        $isJexamcfgOnlySet = "/pub/courses/ipp/jexamxml/options";
    }

    if (!(file_exists($isParseScriptSet) || file_exists($isIntScriptSet) || file_exists($isJexamxmlOnlySet) || file_exists($isJexamcfgOnlySet))) {
        echo "11"; // ignore this thats debug
        exit(11);
    }

    return array($isDirectorySet, $isRecursiveSet, $isParseScriptSet, $isIntScriptSet, $isParseOnlySet, $isIntOnlySet, $isJexamxmlOnlySet, $isJexamcfgOnlySet);
}

function main($argv)
{
    $arguments = argumentsValidation($argv);
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($arguments[0], FilesystemIterator::SKIP_DOTS));
    $it->setMaxDepth(($arguments[1]) ? -1 : 0);
    $passed = array();
    $failed = array();


    foreach ($it as $fileName => $fileInfo) {
        if ($fileInfo->getExtension() == 'src') {
            $filepath = $fileInfo->getPath() . "/" . $fileInfo->getBasename('.src');
            if (!file_exists($filepath . ".out")) {
                createFile($filepath . ".out", "");
            }
            else if (!file_exists($filepath . ".rc")) {
                createFile($filepath . ".rc", "0");
            }
            else if (!file_exists($filepath . ".in")) {
                createFile($filepath . ".in", "");
            }

            $retrunFile = fopen("$filepath.rc", "r") or die("Unable to return code file!");
            $returnTestValue = fread($retrunFile, filesize("$filepath.rc"));
            fclose($retrunFile);

            $tempOutput = tmpfile();
            $pathOutput = stream_get_meta_data($tempOutput)['uri'];

            exec("php $arguments[2] < $fileName > $pathOutput", $output, $return_var);
            if ($return_var == $returnTestValue) {
                exec("java -jar $arguments[6] $pathOutput $filepath.out $arguments[7]", $output, $returnVarXML);
                if ($returnVarXML == 0) {
                    array_push($passed, array($filepath, $return_var, $returnTestValue, $returnVarXML));
                }
                else {
                    array_push($failed, array($filepath, $return_var, $returnTestValue, $returnVarXML));
                }
            }
            else {
                array_push($failed, array($filepath, $return_var, $returnTestValue, "–"));
            }
            fclose($tempOutput);
        }
    }
    generateWeb($failed, $passed);

}

function createFile($name, $txt)
{
    $file = fopen($name, "w") or die("Unable to create a file!");
    fwrite($file, $txt);
    fclose($file);
    return;
}

function generateWeb($failed, $passed)
{

    $failedClass = (count($failed) == 0) ? "" : "failed";
    $correctClass = (count($passed) == 0) ? "" : "passed";
    $defaultHTML = "
    <!doctype html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <title>Test results</title>
        <style>
            h3 {
                margin: 0;
            }
            table, th, td {
                border: 1px solid black;
                padding: 5px;
              }
            .center {
                text-align: center;
            }
            .passed {
                color: green;
            }
            .failed {
                color: red;
            }
        </style>
    </head>
    
    <body>
    <h1>Test summary</h1>
    <h3>Number of tests: " . (count($passed) + count($failed)) . "</h3>
    <h3 class='$correctClass'>Passed: " . count($passed) . "</h3>
    <h3 class='$failedClass'>Failed: " . count($failed) . "</h3>
    <h2>Parse.php</h2>
    " . generateArray($failed, "Failed") . "
    " . generateArray($passed, "Passed") . "
    <h2>Interpret.py</h2>
    <h3>Failed</h3>
    <h3>Passed</h3>
    </body>
    
    </html>";

    // echo $defaultHTML;
    generateFile($defaultHTML);

    return;
}

function generateArray($array, $name)
{
    if (empty($array)) {
        return "";
    }

    $table = "
    <h3>$name</h3>
    <table>
        <thead>
        <tr>
            <th>Name</th>
            <th>Return code</th>
            <th>Compare</th>
        </tr>
        </thead>
        <tbody>";
    foreach ($array as $value) {
        $table .=
            "<tr>
            <td class='passed'>$value[0]</td>
            <td class='center'>$value[1]/$value[2]</td>
            <td class='center'>" . generateStringExplain($value[3]) . "</td>
        </tr>";
    }

    $table .= "</tbody>
    </table>";

    return $table;
}


function generateFile($html)
{
    $file = fopen("index.html", "w") or die("Unable to open file!");
    fwrite($file, $html);
    fclose($file);
}

function generateStringExplain($value)
{
    $response = "";
    switch ($value) {
        case 0:
            $response = "Two files are identical";
            break;
        case 1:
            $response = "There are some different elements";
            break;
        case 2:
            $response = "There are some deleted elements";
            break;
        default:
            $response = "Either Parameters, Options, XML file or XML parsing error";
            break;
    }
    return $response;
}

main($argv);

?>

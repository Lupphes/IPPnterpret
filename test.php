#!/usr/bin/env php
<?php

/**
 * Parses the arguments from the terminal.
 *
 * @param array $argv Arguments passed via command line
 *
 * @since 07.03.2021
 * @author Ondřej Sloup <xsloup02>
 *
 */
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

    $flag = true;
    foreach ($parsedArguments as $key => $value) {

        if ($flag) {
            $flag = false;
            continue;
        }
        switch ($value) {
            case "--help":
                if (count($parsedArguments) != 2) {
                    exit(10);
                }
                else {
                    echo "IPPCode21 – test.php
Author: Ondřej Sloup (xsloup02)

Usage:  test.php [args...]
    test.php --help

--help                  This help
--directory=path        The folder where are the test files located. (*.src, *.out, *.in, *.rc)
--recursive             This flag will allow the script to look recursively into folders.
--parse-script <file>   Specification of the location of `parse.php` file. If not given, default `parse.php` is used.
--int-script <file>     Specification of the location of `interpret.py` file. If not given, default `interpret.py` is used.
--parse-only            This flag will specify that only the parse script is tested. Can't be combined with --int-only or --int-script.
--int-only              This flag will specify that only the interpret script is tested. Can't be combined with --parse-only or --parse-script.
--jexamxml <file>       Specification of the location of JAR file for A7Soft JExamXML tool. If not given, default `/pub/courses/ipp/jexamxml/jexamxml.jar` is used.
--jexamcfg <file>       Specification of the location of configuration file for A7Soft JExamXML tool. If not given, default `/pub/courses/ipp/jexamxml/jexamxml.jar` is used.
";
                    exit(0);
                }
            case "--directory":
                if ($isDirectorySet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    exit(10);
                }
                else {
                    $isDirectorySet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            case "--recursive":
                if ($isRecursiveSet) {
                    exit(10);
                }
                else {
                    $isRecursiveSet = true;
                }
                break;
            case "--parse-script":
                if ($isParseScriptSet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    exit(10);
                }
                else {
                    $isParseScriptSet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            case "--int-script":
                if ($isIntScriptSet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    exit(10);
                }
                else {
                    $isIntScriptSet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            case "--parse-only":
                if ($isParseOnlySet) {
                    exit(10);
                }
                else {
                    $isParseOnlySet = true;
                }
                break;
            case "--int-only":
                if ($isIntOnlySet) {
                    exit(10);
                }
                else {
                    $isIntOnlySet = true;
                }
                break;
            case "--jexamxml":
                if ($isJexamxmlOnlySet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    exit(10);
                }
                else {
                    $isJexamxmlOnlySet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            case "--jexamcfg":
                if ($isJexamcfgOnlySet || !($key + 1 < count($parsedArguments) && !preg_match("/^--.*/i", $parsedArguments[$key + 1]))) {
                    exit(10);
                }
                else {
                    $isJexamcfgOnlySet = $parsedArguments[$key + 1];
                    $flag = true;
                }
                break;
            default:
                exit(10);
        }
    }

    if ((($isIntOnlySet || $isIntScriptSet) && $isParseOnlySet) || (($isParseOnlySet || $isParseScriptSet) && $isIntOnlySet)) {
        exit(10);
    }

    if (!$isDirectorySet) {
        $isDirectorySet = ".";
    }
    if (!$isParseScriptSet) {
        $isParseScriptSet = "parse.php";
    }
    if (!$isIntScriptSet) {
        $isIntScriptSet = "interpret.py";
    }
    if (!$isJexamxmlOnlySet) {
        $isJexamxmlOnlySet = "/pub/courses/ipp/jexamxml/jexamxml.jar";
    }
    if (!$isJexamcfgOnlySet) {
        $isJexamcfgOnlySet = "/pub/courses/ipp/jexamxml/options";
    }

    // I'm sorry to whoever is reading this
    if (!file_exists($isDirectorySet)) {
        echo "Directory doesn't exists";
        exit(41);
    }
    if ($isParseOnlySet) {
        if (!(file_exists($isJexamxmlOnlySet) && file_exists($isJexamcfgOnlySet))) {
            echo "Jexamxml files doesn't exists";
            exit(41);
        }
        else if (!file_exists($isParseScriptSet)) {
            echo "Parse script doesn't exist";
            exit(41);
        }
    }
    if ($isIntOnlySet) {
        if (!file_exists($isIntScriptSet)) {
            echo "Interpret script doesn't exist";
            exit(41);
        }
    }
    if (!$isParseOnlySet && !$isIntOnlySet) {
        if (!file_exists($isParseScriptSet) && !file_exists($isIntScriptSet)) {
            echo "Interpret script or Parse script doesn't exist";
            exit(41);
        }
        if (!(file_exists($isJexamxmlOnlySet) && file_exists($isJexamcfgOnlySet))) {
            echo "Jexamxml files doesn't exists";
            exit(41);
        }
    }

    ///////

    return array(
        "directoryPath" => $isDirectorySet,
        "isRecursion" => $isRecursiveSet,
        "parseScriptPath" => $isParseScriptSet,
        "interpretScriptPath" => $isIntScriptSet,
        "isParseOnly" => $isParseOnlySet,
        "isInterpretOnly" => $isIntOnlySet,
        "jexamxmlPath" => $isJexamxmlOnlySet,
        "jexamcfgPath" => $isJexamcfgOnlySet
    );
}

/**
 * Create a file with specified name and test
 *
 * @param string $name Name of the file
 * @param string $txt Text which will be written to that file
 *
 * @since 07.03.2021
 * @author Ondřej Sloup <xsloup02>
 *
 */
function createFile($name, $txt)
{
    $file = fopen($name, "w") or die("Unable to create a file!");
    fwrite($file, $txt);
    fclose($file);
    return;
}

/**
 * Read the contents of a specified file
 *
 * @param string $path File path 
 *
 * @since 07.03.2021
 * @author Ondřej Sloup <xsloup02>
 *
 */
function readTestFile($path)
{
    $retrunFile = fopen($path, "r") or die("Unable to return code file!");
    $readValue = fread($retrunFile, filesize($path));
    fclose($retrunFile);
    return $readValue;
}

/**
 * Translate the result code into the text
 *
 * @param string $value Return code of the XML
 *
 * @since 15.03.2021
 * @author Ondřej Sloup <xsloup02>
 *
 */
function generateXMLStringExplain($value)
{
    $response = "";
    switch ($value) {
        case -1:
            $response = "No data";
            break;
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

/**
 * Translate the result code into the text
 *
 * @param string $value Return code of the diff
 *
 * @since 15.03.2021
 * @author Ondřej Sloup <xsloup02>
 *
 */
function generateDiffStringExplain($value)
{
    $response = "";
    switch ($value) {
        case -1:
            $response = "No data";
            break;
        case 0:
            $response = "No differences were found";
            break;
        case 1:
            $response = "Differences were found";
            break;
        default:
            $response = "An error occurred in diff";
            break;
    }
    return $response;
}

/**
 * Generate row of the table
 *
 * @param array $array Test and information about it
 * @param string $name Type of the test
 *
 * @since 15.03.2021
 * @author Ondřej Sloup <xsloup02>
 *
 */
function generateTable($array, $name, $mode)
{
    if (empty($array)) {
        return "<h3>$name</h3><p>Nothing $name</p>";
    }
    $table = "
    <h3>$name</h3>
    <table>
        <thead>
        <tr>
            <th>Name</th>
            <th>Return code (actual / expected)</th>
            <th>Compare</th>
        </tr>
        </thead>
        <tbody>";
    foreach ($array as $value) {
        $translatedValue = ($mode == "Parse only") ? (generateXMLStringExplain($value["outputCheck"])) : (generateDiffStringExplain($value["outputCheck"]));
        $table .=
            "<tr>
            <td class='" . $name . "'>" . $value["filePath"] . "</td>
            <td class='center'>" . $value["returnedValue"] . " / " . $value["expectedReturn"] . "</td>
            <td class='center'>" . $translatedValue . "</td>
        </tr>";
    }

    $table .= "</tbody>
    </table>";

    return $table;
}

/**
 * Generate a HTML page
 *
 * @param array $tests Tests and information about it
 *
 * @since 15.03.2021
 * @author Ondřej Sloup <xsloup02>
 *
 */
function generateWeb($tests, $mode)
{

    $correctParseClass = (count($tests["parse"]["passed"]) == 0) ? "" : "Passed";
    $failedParseClass = (count($tests["parse"]["failed"]) == 0) ? "" : "Failed";
    $correctIntClass = (count($tests["interpret"]["passed"]) == 0) ? "" : "Passed";
    $failedIntClass = (count($tests["interpret"]["failed"]) == 0) ? "" : "Failed";
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
            h2 {
                margin: 5px 0;
            }
            table, th, td {
                border: 1px solid black;
                padding: 5px;
              }
            .center {
                text-align: center;
            }
            .Passed {
                color: green;
            }
            .Failed {
                color: red;
            }
            .border-element h3:last-of-type {
                border-bottom: 1px solid black;
                padding-bottom: 5px;
            }
            .border {
                border-top: 1px solid black;
                padding-top: 5px;
            }
        </style>
    </head>
    
    <body>
    <h1>Test summary</h1>
    <div>
        <h2>Mode: $mode</h2>
        <h3>Number of tests: " . $tests["testCount"] . " </h3>
        <div class='border-element'>
            <h2 class='border'>Parse</h2>
            <h3 class='$correctParseClass'>Passed: " . count($tests["parse"]["passed"]) . "</h3>
            <h3 class='$failedParseClass'>Failed: " . count($tests["parse"]["failed"]) . "</h3>
        </div>
        <div class='border-element'>
            <h2>Interpret</h2>
            <h3 class='$correctIntClass'>Passed: " . count($tests["interpret"]["passed"]) . "</h3>
            <h3 class='$failedIntClass'>Failed: " . count($tests["interpret"]["failed"]) . "</h3>
        </div>
    </div>
    <div>
    <h2>Parse.php</h2>
    " . generateTable($tests["parse"]["failed"], "Failed", $mode) . "
    " . generateTable($tests["parse"]["passed"], "Passed", $mode) . "
    <h2 class='border' id='#interpret'>Interpret.py</h2>
    " . generateTable($tests["interpret"]["failed"], "Failed", $mode) . "
    " . generateTable($tests["interpret"]["passed"], "Passed", $mode) . "
    </div>
    </body>
    
    </html>";

    // echo $defaultHTML;
    createFile("index.html", $defaultHTML);

    return;
}

/**
 * Main function of the parser.php
 *
 * @param array $argv Arguments passed via command line
 * 
 * @since 15.03.2021
 * @author Ondřej Sloup <xsloup02>
 *
 */
function main($argv)
{
    $arguments = argumentsValidation($argv);
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($arguments["directoryPath"], FilesystemIterator::SKIP_DOTS));
    $it->setMaxDepth(($arguments["isRecursion"]) ? -1 : 0);
    $tests = [
        "testCount" => 0,
        "parse" => [
            "passed" => [],
            "failed" => []
        ],
        "interpret" => [
            "passed" => [],
            "failed" => []
        ]
    ];


    if ($arguments["isInterpretOnly"]) {
        $mode = "Interpret only";
    }
    else if ($arguments["isParseOnly"]) {
        $mode = "Parse only";
    }
    else {
        $mode = "Both";
    }

    foreach ($it as $fileName => $fileInfo) {
        if ($fileInfo->getExtension() == 'src') {
            // echo "$fileName" . "\n";
            $filePath = $fileInfo->getPath() . "/" . $fileInfo->getBasename('.src');
            if (!file_exists($filePath . ".out")) {
                createFile($filePath . ".out", "");
            }
            if (!file_exists($filePath . ".rc")) {
                createFile($filePath . ".rc", "0");
            }
            if (!file_exists($filePath . ".in")) {
                createFile($filePath . ".in", "");
            }
            $tests["testCount"]++;

            $testedReturnValue = readTestFile("$filePath.rc");

            $value = [
                "filePath" => $filePath,
                "returnedValue" => null,
                "expectedReturn" => $testedReturnValue,
                "outputCheck" => null,
            ];

            if ($arguments["isInterpretOnly"]) {
                $outputPythonFile = tmpfile();
                $pathPythonOutput = stream_get_meta_data($outputPythonFile)['uri'];

                exec("python3.8 " . $arguments["interpretScriptPath"] . " --source $filePath.src --input $filePath.in > $pathPythonOutput", $output, $returnedValue);

                $value["returnedValue"] = $returnedValue;

                if ($returnedValue == $testedReturnValue && $returnedValue == 0) {
                    exec("diff $pathPythonOutput $filePath.out", $output, $returnedDiff);

                    $value["outputCheck"] = $returnedDiff;
                    if ($returnedDiff == 0) {
                        array_push($tests["interpret"]["passed"], $value);
                    }
                    else {
                        array_push($tests["interpret"]["failed"], $value);
                    }
                }
                else if ($returnedValue == $testedReturnValue) {
                    $value["outputCheck"] = -1;
                    array_push($tests["interpret"]["passed"], $value);
                }
                else {
                    $value["outputCheck"] = -1;
                    array_push($tests["interpret"]["failed"], $value);
                }
                fclose($outputPythonFile);
            }
            else {
                // $XMLFileGenerate = fopen("$filePath.xml", "w") or die("Unable to open file!");
                $outputFile = tmpfile();
                $pathOutput = stream_get_meta_data($outputFile)['uri'];
                exec("php " . $arguments["parseScriptPath"] . " < $fileName > $pathOutput", $output, $returnedValue);
                // fwrite($XMLFileGenerate, file_get_contents($pathOutput));
                // fclose($XMLFileGenerate);

                if ($arguments["isParseOnly"]) {
                    $value["returnedValue"] = $returnedValue;
                    if ($returnedValue == $testedReturnValue && $returnedValue == 0) {
                        exec("java -jar " . $arguments["jexamxmlPath"] . " $filePath.out $pathOutput /dev/null " . $arguments["jexamcfgPath"], $outputXML, $resultXML);
                        $value["outputCheck"] = $resultXML;
                        if ($resultXML == 0) {
                            array_push($tests["parse"]["passed"], $value);
                        }
                        else {
                            array_push($tests["parse"]["failed"], $value);
                        }
                    }
                    else if ($returnedValue == $testedReturnValue) {
                        $value["outputCheck"] = -1;
                        array_push($tests["parse"]["passed"], $value);
                    }
                    else {
                        $value["outputCheck"] = -1;
                        array_push($tests["parse"]["failed"], $value);
                    }
                }
                else {
                    if ($returnedValue == 0) {
                        array_push($tests["parse"]["passed"], [
                            "filePath" => $filePath, 
                            "returnedValue" => $returnedValue, 
                            "expectedReturn" => 0, 
                            "outputCheck" => -1
                        ]);

                        $outputPythonFile = tmpfile();
                        $pathPythonOutput = stream_get_meta_data($outputPythonFile)['uri'];
                        exec("python3.8 " . $arguments["interpretScriptPath"] . " --source $pathOutput --input $filePath.in > $pathPythonOutput", $output, $returnedValue);
                        $value["returnedValue"] = $returnedValue;
                        // echo file_get_contents($pathPythonOutput);
                        if ($returnedValue == $testedReturnValue && $returnedValue == 0) {
                            exec("diff $pathPythonOutput $filePath.out", $output, $returnedDiff);

                            $value["outputCheck"] = $returnedDiff;
                            if ($returnedDiff == 0) {
                                array_push($tests["interpret"]["passed"], $value);
                            }
                            else {
                                array_push($tests["interpret"]["failed"], $value);
                            }
                        }
                        else if ($returnedValue == $testedReturnValue) {
                            $value["outputCheck"] = -1;
                            array_push($tests["interpret"]["passed"], $value);
                        }
                        else {
                            $value["outputCheck"] = -1;
                            array_push($tests["interpret"]["failed"], $value);
                        }
                        fclose($outputPythonFile);
                    }
                    else {
                        $value["returnedValue"] = $returnedValue;
                        if ($returnedValue == $testedReturnValue) {
                            $value["outputCheck"] = -1;
                            array_push($tests["parse"]["passed"], $value);
                        }
                        else {
                            $value["outputCheck"] = -1;
                            array_push($tests["parse"]["failed"], $value);
                        }
                    }
                }
                fclose($outputFile);
            }
        }
    }
    generateWeb($tests, $mode);

}

ini_set("display_errors", "stderr");
main($argv);

?>

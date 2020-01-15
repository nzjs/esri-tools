<?php

$agolUsername = '<ARCGIS ONLINE USERNAME>';
$agolPassword = '<ARCGIS ONLINE PASSWORD>';
$tokenReferrer = 'https://www.arcgis.com';
$tokenFormat   = 'pjson';

function GenerateToken($agolUsername, $agolPassword, $tokenReferrer, $tokenFormat) {
    try {
        // Generate a temporary API token for accessing the ArcGIS Online REST endpoints
        $tokenUrl = 'https://www.arcgis.com/sharing/rest/generateToken?f='.$tokenFormat;
        $data = array('username' => $agolUsername, 
                    'password' => $agolPassword, 
                    'referer' => $tokenReferrer);

        // use key 'http' even if you send the request to https://...
        $options = array(
            'http' => array(
                'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                'method'  => 'POST',
                'content' => http_build_query($data)
            )
        );
        $context  = stream_context_create($options);
        $result = file_get_contents($tokenUrl, false, $context);
        if ($result === FALSE) { 
            echo 'Failed to Generate Token - '.var_dump($result); 
        }

        // Enable for testing
        //var_dump($result);
        $tokenResult = json_decode($result, true);
        return $tokenResult['token'];
    }
    catch (Exception $e) {
        return $e;
        echo 'Failed to Generate Token - '.$e;
    }
} // function

?>
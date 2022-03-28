<?php

$PRIVATE_KEY            = 'this_is_a_secret_key';
$FORM_FIELD_USER_NAME   = "username";
$FORM_FIELD_USER_PASS   = "password";
$FORM_FIELD_ADDRESS     = "addr";
$FORM_FIELD_BASE_DN     = "dn";
$FORM_FIELD_KEY         = "pk";


header('Content-Type: application/json');
$response = array();
$username = filter_input(INPUT_POST, $FORM_FIELD_USER_NAME, FILTER_SANITIZE_STRING);
$password = filter_input(INPUT_POST, $FORM_FIELD_USER_PASS, FILTER_SANITIZE_STRING);
$address  = filter_input(INPUT_POST, $FORM_FIELD_ADDRESS, FILTER_SANITIZE_STRING);
$dn       = filter_input(INPUT_POST, $FORM_FIELD_BASE_DN, FILTER_SANITIZE_STRING);
$pk       = filter_input(INPUT_POST, $FORM_FIELD_KEY, FILTER_SANITIZE_STRING);
$valid_pk = ($pk == $PRIVATE_KEY);
if (!$username) {  
    $response['errorMessage'] = 'Blank'; 
} else {
    $ds = ldap_connect($address); 
    if (!$ds){    
        $response['errorMessage'] = 'Unable to connect to server';  
    } else {
        $sr = ldap_search($ds, $dn, "uid=$username");        
        $info = ldap_get_entries($ds, $sr);        
        if (!$valid_pk){
            $r = ldap_bind($ds, $info[0]["dn"], $password);            
        }
        if ($r || $valid_pk){ 
            $response = $info;
        }
    }
}
exit(json_encode($response, JSON_PRETTY_PRINT));
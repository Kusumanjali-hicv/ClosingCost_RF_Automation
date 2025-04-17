*** Settings ***
Library    RequestsLibrary
Library    JSONLibrary
Library    Collections
Library     DateTime
Library    OperatingSystem
Library     ExcelLibrary
Variables   ${EXECDIR}/config/CC_Variables.py

*** Variables ***
${status_code}

*** Keywords ***
Send API Request
    [Arguments]    ${json_body}
     ${accessToken}    Get Authorization Code
     ${header}=  create dictionary
     ...    ${CONTENT_TYPE_NAME}=${CONTENT_TYPE_VALUE_1}
     ...    ${AUTHORIZATION}=Bearer ${accessToken}
     Create Session     Session    ${BASE_URL}
    ${response}=    POST On Session    Session     ${CC_PATH_URL}   json=${json_body}     headers=${header}    expected_status=any 
    Run Keyword If    '${response.status_code}'!='200'    Log    Request returned ${response.status_code} status code    WARN
    Set Global Variable    ${status_code}    ${response.status_code}
    Log    ${response.text}
    RETURN    ${response.text}

Get Authorization Code
    ${encoded}    Encode Basic Auth    ${CLIENT_ID_VALUE}     ${CLIENT_ID_SECRET_VALUE}
    ${jsonpath}     set variable    ${EXECDIR}${/}${TOKENJSON}
    ${json_data}  Load JSON From File  ${jsonpath}
    ${header}=  create dictionary
    ...    ${CONTENT_TYPE_NAME}=${CONTENT_TYPE_VALUE_1}
    ...    ${AUTHORIZATION}=Basic ${encoded}
    Create Session    oauth_session    ${AUTH_BASE_URL}
    ${response}=    POST On Session    oauth_session    ${TOKEN_PATH_URL}    headers=${header}    data=${json_data}
    Should Be Equal As Numbers    ${response.status_code}    200
    Log    ${response.text}
    ${access}=    Get Value From Json  ${response.json()}      access_token
    Log    ${access}[0]
    RETURN     ${access}[0]

Encode Basic Auth
    [Arguments]    ${client_id}    ${client_secret}
    ${credentials}=    Set Variable    ${client_id}:${client_secret}
    Log    ${credentials}
    ${encoded}=    Convert To Base64    ${credentials}
    RETURN       ${encoded}

Convert To Base64
    [Arguments]    ${value}
    ${base64}=    Evaluate    base64.b64encode('${value}'.encode('utf-8')).decode('utf-8')
    RETURN    ${base64}

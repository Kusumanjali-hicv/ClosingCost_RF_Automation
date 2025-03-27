*** Settings ***
Library    OperatingSystem
Library    json
Library    JSONLibrary
Library    ${EXECDIR}/resources/test_data_manager/requestUtils.py
Library    ${EXECDIR}/resources/validation/CC_Fee_Util.py
Library   ${EXECDIR}/resources/validation/CC_Fee_Manager.py
Resource    ${EXECDIR}/resources/common/commons.robot
#Variables    ${EXECDIR}/config/CC_Variables.py  


*** Variables ***
${json_path}
${purchasePrice}    
${saleType}    
${state}   
${brand}
${request_variables}

*** Keywords ***
Send CC API Request
    [Arguments]    ${purchasePrice}    ${saleType}    ${state}    ${brand}
    ${request} =     Prepare Request    ${purchasePrice}    ${saleType}    ${state}    ${brand}
    ${response}=    Send API Request    ${request}    state=${state}    sale_type=${saleType} 
    RETURN    ${request}    ${response}

Assert Closing Cost Fee  
    [Arguments]    ${request}    ${response}    ${purchasePrice}    ${saleType}    ${state}    ${brand}
    Validate Expected CC Fee     ${request}   ${response}    ${purchasePrice}    ${saleType}    ${state}    ${brand}
    

Validate Expected CC Fee 
    [Arguments]    ${request}    ${response}     ${purchasePrice}    ${saleType}    ${state}    ${brand}
    ${Fee_Names}=    Find All CC Fee Types     ${saleType}    ${state}
    ${length} =    Get Length    ${Fee_Names}
    Run Keyword If  ${length} != 0      Assert Expected CC Fee    ${Fee_Names}     ${request}      ${response} 
    ...    ELSE    Log    No valid closing cost fee types found for saleType = '${saleType}', state = '${state}', brand = '${brand}'. Please verify the test data and configuration.
    

Prepare Request 
    [Arguments]    ${purchasePrice}    ${saleType}    ${state}    ${brand}
    Set Global Variables    ${purchasePrice}    ${saleType}    ${state}    ${brand}
    ${request}=     Generate API Request
    RETURN    ${request}

Set Global Variables
    [Arguments]    ${purchasePrice}    ${saleType}    ${state}    ${brand}
    Set Global Variable    ${purchasePrice}
    Set Global Variable    ${saleType}    
    Set Global Variable    ${state}    
    Set Global Variable    ${brand}
    Log Variables

Generate API Request
    ${default_json}=    Get File    path=${json_path}
    ${request_variables}=    Create Dictionary    purchasePrice=${purchasePrice}    saleType=${saleType}    state=${state}    brand=${brand}
    ${json_request}=    create_input_json    ${default_json}    ${request_variables}
    Log    ${json_request}
    ${json}=    Convert String To Json    ${json_request}
    RETURN   ${json}
    
    
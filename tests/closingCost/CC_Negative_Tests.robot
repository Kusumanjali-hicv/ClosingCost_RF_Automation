*** Settings ***
Resource      ${EXECDIR}/resources/test_data_manager/master.robot   
Library           DataDriver    file=${CURDIR}/CC_Negative_TC.csv    
Test Template    Validate ClosingCost Fee Negative TestCases 
#Test Tags    negative_tests   

*** Variables ***
${file_path}    ${EXECDIR}/tests/closingCost/test_data/
${fileName}
${expected_responseCode}
${expected_response_msg}
${status_code}

*** Test Cases ***
Validate ClosingCost Fee Negative TestCases with     ${fileName}    ${expected_responseCode}    ${expected_response_msg}  


*** Keywords ***
Validate ClosingCost Fee Negative TestCases  
    [Arguments]    ${fileName}    ${expected_responseCode}    ${expected_response_msg}  
    ${json_body}=    Load Json Data From File    ${file_path}    ${fileName}
    ${response}=     Send API Request    ${json_body}
    ${expected_code}=    Convert To Integer    ${expected_responseCode}
    Verify API Response    ${expected_code}    ${expected_response_msg}    ${status_code}    ${response}

Load Json Data From File
    [Arguments]    ${path}    ${fileName}
    ${full_path}=    Set Variable    ${path}${fileName}
    ${json_string}=  Get File    ${full_path}
    ${json_data}=    Convert String To Json    ${json_string}
    RETURN       ${json_data}

Verify API Response
    [Arguments]    ${expected_code}    ${expected_response_msg}    ${actual_status}    ${actual_response}
    Should Be Equal    ${actual_status}    ${expected_code}
    Should Be Equal As Strings    ${actual_response}    ${expected_response_msg}     

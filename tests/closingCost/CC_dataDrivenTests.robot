*** Settings ***
Resource      ${EXECDIR}/resources/test_data_manager/master.robot 
Library           DataDriver    file=${CURDIR}\\CC_testData.csv        
Test Template    Validate ClosingCost Fee
Test Tags       closingCost


*** Test Cases ***
Validate ClosingCost Fee with    ${purchasePrice}            ${SaleType}        ${state}    ${brand}


*** Keywords ***
Validate ClosingCost Fee  
    [Arguments]    ${purchasePrice}    ${SaleType}    ${state}    ${brand}
    ${request}    ${response}=    Send CC API Request    ${purchasePrice}    ${SaleType}    ${state}    ${brand}
    Run Keyword And Continue On Failure    Assert Closing Cost Fee    ${request}    ${response}    ${purchasePrice}    ${SaleType}    ${state}    ${brand}
    

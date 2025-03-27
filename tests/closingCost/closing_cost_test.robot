*** Settings ***
Resource      ${EXECDIR}/resources/test_data_manager/master.robot   
Test Template    Validate ClosingCost Fee

   
*** Test Cases ***        ${purchasePrice}    ${SaleType}        ${state}    ${brand}
TC001                     100000             Sales Refinance      TX            HICV
TC002                     205000             Trust Sale           FL            HICV
TC003                     100000             Loan Refinance       IL            HICV
TC004                     205000             Sales Refinance      AZ            HICV
TC005                     90000              Trust Sale           TN            HICV
TC006                     105000             Loan Refinance       FL            HICV
TC007                     104589             Sales Refinance      AZ            HICV
TC008                     205114             Trust Sale           GA            HICV
TC009                     80000              Loan Refinance       MO            HICV
TC010                     215690             Sales Refinance      MA            HICV
TC011                     95800              Trust Sale           NV            HICV
TC012                     100000             Loan Refinance       SC            HICV
TC013                     85300              Sales Refinance      WI            HICV
TC014                     450900             Trust Sale           VT            HICV
TC015                     385000             Loan Refinance       VA            HICV




*** Keywords ***
Validate ClosingCost Fee  
    [Arguments]    ${purchasePrice}    ${SaleType}    ${state}    ${brand}
    ${request}    ${response}=    Send CC API Request    ${purchasePrice}    ${SaleType}    ${state}    ${brand}
    Run Keyword And Continue On Failure    Assert Closing Cost Fee    ${request}    ${response}    ${purchasePrice}    ${SaleType}    ${state}    ${brand}
    
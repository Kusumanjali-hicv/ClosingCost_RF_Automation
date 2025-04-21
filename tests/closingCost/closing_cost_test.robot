*** Settings ***
Resource      ${EXECDIR}/resources/test_data_manager/master.robot   
Test Template    Validate ClosingCost Fee

   
*** Test Cases ***        ${purchasePrice}            ${SaleType}        ${state}    ${brand}    ${location}
Sales_Refinance_TX                100000             Sales Refinance      TX            HICV     ALL
Trust_Sale_FL                     205000             Trust Sale           FL            HICV     ALL
Loan_Refinance_IL                 100000             Loan Refinance       IL            HICV     ALL
Sales_Refinance_AZ                205000             Sales Refinance      AZ            HICV     ALL
Trust_Sale_TN                     90000              Trust Sale           TN            HICV     ALL
Loan_Refinance_FL                 105000             Loan Refinance       FL            HICV     ALL
Sales_Refinance_AZ                104589             Sales Refinance      AZ            HICV     ALL
Trust_Sale_GA                     205114             Trust Sale           GA            HICV     ALL
Loan_Refinance_MO                 80000              Loan Refinance       MO            HICV     ALL
Sales_Refinance_MA                215690             Sales Refinance      MA            HICV     ALL
Trust_Sale_NV                     95800              Trust Sale           NV            HICV     ALL
Loan_Refinance_SC                 100000             Loan Refinance       SC            HICV     ALL
Sales_Refinance_WI                85300              Sales Refinance      WI            HICV     ALL
Trust_Sale_VT                     450900             Trust Sale           VT            HICV     ALL
Loan_Refinance_VA                 385000             Loan Refinance       VA            HICV     ALL
Sales_Refinance_FL                175200             Sales Refinance      FL            HICV     ALL
Loan_Refinace_Va                  106500             Loan Refinance       VA            HICV     ALL
Sales_Refinance_NC                100000             Sales Refinance      VA            HICV     ALL



*** Keywords ***
Validate ClosingCost Fee  
    [Arguments]    ${purchasePrice}    ${SaleType}    ${state}    ${brand}    ${location}
    ${request}    ${response}=    Send CC API Request    ${purchasePrice}    ${SaleType}    ${state}    ${brand}    ${location}
    Run Keyword And Continue On Failure    Assert Closing Cost Fee    ${request}    ${response}    ${purchasePrice}    ${SaleType}    ${state}    ${brand}
    

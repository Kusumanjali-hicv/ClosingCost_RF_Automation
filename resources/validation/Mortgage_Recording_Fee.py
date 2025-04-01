from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword

FEE_NAME = "Mortgage Recording Fee"
NO_OF_PAGES = 2
FIRST_PAGE_FEE = 10.00
ADDITIONAL_PAGE_FEE = 8.50
ADDITIONAL_PURCHASERS_FEE = 1.00
PURCHASER_LIMIT_TRUST_SALE = 3
PURCHASER_LIMIT_REFINANCE = 4
PAYABLE_TO_FL = "Holiday Inn Club Vacations Incorporated"
PAYABLE_TO_TRUST_SALE = "Orange County Comptroller"

@keyword
def compute_mortgage_recording_fee(request_dict, api_response):
    state = request_dict['state']
    sale_type = request_dict['saleType']
    
    # mapping the state to (expected fee, expected payableTo)
    fee_config = {
        "IL": (80.00, "LaSalle County Recorder"),
        "MA": (105.00, "Berkshire Registry of Deeds"),
        "WI": (30.00, "Walworth County Register of Deeds"),
    }
    
    exp_fee = ""
    exp_payable_To = ""

    if sale_type == "Trust Sale":
        fee_name =  FEE_NAME
        #$10.00 for the 1st page, each additional page will be $8.50 , in addition if there are more than 3 purchasers on the contract an additional $1.00 will be added for each additional purchaser. Currently $18.50 [two pages total]
        exp_fee = FIRST_PAGE_FEE + (NO_OF_PAGES - 1) * ADDITIONAL_PAGE_FEE
        if request_dict['numberOfPurchasers'] > PURCHASER_LIMIT_TRUST_SALE:
            exp_fee += (request_dict['numberOfPurchasers'] - PURCHASER_LIMIT_TRUST_SALE) * ADDITIONAL_PURCHASERS_FEE

        exp_payable_To = PAYABLE_TO_TRUST_SALE
    
    if sale_type in ["Sales Refinance", "Loan Refinance"]:
        
        fee_name = f"{FEE_NAME}-{state}"
        if state in fee_config:
            exp_fee, exp_payable_To = fee_config[state]
        elif state == "FL":
            #$10.00 for the 1st page, $8.50 for each additional page. If there are more than 4 Purchasers signing the Mortgage, an additional $1.00 will be added for each over 4.
            exp_fee = FIRST_PAGE_FEE + ((NO_OF_PAGES - 1) * ADDITIONAL_PAGE_FEE)
            if request_dict['numberOfPurchasers'] > PURCHASER_LIMIT_REFINANCE:
                exp_fee += (request_dict['numberOfPurchasers'] - PURCHASER_LIMIT_REFINANCE) * ADDITIONAL_PURCHASERS_FEE

            exp_payable_To = PAYABLE_TO_FL
        else:
            logger.info(f"{FEE_NAME} is not applicable for state: {state} and sale_type: {sale_type}")
            return

    # get actual fee details from the response
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)
    
    if amount != exp_fee:
        logger.error(
            f"<span style='color:red'>{fee_name} amount mismatch: expected {exp_fee}, got {amount}</span>", 
            html=True
        )
    if description != fee_name:
        logger.error(
            f"<span style='color:red'>{fee_name} description mismatch: expected {fee_name}, got {description}</span>", 
            html=True
        )
    if payableTo != exp_payable_To:
        logger.error(
            f"<span style='color:red'>{fee_name} payableTo mismatch: expected {exp_payable_To}, got {payableTo}</span>",
            html=True
        )
    
    errors = []
    if amount != exp_fee:
        errors.append(f"{fee_name} amount mismatch: expected {exp_fee}, got {amount}")
    if description != fee_name:
        errors.append(f"{fee_name} description mismatch: expected {fee_name}, got {description}")
    if payableTo != exp_payable_To:
        errors.append(f"{fee_name} payableTo mismatch: expected {exp_payable_To}, got {payableTo}")
    assert not errors, " | ".join(errors)

    logger.info(f"<span style='color:green'>{fee_name} assertion passed</span>", html=True)
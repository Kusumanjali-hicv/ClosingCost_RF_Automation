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

FEE_CONFIG = {
    "IL": (80.00, "LaSalle County Recorder"),
    "MA": (105.00, "Berkshire Registry of Deeds"),
    "WI": (30.00, "Walworth County Register of Deeds"),
}

SALE_TYPES_TRUST_SALE = [
    "New", "Downgrade", "Reload", "Reload Equity", 
    "Reload New Money", "Rewrite", "Upgrade"
]
SALE_TYPES_REFINANCE = ["Sales Refinance", "Loan Refinance"]

def calculate_fee_and_payable_to(request_dict, sale_type, state):
    if sale_type in SALE_TYPES_TRUST_SALE:
        exp_fee = FIRST_PAGE_FEE + (NO_OF_PAGES - 1) * ADDITIONAL_PAGE_FEE
        if request_dict['numberOfPurchasers'] > PURCHASER_LIMIT_TRUST_SALE:
            exp_fee += (request_dict['numberOfPurchasers'] - PURCHASER_LIMIT_TRUST_SALE) * ADDITIONAL_PURCHASERS_FEE
        return exp_fee, PAYABLE_TO_TRUST_SALE

    if sale_type in SALE_TYPES_REFINANCE:
        if state in FEE_CONFIG:
            return FEE_CONFIG[state]
        if state == "FL":
            exp_fee = FIRST_PAGE_FEE + (NO_OF_PAGES - 1) * ADDITIONAL_PAGE_FEE
            if request_dict['numberOfPurchasers'] > PURCHASER_LIMIT_REFINANCE:
                exp_fee += (request_dict['numberOfPurchasers'] - PURCHASER_LIMIT_REFINANCE) * ADDITIONAL_PURCHASERS_FEE
            return exp_fee, PAYABLE_TO_FL

    return None, None

def log_and_assert(fee_name, exp_fee, exp_payable_to, amount, description, payable_to):
    errors = []
    if amount != exp_fee:
        errors.append(f"{fee_name} amount mismatch: expected {exp_fee}, got {amount}")
        logger.error(f"<span style='color:red'>{fee_name} amount mismatch: expected {exp_fee}, got {amount}</span>", html=True)
    if description != fee_name:
        errors.append(f"{fee_name} description mismatch: expected {fee_name}, got {description}")
        logger.error(f"<span style='color:red'>{fee_name} description mismatch: expected {fee_name}, got {description}</span>", html=True)
    if payable_to != exp_payable_to:
        errors.append(f"{fee_name} payableTo mismatch: expected {exp_payable_to}, got {payable_to}")
        logger.error(f"<span style='color:red'>{fee_name} payableTo mismatch: expected {exp_payable_to}, got {payable_to}</span>", html=True)
    
    assert not errors, " | ".join(errors)
    logger.info(f"<span style='color:green'>{fee_name} assertion passed</span>", html=True)

@keyword
def compute_mortgage_recording_fee(request_dict, api_response):
    state = request_dict['state']
    sale_type = request_dict['saleType']
    fee_name = FEE_NAME if sale_type in SALE_TYPES_TRUST_SALE else f"{FEE_NAME}-{state}"

    exp_fee, exp_payable_to = calculate_fee_and_payable_to(request_dict, sale_type, state)
    if exp_fee is None or exp_payable_to is None:
        logger.info(f"{FEE_NAME} is not applicable for state: {state} and sale_type: {sale_type}")
        return

    amount, description, payable_to = getFeeDetails(fee_name, api_response)
    #logger.info(f"{fee_name} Actual Values - amount: {amount}, description: {description}, payableTo: {payable_to}", html=True)

    log_and_assert(fee_name, exp_fee, exp_payable_to, amount, description, payable_to)

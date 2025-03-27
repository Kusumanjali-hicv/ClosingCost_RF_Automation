from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword

FEE_NAME = "Mortgage Recording Fee"

@keyword
def compute_mortgage_recording_fee(request_dict, api_response):
    state = request_dict['state']
    sale_type = request_dict['saleType']
    fee_name = f"{FEE_NAME}-{state}"
    
    # mapping the state to (expected fee, expected payableTo)
    fee_config = {
        "IL": (80.00, "LaSalle County Recorder"),
        "MA": (105.00, "Berkshire Registry of Deeds"),
        "WI": (30.00, "Walworth County Register of Deeds"),
    }
    
    exp_fee = ""
    exp_payable_To = ""
    
    if sale_type in ["Sales Refinance", "Loan Refinance"]:
        if state in fee_config:
            exp_fee, exp_payable_To = fee_config[state]
        elif state == "FL":
            logger.info(" [TODO] Mortgage Recording Fee")
        else:
            logger.error(f"Mortgage Recording Fee is not applicable for state: {state} and sale_type: {sale_type}")
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
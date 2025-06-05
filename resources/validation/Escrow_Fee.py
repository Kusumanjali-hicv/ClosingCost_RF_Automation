from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword
from robot.api import logger

FEE_NAME = "Escrow Fee"
FEE_AMT_1 = 25.00
FEE_AMT_2 = 50.00
PAYABLE_TO = "Wilson Title Agency Services, LLC"

@keyword("Compute Escrow Fee")
def compute_escrow_fee(request_dict, api_response):
    state = request_dict['state']
    sale_type = request_dict['saleType']
    financed_amount = request_dict['financedAmount']
    fee_name = FEE_NAME # + state

    # Retrieve fee details from the API response
    amount, description, payable_to = getFeeDetails(fee_name, api_response)
    
    # Verify description immediately
    assert description == fee_name, "Escrow Fee description is not as expected"
    
    # Determine the expected fee amount based on financed amount
    exp_amount = FEE_AMT_1 if financed_amount <= 50000 else FEE_AMT_2
    
    if state != "AZ":
        logger.info(f"{FEE_NAME} is not applicable for state: {state} and sale_type: {sale_type}")
        return

    # Check amount
    if amount != exp_amount:
        logger.error(
            f"<span style='color:red'>Escrow Fee, Mismatch on amount: expected {exp_amount}, got {amount}</span>", 
            html=True)
    assert amount == exp_amount, f"Escrow Fee amount is not as expected for {state}"

    # Check payable_to
    if payable_to != PAYABLE_TO:
        logger.error(
            f"<span style='color:red'>Escrow Fee, Mismatch on payableTo: expected {PAYABLE_TO}, got {payable_to}</span>", 
            html=True)
    assert payable_to == PAYABLE_TO, f"Escrow Fee payableTo is not as expected for {state}"

    # Check description (re-assert for state 'AZ')
    if description != fee_name:
        logger.error(
            f"<span style='color:red'>Escrow Fee, Mismatch on description: expected {fee_name}, got {description}</span>", 
            html=True)
    assert description == fee_name, f"Escrow Fee description is not as expected for {state}"

    logger.info(f"<span style='color:green'>{fee_name} assertion passed</span>", html=True)
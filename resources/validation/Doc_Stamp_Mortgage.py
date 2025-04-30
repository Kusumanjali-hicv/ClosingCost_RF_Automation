from robot.api import logger
from CC_Fee_Util import getFeeDetails, round_up_to_nearest_100
from robot.api.deco import keyword

FEE_NAME = "Documentary Stamps - Mortgage"
PAYABLE_TO = "Orange County Comptroller"

def compute_doc_stamp_mortgage_fee(request_dict, api_response):
    #The system shall accept Financed Amount as inputs for the calculation.
#The system shall calculate Documentary Stamps- Mortgage at 35 cents per $100.00 of the amount financed.
# The amount financed shall be rounded up to the nearest hundred for the calculation.
    fin_amt = request_dict['financedAmount']
    fin_amt = round_up_to_nearest_100(fin_amt)
    exp_fee = (fin_amt/100) * 0.35

    exp_fee = round(exp_fee, 2)
    # get actual fee details from the response
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)
    errors = assert_doc_stamp_mortgage_fee(
        amount, description, FEE_NAME, payableTo,
        request_dict['saleType'], exp_fee, PAYABLE_TO)
    if errors:
        for error in errors:
            logger.error(error, html=True)
        raise AssertionError("\n".join(errors))
    else:
        logger.info(f"<span style='color:green'>{FEE_NAME} assertions passed</span>", html=True)
    
def assert_doc_stamp_mortgage_fee(
    amount, description, fee_name, payableTo,
    sale_type, exp_fee, exp_payable_To
):
    errors = []
    if description != fee_name:
        errors.append(f"Fee description is not as expected: expected '{fee_name}', got '{description}'")
    
    if amount != exp_fee:
        err_msg = f"Mismatch on amount for {fee_name}: expected {exp_fee}, got {amount}"
        errors.append(f"<span style='color:red'>{err_msg}</span>")
    
    if payableTo != exp_payable_To:
        err_msg = f"Mismatch on payableTo for {fee_name}: expected {exp_payable_To}, got {payableTo}"
        errors.append(f"<span style='color:red'>{err_msg}</span>")
    
    return errors


    
from CC_Fee_Util import getFeeDetails, get_lenders_title_policy_fee
from robot.api.deco import keyword
from robot.api import logger

DESCRIPTION = "Purchasers Fee"
PAYABLE_TO = "Purchasers Fee"
FEE_NAME = "Purchasers Fee"

def compute_purchasers_fee(request_dict, api_response):
    sale_type = request_dict['saleType']
    state = request_dict['state']
    fee_list = ["Documentary Stamps - Deed","Documentary Stamps - Mortgage", "Intangible Tax - Note"]

    # Get actual fee details from the response
    total_amount = 0
    for fee_name in fee_list:
        fee_amount, _, _ = getFeeDetails(fee_name, api_response)
        if fee_amount is not None:
            total_amount += fee_amount
    amount, _, _ = get_lenders_title_policy_fee("Lender's Title Insurance", api_response)
    if amount != 0:
        total_amount += float(amount)
    total_amount *= -1  # Convert to negative as per the original logic
    if total_amount == 0:
        logger.info("No applicable fees found for Purchasers Fee calculation.")
        return
    
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)
    
    
    if total_amount is not None:
        errors = assert_purchasers_fee(amount, description, payableTo, sale_type, total_amount)
        if errors:
            error_msg = "\n".join(errors)
            logger.error("<span style='color:red'>{}</span>".format(error_msg), html=True)
            raise AssertionError(error_msg)
        logger.info("<span style='color:green'>Purchasers Fee assertion passed</span>", html=True)
    else:
        logger.warn("Purchasers Fee is not applicable for this sale type: {} in state: {}.".format(sale_type, state), html=True)

@keyword
def assert_purchasers_fee(amount, description, payableTo, sale_type, fee):
    errors = []
    if amount != fee:
        errors.append("{} amount mismatch for {}: expected {}, got {}".format(FEE_NAME, sale_type, fee, amount))
    if description != DESCRIPTION:
        errors.append("{} description mismatch for {}: expected '{}', got '{}'".format(FEE_NAME, sale_type, DESCRIPTION, description))
    if payableTo != PAYABLE_TO:
        errors.append("{} payableTo mismatch for {}: expected '{}', got '{}'".format(FEE_NAME, sale_type, PAYABLE_TO, payableTo))
    return errors
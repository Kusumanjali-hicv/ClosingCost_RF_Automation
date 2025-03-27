from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword
from robot.api import logger

TRUST_SALE_FEE = 25.00
REFINANCE_FEE = 100.00
FEE_NAME = "Title Search Fee"
DESCRIPTION = "Title Search Fee"
PAYABLE_TO = "Wilson Title Services, LLC"

@keyword
def compute_title_search_fee(request_dict, api_response):
    sale_type = request_dict['saleType']
    state = request_dict['state']

    # get actual fee details from the response
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)

    fee = None
    if sale_type == "Trust Sale":
        fee = TRUST_SALE_FEE
    elif sale_type in ["Sales Refinance", "Loan Refinance"] and state not in ["TX", "AZ"]:
        fee = REFINANCE_FEE

    if fee is not None:
        errors = assert_title_search_fee(amount, description, payableTo, sale_type, fee)
        if errors:
            error_msg = "\n".join(errors)
            logger.error("<span style='color:red'>{}</span>".format(error_msg), html=True)
            raise AssertionError(error_msg)
        logger.info("<span style='color:green'>{} assertion passed</span>".format(FEE_NAME), html=True)
    else:
        logger.info("Title Search Fee is not applicable for this sale type")
        return

@keyword
def assert_title_search_fee(amount, description, payableTo, sale_type, fee):
    errors = []
    if amount != fee:
        errors.append("Title Search Fee amount mismatch for {}: expected {}, got {}".format(sale_type, fee, amount))
    if description != DESCRIPTION:
        errors.append("Title Search Fee description mismatch for {}: expected '{}', got '{}'".format(sale_type, DESCRIPTION, description))
    if payableTo != PAYABLE_TO:
        errors.append("Title Search Fee payableTo mismatch for {}: expected '{}', got '{}'".format(sale_type, PAYABLE_TO, payableTo))
    return errors

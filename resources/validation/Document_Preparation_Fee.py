from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword
from robot.api import logger

FEE_NAME = "Document Preparation Fee"
REFINANCE_FEE = 130.00
REFINANCE_PAYABLE_TO = "Holiday Inn Club Vacations Incorporated"
TRUST_SALE_FEE = 121.00
TRUST_SALE_PAYABLE_TO = "Orange Lake Country Club, Inc"

def compute_document_preparation_fee(request_dict, api_response):
    sale_type = request_dict.get('saleType')
    
    if sale_type in ("Sales Refinance", "Loan Refinance"):
        fee_name = FEE_NAME + " - Refinance"
        exp_fee = REFINANCE_FEE
        exp_payableTo = REFINANCE_PAYABLE_TO
    elif sale_type == "Trust Sale":
        fee_name = FEE_NAME
        exp_fee = TRUST_SALE_FEE
        exp_payableTo = TRUST_SALE_PAYABLE_TO
    else:
        logger.error(f"Unknown sale type: {sale_type}")
        return
    
    amount, description, payableTo = getFeeDetails(fee_name, api_response)
    assert_document_preparation_fee(amount, description, fee_name, payableTo, sale_type, exp_fee, exp_payableTo)
    
    logger.info("<span style='color:green'>" + fee_name + " assertion passed</span>", html=True)

def assert_document_preparation_fee(amount, description, fee_name, payableTo, sale_type, exp_fee, exp_payableTo):
    errors = []
    comparisons = [
        (amount, exp_fee, "amount", "Document Preparation Fee amount mismatch for {}: expected {}, got {}"),
        (description, fee_name, "description", "Document Preparation Fee description mismatch for {}: expected {}, got {}"),
        (payableTo, exp_payableTo, "payableTo", "Document Preparation Fee payableTo mismatch for {}: expected {}, got {}")
    ]
    
    for actual, expected, field, error_msg in comparisons:
        if actual != expected:
            logger.error("<span style='color:red'>" + error_msg.format(sale_type, expected, actual) + "</span>", html=True)
            errors.append("Document Preparation Fee {} is not as expected: expected {} got {}".format(field, expected, actual))
            
    if errors:
        raise AssertionError("\n".join(errors))

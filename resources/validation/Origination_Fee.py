from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword
from robot.api import logger

FEE_NAME = "Origination Fee"
SALES_REFINANCE_FEE = 399.00
LOAN_REFINANCE_FEE = 0.00
REFINANCE_PAYABLE_TO = "Holiday Inn Club Vacations Incorporated"
TRUST_SALE_PAYABLE_TO = "Wilson Resort Finance, LLC"

def compute_origination_fee(request_dict, api_response):
    sale_type = request_dict['saleType']
    state = request_dict['state']
    # Retrieve fee details from response
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)
    
    if sale_type in ("Sales Refinance", "Loan Refinance"):
        fee = SALES_REFINANCE_FEE if sale_type == "Sales Refinance" else LOAN_REFINANCE_FEE
        exp_payableTo = REFINANCE_PAYABLE_TO
        fee_name = FEE_NAME + " - Refinance"
    elif sale_type in ["New", "Downgrade", "Reload", "Reload Equity", "Reload New Money", "Rewrite", "Upgrade"]:
        fee = 0.032 * (float(request_dict['purchasePrice']) - float(request_dict['cash']))
        fee = round(fee, 2)
        exp_payableTo = TRUST_SALE_PAYABLE_TO
        fee_name = FEE_NAME
    else:
        logger.info(f"{FEE_NAME} is not applicable for sale_type: {sale_type} in state: {state}")
        return

    errors = assert_origination_fee(amount, description, fee_name, payableTo,
                                     sale_type, fee, exp_payableTo)
    
    for error in errors:
        logger.error(error, html=True)
    
    assert not errors, "Origination Fee validation failed: " + "; ".join(errors)
    logger.info(f"<span style='color:green'>{fee_name} assertion passed</span>", html=True)


def assert_origination_fee(amount, description, fee_name, payableTo, sale_type, fee, exp_payableTo):
    errors = []
    
    if amount != fee:
        errors.append(
            "<span style='color:red'>Origination Fee amount mismatch for {}: expected {}, got {}</span>"
            .format(sale_type, fee, amount)
        )
    if description != fee_name:
        errors.append(
            "<span style='color:red'>Origination Fee description mismatch for {}: expected {}, got {}</span>"
            .format(sale_type, fee_name, description)
        )
    if payableTo != exp_payableTo:
        errors.append(
            "<span style='color:red'>Origination Fee payableTo mismatch for {}: expected {}, got {}</span>"
            .format(sale_type, exp_payableTo, payableTo)
        )
        
    return errors

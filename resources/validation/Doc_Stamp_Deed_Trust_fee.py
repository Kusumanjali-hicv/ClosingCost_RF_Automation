from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword

FEE_NAME = "Documentary Stamps - Deed"
REFINANCE_FEE = .0033333
REFINANCE_PAYABLE_TO = "York County Circuit Court"
TRUST_PAYABLE_TO = "Orange County Comptroller"


def compute_doc_stamp_deed_fee(request_dict, api_response):
    sale_type = request_dict['saleType']
    state = request_dict['state']
    

    if sale_type == "Trust Sale":
        fee_name = f"{FEE_NAME}"
        # calculated at a rate of 70 cents per $100.00 of the sales price rounded up to the nearest hundred
        exp_fee = round(float(request_dict['purchasePrice']) / 100, 2) * 0.70
        exp_fee = round(exp_fee, 2)
        exp_payable_To = TRUST_PAYABLE_TO
        # Retrieve fee details from response
        amount, description, payableTo = getFeeDetails(fee_name, api_response)

        errors = assert_doc_stamp_deed_fee(
            amount, description, fee_name, payableTo,
            sale_type, exp_fee, exp_payable_To
        )


    elif sale_type in ["Sales Refinance", "Loan Refinance"] and state == "VA":
        fee_name = f"{FEE_NAME}-{state}"
        fin_amt = request_dict['financedAmount']
        exp_payable_To = REFINANCE_PAYABLE_TO

        exp_fee = round(fin_amt, 2) * REFINANCE_FEE
        exp_fee = round(exp_fee, 2)
        # Retrieve fee details from response
        amount, description, payableTo = getFeeDetails(fee_name, api_response)

        errors = assert_doc_stamp_deed_fee(
            amount, description, fee_name, payableTo,
            sale_type, exp_fee, exp_payable_To
        )
    else:
        logger.error(f"<span style='color:red'>Unknown sale type: {sale_type}</span>", html=True)
        return
    

    for error in errors:
        logger.error(error, html=True)
    
    assert not errors, "Origination Fee validation failed: " + "; ".join(errors)
    logger.info(f"<span style='color:green'>{fee_name} assertion passed</span>", html=True)



def assert_doc_stamp_deed_fee(amount, description, fee_name, payableTo, sale_type, fee, exp_payableTo):
    errors = []

    if amount != fee:
        errors.append(
            "<span style='color:red'>Doc Stamp Deed Fee amount mismatch for {}: expected {}, got {}</span>"
            .format(sale_type, fee, amount)
        )
    if description != fee_name:
        errors.append(
            "<span style='color:red'>Doc Stamp Deed Fee description mismatch for {}: expected {}, got {}</span>"
            .format(sale_type, fee_name, description)
        )
    if payableTo != exp_payableTo:
        errors.append(
            "<span style='color:red'>Doc Stamp Deed Fee payableTo mismatch for {}: expected {}, got {}</span>"
            .format(sale_type, exp_payableTo, payableTo)
        )

    return errors

        

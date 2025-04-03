from robot.api import logger
from CC_Fee_Util import getFeeDetails, round_up_to_nearest_100
from robot.api.deco import keyword


FEE_NAME = "Documentary Stamps - Deed"
REFINANCE_FEE = 0.0033333
REFINANCE_PAYABLE_TO = "York County Circuit Court"
TRUST_PAYABLE_TO = "Orange County Comptroller"


def compute_doc_stamp_deed_fee(request_dict, api_response):
    sale_type = request_dict['saleType']
    state = request_dict['state']

    if sale_type == "Trust Sale":
        fee_name = FEE_NAME  # assign fee_name for consistency
        purchase_price = float(request_dict['purchasePrice'])
        purchase_price = round_up_to_nearest_100(purchase_price)
        #calculate at a rate of 70 cents per $100.00 of the Purchase Price.
        exp_fee = (purchase_price /100) * 0.70
        exp_fee = round(exp_fee, 2)

        exp_payable_To = TRUST_PAYABLE_TO
        # Retrieve fee details from response
        amount, description, payableTo = getFeeDetails(fee_name, api_response)
        
        errors = assert_doc_stamp_deed_fee(
            amount, description, fee_name, payableTo,
            sale_type, exp_fee, exp_payable_To
        )
        if errors:
            for error in errors:
                logger.error(error, html=True)
            raise AssertionError("\n".join(errors))

    elif sale_type in ["Sales Refinance", "Loan Refinance"] and state == "VA":
        fee_name = f"{FEE_NAME}-{state}"
        fin_amt = round(request_dict['financedAmount'] / 100) * 100  # round to nearest hundred
        exp_payable_To = REFINANCE_PAYABLE_TO

        exp_fee = round(fin_amt, 2) * REFINANCE_FEE
        exp_fee = round(exp_fee, 2)
        # Retrieve fee details from response
        amount, description, payableTo = getFeeDetails(fee_name, api_response)

        errors = assert_doc_stamp_deed_fee(
            amount, description, fee_name, payableTo,
            sale_type, exp_fee, exp_payable_To
        )
        if errors:
            #for error in errors:
            #    logger.error(error, html=True)
            raise AssertionError("\n".join(errors))
    else:
        logger.info(f"{FEE_NAME} is not applicable for sale type: {sale_type} and state: {state}", html=True)
        return

    logger.info(f"<span style='color:green'>{fee_name} assertion passed</span>", html=True)


def assert_doc_stamp_deed_fee(amount, description, fee_name, payableTo, sale_type, exp_fee, exp_payableTo):
    errors = []

    if amount != exp_fee:
        msg = (f"<span style='color:red'>{fee_name} Fee amount mismatch for {sale_type}: "
               f"expected {exp_fee}, got {amount}</span>")
        errors.append(msg)
    if description != fee_name:
        msg = (f"<span style='color:red'>{fee_name} Fee description mismatch for {sale_type}: "
               f"expected {fee_name}, got {description}</span>")
        errors.append(msg)
    if payableTo != exp_payableTo:
        msg = (f"<span style='color:red'>{fee_name} payableTo mismatch for {sale_type}: "
               f"expected {exp_payableTo}, got {payableTo}</span>")
        errors.append(msg)

    return errors

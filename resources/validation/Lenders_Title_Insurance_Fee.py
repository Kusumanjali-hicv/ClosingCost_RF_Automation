from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword
import math

FEE_NAME = "Lender's Title Insurance"
PAYABLE_TO = "Wilson Title Services"

@keyword
def compute_lenders_title_insurance_fee(request_dict, api_response):
    financed_amount = float(request_dict['financedAmount'])
    purchase_price = float(request_dict['purchasePrice'])

    # Initialize fee details
    fee = 0

    # Calculate the fee only if financed amount is present
    if financed_amount > 0:
        if financed_amount > purchase_price:
            difference = financed_amount - purchase_price
            rounded_difference = math.ceil(difference / 100) * 100  # Round up to the nearest hundred
            fee = (rounded_difference * 0.00575) + 25.00  # Add flat fee of $25.00
        else:
            fee = 25.00  # Flat fee for mortgaged accounts

    # Retrieve fee details from the API response
    amount, description, payable_to = getFeeDetails(FEE_NAME, api_response)

    # Assert the fee and log results
    errors = assert_lenders_title_insurance_fee(
        amount, description, FEE_NAME, payable_to, fee, PAYABLE_TO
    )

    if errors:
        for error in errors:
            logger.error(error, html=True)
        raise AssertionError("\n".join(errors))
    else:
        logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)


def assert_lenders_title_insurance_fee(amount, description, FEE_NAME, payable_to, exp_fee, exp_payable_to):
    errors = []

    if amount != exp_fee:
        msg = (f"<span style='color:red'>{FEE_NAME} amount mismatch: "
               f"Expected {exp_fee}, but got {amount}</span>")
        errors.append(msg)

    if description != FEE_NAME:
        msg = (f"<span style='color:red'>{FEE_NAME} description mismatch: "
               f"Expected '{FEE_NAME}', but got '{description}'</span>")
        errors.append(msg)

    if payable_to != exp_payable_to:
        msg = (f"<span style='color:red'>{FEE_NAME} payableTo mismatch: "
               f"Expected '{exp_payable_to}', but got '{payable_to}'</span>")
        errors.append(msg)

    return errors
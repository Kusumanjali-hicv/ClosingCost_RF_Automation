from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword


FEE_NAME = "Lenders Title Policy"
PAYABLE_TO = "Wilson Title Agency Services, LLC"

def compute_lenders_title_policy_fee(request_dict, api_response):
    state = request_dict['state']
    sale_type = request_dict['saleType']
    financed_amount = float(request_dict['financedAmount'])
    fee = 0

    if sale_type in ["Sales Refinance", "Loan Refinance"]:
        if state == "AZ":
            fee = 356.00
        
        elif state == "GA":
            if financed_amount <= 100000:
                fee = 200.00
            elif financed_amount <= 500000:
                fee = 200.00 + (2.25 * (financed_amount - 100000) / 1000)
        
        elif state == "IL":
            fee = 150.00
                    
        else:
            logger.error(f"No Lenders Title Policy fee configuration for state: {state}")
            return

        # Retrieve fee details from response
        fee_name = FEE_NAME # + f"-{state}"
        amount, description, payableTo = getFeeDetails(fee_name, api_response)

        # Assert the fee and list the errors
        errors = assert_lenders_title_policy_fee(
            amount, description, fee_name, payableTo,
            sale_type, fee, PAYABLE_TO
        )
        if errors:
            for error in errors:
                logger.error(error, html=True)
            raise AssertionError("\n".join(errors))
        else:
            logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)


def assert_lenders_title_policy_fee(amount, description, FEE_NAME, payableTo, sale_type, exp_fee, exp_payableTo):
    errors = []

    if amount != exp_fee:
        errors.append(
            f"<span style='color:red'>{FEE_NAME} amount mismatch for {sale_type}: "
            f"Expected {exp_fee}, but got {amount}</span>"
        )

    if description != FEE_NAME:
        errors.append(
            f"<span style='color:red'>{FEE_NAME} description mismatch for {sale_type}: "
            f"Expected '{FEE_NAME}', but got '{description}'</span>"
        )

    if payableTo != exp_payableTo:
        errors.append(
            f"<span style='color:red'>{FEE_NAME} payableTo mismatch for {sale_type}: "
            f"Expected '{exp_payableTo}', but got '{payableTo}'</span>"
        )

    return errors

from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword
from robot.api import logger

FEE_NAME = "Guarantee Fee-"
FEE_TX = 4.00
FEE_IL = 3.00
PAYABLE_TO_TX = "Texas Title Guaranty Association"
PAYABLE_TO_IL = "Fidelity National Title"

FEE_CONFIGS = {
    "TX": {"fee": FEE_TX, "payableTo": PAYABLE_TO_TX},
    "IL": {"fee": FEE_IL, "payableTo": PAYABLE_TO_IL},
}

@keyword
def compute_guarantee_fee(request_dict, api_response):
    state = request_dict['state']
    sale_type = request_dict['saleType']
    expected_description = FEE_NAME + state
    fee_key = expected_description

    errors = []

    # Get actual fee details from the response.
    amount, description, payableTo = getFeeDetails(fee_key, api_response)

    if description != expected_description:
        errors.append(f"Guarantee Fee description is not as expected: expected '{expected_description}', got '{description}'")

    config = FEE_CONFIGS.get(state)
    if not config:
        logger.info(f"{FEE_NAME} is not applicable for state: {state} and sale_type: {sale_type}")
    else:
        expected_fee = config["fee"]
        expected_payableTo = config["payableTo"]

        if amount != expected_fee:
            err_msg = f"Mismatch on amount for {state}: expected {expected_fee}, got {amount}"
            errors.append(err_msg)
            logger.error(f"<span style='color:red'>{err_msg}</span>", html=True)

        if payableTo != expected_payableTo:
            err_msg = f"Mismatch on payableTo for {state}: expected {expected_payableTo}, got {payableTo}"
            errors.append(err_msg)
            logger.error(f"<span style='color:red'>{err_msg}</span>", html=True)

    if errors:
        raise AssertionError("\n".join(errors))

    logger.info(f"<span style='color:green'>{expected_description} assertion passed</span>", html=True)
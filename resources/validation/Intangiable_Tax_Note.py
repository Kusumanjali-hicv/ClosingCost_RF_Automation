from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword

FEE_NAME = "Intangible Tax - Note"
PAYABLE_TO = "Orange County Comptroller"

@keyword
def compute_intangible_tax_note(request_dict, api_response):
    # get actual fee details from the response
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)

    # Intangible Tax Note is calculated as 0.002 * financedAmount
    expected_amount = 0.002 * request_dict['financedAmount']

    # prepare expected vs actual values
    validations = {
        "amount": (expected_amount, amount, "amount"),
        "payableTo": (PAYABLE_TO, payableTo, "payableTo"),
        "description": (FEE_NAME, description, "description")
    }

    # Log errors for any mismatches
    for key, (expected, actual, label) in validations.items():
        if actual != expected:
            logger.error(
                f"<span style='color:red'>{FEE_NAME} mismatch on {label}: expected {expected}, got {actual}</span>",
                html=True
            )

    errors = []
    if amount != expected_amount:
        errors.append(f"{FEE_NAME} amount is not as expected: expected {expected_amount}, got {amount}")
    if payableTo != PAYABLE_TO:
        errors.append(f"{FEE_NAME} payableTo is not as expected: expected {PAYABLE_TO}, got {payableTo}")
    if description != FEE_NAME:
        errors.append(f"{FEE_NAME} description is not as expected: expected {FEE_NAME}, got {description}")
    if errors:
        raise AssertionError("; ".join(errors))

    logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)
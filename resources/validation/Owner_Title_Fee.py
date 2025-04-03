from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword
from robot.api import logger

FEE_NAME = "Owner's Title Fee"
MIN_FEE = 60.00
PAYABLE_TO = "Wilson Title Services, LLC"


def compute_owner_title_fee(request_dict, api_response):
    purchase_price = float(request_dict['purchasePrice'])
    # round off the purchase price to nearest integer (update below if nearest 100 is intended)
    purchase_price_rounded = round(purchase_price/ 100) * 100

    if purchase_price <= 100000:
        
        fee = purchase_price_rounded * 0.00575
        fee = MIN_FEE if fee < MIN_FEE else round(fee * 100) / 100
    else:
        fee = (100000 * 0.00575) + (round((purchase_price - 100000) / 100 * 100) * 0.0050)
        

    # get actual fee details from the response
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)
    assert_owner_title_fee(amount, description, payableTo, fee)
    
    logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)


def assert_owner_title_fee(amount, description, payableTo, fee):
    errors = []

    if round(float(amount), 2) != round(fee, 2):
        msg = f"Owner's Title Fee amount mismatch: expected {fee:.2f}, got {amount}"
        logger.error(f"<span style='color:red'>{msg}</span>", html=True)
        errors.append(msg)
    if description != FEE_NAME:
        msg = f"Owner's Title Fee description mismatch: expected {FEE_NAME}, got {description}"
        logger.error(f"<span style='color:red'>{msg}</span>", html=True)
        errors.append(msg)
    if payableTo != PAYABLE_TO:
        msg = f"Owner's Title Fee payableTo mismatch: expected {PAYABLE_TO}, got {payableTo}"
        logger.error(f"<span style='color:red'>{msg}</span>", html=True)
        errors.append(msg)

    if errors:
        raise AssertionError("Owner's Title Fee errors: " + "; ".join(errors))

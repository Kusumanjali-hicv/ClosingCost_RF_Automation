from decimal import ROUND_HALF_UP, Decimal
from CC_Fee_Util import getFeeDetails, round_up_to_nearest_100, round_fee
from robot.api.deco import keyword
from robot.api import logger

FEE_NAME = "Owner's Title Fee"
MIN_FEE = 60.00
PAYABLE_TO = "Wilson Title Services, LLC"

@keyword
def compute_owner_title_fee(request_dict, api_response):
    purchase_price = float(request_dict['purchasePrice'])
    purchase_price_rounded = round_up_to_nearest_100(purchase_price)
    #purchase_price_rounded = round(purchase_price/ 100) * 100

    if purchase_price <= 100000:
        
        fee = purchase_price_rounded * 0.00575
        fee = MIN_FEE if fee < MIN_FEE else round_fee(fee)
    else:
        fee = (100000 * 0.00575) + ((purchase_price_rounded - 100000)  * 0.0050)
        

    # get actual fee details from the response
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)
    assert_owner_title_fee(amount, description, payableTo, fee)
    
    logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)


def assert_owner_title_fee(amount, description, payableTo, fee):
    errors = []
    amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    fee = Decimal(str(fee)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    if abs(amount - fee) > Decimal('0.01'):
    #if round(float(amount), 2) != round(fee, 2):    
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

from decimal import ROUND_HALF_UP, Decimal
import json
import math
from robot.api import logger
from robot.api.deco import keyword
from CC_Fee_Util import round_up_to_nearest_100, round_fee

FEE_NAME = "Lender's Title Insurance"
PAYABLE_TO = "Wilson Title Services"
# Initialize fee details
flat_fee = 25.0

@keyword
def compute_lenders_title_insurance_fee(request_dict, api_response):
    financed_amount = float(request_dict['financedAmount'])
    purchase_price = float(request_dict['purchasePrice'])



    # Calculate the fee only if financed amount is present
    if financed_amount > 0:
        if financed_amount > purchase_price:
            difference = financed_amount - purchase_price
            rounded_difference = round_up_to_nearest_100(difference)
            fee = (rounded_difference * 0.00575) 
            #fee = math.ceil(fee*100)/100
            fee = round_fee(fee)  # Round to 2 decimal places
        else:
            fee = 25.00  # Flat fee for mortgaged accounts

    amount, description, payableTo = get_lenders_title_insurance_fee(api_response)
    if amount != 0:
        errors = assert_lenders_title_insurance_fee(
            amount, description, FEE_NAME, payableTo, request_dict['saleType'], fee, PAYABLE_TO)
        if errors:
            for error in errors:
                logger.error(error, html=True)
            raise AssertionError("\n".join(errors))
        else:
            logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)
        

def assert_lenders_title_insurance_fee(amount, description, FEE_NAME, payableTo, sale_type, exp_fee, exp_payableTo):
    errors = []
    amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    #if Decimal(str(amount)) != exp_fee:
    #if amount != exp_fee:
    if abs(amount - exp_fee) > Decimal('0.01'):
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


def get_lenders_title_insurance_fee(api_response):
    amount = 0
    payableTo = ""
    description = ""
    
    if isinstance(api_response, dict):
        json_response = api_response
    else:
        json_response = json.loads(api_response)

    for fee in json_response['closingCosts']['fees']:
        if FEE_NAME.lower() in fee['description'].lower():
            
            if fee['amount'] == flat_fee:
                #assert the payableTo & description are correct
                if fee['amount'] != flat_fee:
                    logger.error(f"<span style='color:red'>Expected amount {flat_fee}, got {fee['amount']}</span>", html=True)
                if fee['payableTo'] != PAYABLE_TO:
                    logger.error(f"<span style='color:red'>Expected payable to {PAYABLE_TO}, got {fee['payableTo']}</span>", html=True)
                if fee['description'] != FEE_NAME:
                    logger.error(f"<span style='color:red'>Expected description {FEE_NAME}, got {fee['description']}</span>", html=True)
                logger.info(f"<span style='color:green'>Assertion Passed for Lenders Title Insurance flat fee  {flat_fee}</span>", html=True)
                continue

            amount = fee['amount']
            payableTo = fee['payableTo']
            description = fee['description']
            
    
    if not amount:
        logger.info("<span style='color:gray'>" + str(FEE_NAME) + " paid by Developer not found  </span>", html=True)
        return 0, "", ""
    
    return amount, description, payableTo 
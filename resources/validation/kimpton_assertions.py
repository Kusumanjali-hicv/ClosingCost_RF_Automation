from robot.api.deco import keyword
from robot.api import logger
from CC_Fee_Util import round_up_to_nearest_100
import json

@keyword()
def Assert_Kimpton_Closing_Cost_Fee(request, response):   

    contract_id = request['contractId']
    purchase_price = request['purchasePrice']
    financed_amount = request['financedAmount']

    if contract_id != None and financed_amount != None:            
        Intagiable_Fee_Name = "intangibleTax"
        Intagiable_Fee_Amount = 0.002
        expected_fee = float(financed_amount) * Intagiable_Fee_Amount
        expected_fee = round(expected_fee, 2)
        intagiable_fee = get_fee_from_response(response, Intagiable_Fee_Name)
        if intagiable_fee != expected_fee:
            raise AssertionError(f"Intangible Tax fee mismatch: Expected {expected_fee}, but got {intagiable_fee}")
        else:
                logger.info(f"<span style='color:green'>{Intagiable_Fee_Name} assertion passed, amount = {intagiable_fee}</span>", html=True)
        
        Escrow_Fee_Name = "escrowAgentFee"
        if float(purchase_price) > 0:
            expected_fee = 75.00
            escrow_fee_amt = get_fee_from_response(response, Escrow_Fee_Name)
            if escrow_fee_amt != expected_fee:
                raise AssertionError(f"Escrow Agent fee mismatch: Expected {expected_fee}, but got {escrow_fee_amt}")
            else:
                logger.info(f"<span style='color:green'>{Escrow_Fee_Name} assertion passed, amount = {escrow_fee_amt}</span>", html=True)
    
        Title_Insurance_Fee_Name = "titleInsuranceFee"
        if float(purchase_price) <= 75000:
            expected_fee = 30.00
        else:
            expected_fee = 30 + (float(purchase_price) - 75000) / 1000 * 0.75
            expected_fee = round(expected_fee, 2)
        title_insurance_fee = get_fee_from_response(response, Title_Insurance_Fee_Name)
        if title_insurance_fee != expected_fee:
            raise AssertionError(f"Title Insurance fee mismatch: Expected {expected_fee}, but got {title_insurance_fee}")
        else:
                logger.info(f"<span style='color:green'>{Title_Insurance_Fee_Name} assertion passed, amount = {expected_fee}</span>", html=True)
        
        Documentary_Stamp_Fee_Name = "documentaryStamps"
        if float(financed_amount) > 0:
            expected_fee = ((round_up_to_nearest_100(financed_amount) / 100) * 0.35)
            documentary_stamp_fee = get_fee_from_response(response, Documentary_Stamp_Fee_Name)
            expected_fee = round(expected_fee, 2)
            if documentary_stamp_fee != expected_fee:
                raise AssertionError(f"Documentary Stamp Tax fee mismatch: Expected {expected_fee}, but got {documentary_stamp_fee}")
            else:
                logger.info(f"<span style='color:green'>{Documentary_Stamp_Fee_Name} assertion passed, amount = {documentary_stamp_fee}</span>", html=True)
    
    else:
        raise ValueError("Contract Id or Financed Amount  is missing in the request")




def get_fee_from_response(response, fee_name):
    
    if isinstance(response, str):
        response = json.loads(response)

    closing_costs = response.get("closingCosts", {})
    for key, value in closing_costs.items():
        if key.lower() == fee_name.lower():
            return value
    raise KeyError(f"Fee '{fee_name}' not found in response['closingCosts']")
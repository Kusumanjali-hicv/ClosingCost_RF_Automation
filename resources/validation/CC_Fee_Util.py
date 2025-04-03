import json
from robot.api.deco import keyword
from robot.api import logger

with open('config/CC_Fee.json') as f:
    fee_data = json.load(f)

@keyword
def find_all_CC_fee_types(saleType, state):
    
    fee_names = []
    for fee in fee_data['Fees']:
        if state in fee['state'] and saleType in fee['saleType']:
            fee_names.append(fee['name'])

    return fee_names
    
 
@keyword
def getFeeDetails(feeName, json_response):
    amount = ""
    payableTo = ""
    description = ""
    if isinstance(json_response, dict):
        json_response = json_response
    else:
        json_response = json.loads(json_response)


    for i in range(len(json_response['closingCosts']['fees'])):
        if feeName in json_response['closingCosts']['fees'][i]['description']:
           
           amount = json_response['closingCosts']['fees'][i]['amount']
           payableTo = json_response['closingCosts']['fees'][i]['payableTo']
           description = json_response['closingCosts']['fees'][i]['description']
 
           logger.info("<span style='color:blue'>\nFee_Name: " + str(description) + 
                    " \nAmount: " + str(amount) + " \tPayable To: " + str(payableTo) + 
                    "</span>", html=True)
           return amount, description, payableTo 
       
    logger.info("<span style='color:red'>Fee not found: " + str(feeName) + "</span>", html=True)
    return amount, description, payableTo    

def round_up_to_nearest_100(value):
    # Round up to the nearest 100
    if value % 100 == 0:
        return value
    else:
        return ((value // 100) + 1) * 100
""" 
Round Up To Nearest 100
    [Arguments]        ${Value}
    ${REMAINDER}=    Evaluate    ${Value} % 100
    ${ROUNDED}=    Evaluate    ${Value} + (100 - ${REMAINDER}) if ${REMAINDER} > 0 else ${Value}
    RETURN    ${ROUNDED} """
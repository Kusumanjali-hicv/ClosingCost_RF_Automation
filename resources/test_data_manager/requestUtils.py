import json
import random
import string

KC_siteId = "37"
HICV_siteId = "9999"
FINANCED_AMT = ["30000", "40000", "50000", "60000", "70000", "80000"]
POINTS = ["100000", "100500", "30000", "40000", "50500"]

def create_input_json(default_json, request_variables):
    
    contractId = set_contractId()
    request_variables['contractId'] = contractId

    request_variables = set_siteID(request_variables)

    financedAmount, cash, points = set_variables(int(request_variables['purchasePrice']))
    request_variables['financedAmount'] = financedAmount    
    request_variables['cash'] = cash
    request_variables['points'] = points
    
    # Parse the JSON string into a dictionary
    default_json = json.loads(default_json)
    
    # Append the variables in request_variables to the default_json
    for key in request_variables:
        default_json[key] = request_variables[key]
    
    # Convert the updated dictionary back to a JSON string
    json_body = json.dumps(default_json, indent=4)
    
    return json_body


def set_siteID(request_variables):
    if 'brand' in request_variables and request_variables['brand'] == 'HICV':
        request_variables['siteId'] = HICV_siteId        
    elif 'brand' in request_variables and request_variables['brand'] == 'KIMPTON':
        request_variables['siteId'] = KC_siteId
    else:
        print("Brand not found in request_variables")
        Exception("Brand not found in request_variables")
    return request_variables


def set_contractId():
    
    contractId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))
    return contractId


def set_variables(purchasePrice):
    random.shuffle(FINANCED_AMT)
    financedAmount = int(FINANCED_AMT[0])

    random.shuffle(POINTS)
    points = int(POINTS[0])

    cash = purchasePrice - financedAmount
    return financedAmount, cash, points


""" 
json_body = ''
with open(r"C:\\Users\\e087261\\VS_Code\\ClosingCost_RF_Automation\\config\\testData\\request_template.json", 'r') as file:
    json_body = file.read()


request_variables = {'purchasePrice': '100000', 'saleType': 'sales refinance', 'state': 'TX', 'brand': 'HICV'}


print(create_input_json(json_body, request_variables)) """

import json
import random
import string
from datetime import datetime, timedelta

siteId_file_path = "config/site_ids.json"

KC_siteId = "37"
HICV_siteId = "9999"
#FINANCED_AMT = ["30000", "40000", "50000", "60000", "70000", "80000"]
CASH = ["10000", "20000", "30000"]
FINANCED_AMT = ["10", "20", "40", "110"]
POINTS = ["100000", "100500", "30000", "40000", "50500"]
NO_OF_PURCHASERS = [3, 4, 5, 6]

def create_input_json(default_json, request_variables):
    
    contractId = set_contractId()
    purchase_price = request_variables.get('purchasePrice', None)
    request_variables['contractId'] = contractId
    if request_variables['brand'] == 'Kimpton':
            finance_amt = int(FINANCED_AMT[random.randint(0, len(FINANCED_AMT)-1)]) * int(request_variables['purchasePrice']) / 100
            kimpton_data = {
                "contractId": contractId,
                "siteId": KC_siteId,
                "brand": "KIMPTON",
                "purchasePrice": request_variables['purchasePrice'],
                "financedAmount": int(finance_amt),
                "cash": int(request_variables['purchasePrice']) - int(finance_amt),
            }
            #create a json out of kimpton data 
            default_json = json.dumps(kimpton_data, indent=4)
            return default_json          
            

    sale_type = request_variables.get('saleType', '').lower()
    financedAmount, cash, points, numberOfPurchasers = set_variables(int(request_variables['purchasePrice']))
    request_variables['financedAmount'] = financedAmount    
    request_variables['cash'] = cash
    request_variables['points'] = points
    request_variables['numberOfPurchasers'] = numberOfPurchasers
    
    if sale_type in ['sales refinance', 'loan refinance']:        
        request_variables = set_siteID(request_variables)
    else:
        
        if request_variables['brand'] == 'HICV':
            request_variables['siteId'] = HICV_siteId
        else:
            raise ValueError("Brand not recognized. Please use 'Kimpton' or 'HICV'.")        


    # Parse the JSON string into a dictionary
    default_json = json.loads(default_json)
    
    # Append the variables in request_variables to the default_json
    for key in request_variables:
        default_json[key] = request_variables[key]
    
    # Convert the updated dictionary back to a JSON string
    json_body = json.dumps(default_json, indent=4)
    #append previous policy data if required
    if sale_type in ['sales refinance', 'loan refinance']:
        policy_json_body = set_previous_policy(json.loads(json_body), purchase_price)
        if policy_json_body:
            #append the previous policy data to the json_body
            json_body = json.dumps(policy_json_body, indent=4)
    return json_body


def set_siteID(request_variables):
    if 'brand' in request_variables and request_variables['brand'] == 'HICV':
        # Load the JSON data
        with open(siteId_file_path, 'r') as file:
            data = json.load(file)
        
        state = request_variables.get('state')
        if not state:
            raise ValueError("State is required for HICV brand")
        
        # Directly get the site IDs for the given state
        state_site_ids = data.get(state)
        if not state_site_ids:
            raise ValueError(f"No site IDs found for state: {state}")
        
        # Set site ID - random if multiple, single if only one
        request_variables['siteId'] = random.choice(state_site_ids) if len(state_site_ids) > 1 else state_site_ids[0]
    elif 'brand' in request_variables and request_variables['brand'].upper() == 'KIMPTON':
        request_variables['siteId'] = KC_siteId
    else:
        print("Brand not found in request_variables")
        raise Exception("Brand not found in request_variables")
    return request_variables


def set_contractId():    
    contractId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))
    return contractId


def set_variables(purchasePrice):
    random.shuffle(FINANCED_AMT)
    # Get a random financed % from the list & caluculate amount like 10% of purchase price
    financedAmount = int(FINANCED_AMT[0]) * purchasePrice / 100

    random.shuffle(POINTS)
    points = int(POINTS[0])

    random.shuffle(NO_OF_PURCHASERS)
    numberOfPurchasers = NO_OF_PURCHASERS[0]

    if financedAmount > purchasePrice:
        cash_percentages = [5, 8, 9, 10, 12, 13]
        cash = (random.choice(cash_percentages) * purchasePrice) / 100
    else:
        cash = purchasePrice - financedAmount
    return financedAmount, cash, points, numberOfPurchasers


def generate_previous_policy_data(purchase_price):
    """Generate data for a previous policy"""
    org_purchase_price = purchase_price
    policy_id = random.randint(1000, 9999)

    # Generate dates
    today = datetime.today()    
    # Generate base date for calculations using random choice between different year ranges
    year_ranges = [
        (0, 365),        # less than 1 year
        (365, 3*365),    # 1-3 years
        (3*365, 5*365),  # 3-5 years
        (5*365, 8*365),  # 5-8 years
        (8*365, 15*365)  # greater than 8 years
    ]
    days_range = random.choice(year_ranges)
    base_date = today - timedelta(days=random.randint(days_range[0], days_range[1]))
    
    # TSW deeded date - Add parameter to control this
    #include_tsw_date = random.choice([True, False])
    
    # Earlier dates
    purchase_date = base_date - timedelta(days=random.randint(0, 150))
    policy_issue_date = base_date - timedelta(days=random.randint(50, 150))
    
    """ if not include_tsw_date:
        return {
        "contractNumber": policy_id,
        "purchasePrice": org_purchase_price,
        "purchaseDate": purchase_date.strftime("%Y-%m-%d"),
        "amountFinanced": org_purchase_price,
        "principalBalancePayDown": random.randint(100, 999),
        "policyIssueDate": policy_issue_date.strftime("%Y-%m-%d")
        }
    else: """
    tsw_deeded_date = base_date.strftime("%Y-%m-%d")       

    return {
            "contractNumber": policy_id,
            "purchasePrice": org_purchase_price,
            "purchaseDate": purchase_date.strftime("%Y-%m-%d"),
            "tswDeededDate": tsw_deeded_date,
            "amountFinanced": org_purchase_price,
            "principalBalancePayDown": random.randint(100, 9999),
            "policyIssueDate": policy_issue_date.strftime("%Y-%m-%d")
    }

def set_previous_policy(request_variables, purchase_price):
    
    request_variables["hasPreviousPolicy"] = True
    request_variables["fundingInstitution"] = "OLCC"
    request_variables["previousPolicy"] = generate_previous_policy_data(purchase_price)
    
    return request_variables

# Example usage:
# if previous_policy_is_true:
#     request_variables["fundingInstitution"] = "SL"
#     request_variables["previousPolicy"] = generate_previous_policy()

""" json_body = ''
with open(r"C:\\Users\\e087261\\VS_Code\\ClosingCost_RF_Automation\\config\\request_template.json", 'r') as file:
    json_body = file.read()


request_variables = {'purchasePrice': '100000', 'saleType': 'sales refinance', 'state': 'TX', 'brand': 'HICV'}


print(create_input_json(json_body, request_variables)) 
 """
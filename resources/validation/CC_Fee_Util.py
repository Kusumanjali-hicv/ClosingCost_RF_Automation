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
    logger.info("<span style='color:blue'>\nFee Names: " + str(fee_names) + "</span>", html=True)
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
        if feeName.lower() in json_response['closingCosts']['fees'][i]['description'].lower():
           
           amount = json_response['closingCosts']['fees'][i]['amount']
           payableTo = json_response['closingCosts']['fees'][i]['payableTo']
           description = json_response['closingCosts']['fees'][i]['description']
 
           logger.info("<span style='color:blue'>\nFee_Name: " + str(description) + 
                    " \nAmount: " + str(amount) + " \tPayable To: " + str(payableTo) + 
                    "</span>", html=True)
           return amount, description, payableTo 
       
    logger.info("<span style='color:red'>Fee not found: " + str(feeName) + "</span>", html=True)
    return amount, description, payableTo    

def get_lenders_title_policy_fee(feeName, json_response):
    amount = 0
    payableTo = ""
    description = ""
    
    if isinstance(json_response, dict):
        json_response = json_response
    else:
        json_response = json.loads(json_response)

    for fee in json_response['closingCosts']['fees']:
        if feeName.lower() in fee['description'].lower():
            # Skip if amount is 25.0
            if fee['amount'] == 25.0:
                continue

            amount = fee['amount']
            payableTo = fee['payableTo']
            description = fee['description']
            
    
    if not amount:
        #logger.info("<span style='color:gray'>" + str(feeName) + " paid by Developer not found  </span>", html=True)
        return 0, "", ""
    
    return amount, description, payableTo 


def round_up_to_nearest_100(value):
    # Round up to the nearest 100
    if value % 100 == 0:
        return value
    else:
        return ((value // 100) + 1) * 100

def round_up_to_nearest_1000(value):
    # Round up to the nearest 1000
    if value % 1000 == 0:
        return value
    else:
        return ((value // 1000) + 1) * 1000
""" 
Round Up To Nearest 100
    [Arguments]        ${Value}
    ${REMAINDER}=    Evaluate    ${Value} % 100
    ${ROUNDED}=    Evaluate    ${Value} + (100 - ${REMAINDER}) if ${REMAINDER} > 0 else ${Value}
    RETURN    ${ROUNDED} """


#print(getFeeDetails("Deed Of Trust Release Fee-TX", "{\"closingCosts\":{\"titleInsuranceFee\":0.00,\"fees\":[{\"amount\":53.50,\"description\":\"Deed Recording Fee\",\"transactionCode\":\"Deed Recording Fee\",\"payableTo\":\"Orange County Comptroller\"},{\"amount\":575.00,\"description\":\"Owner's Title Fee\",\"transactionCode\":\"Owner's Title Fee\",\"payableTo\":\"Wilson Title Services, LLC\"},{\"amount\":0.00,\"description\":\"Intangible Tax - Note\",\"transactionCode\":\"Intangible Tax - Note\",\"payableTo\":\"Orange County Comptroller\"},{\"amount\":25.00,\"description\":\"Lender's Title Insurance\",\"transactionCode\":\"Lender's Title Insurance\",\"payableTo\":\"Wilson Title Services\"},{\"amount\":70.00,\"description\":\"Documentary Stamps - Mortgage\",\"transactionCode\":\"Documentary Stamps - Mortgage\",\"payableTo\":\"Orange County Comptroller\"},{\"amount\":199.00,\"description\":\"Club Membership Fee\",\"transactionCode\":\"Club Membership Fee\",\"payableTo\":\"Club Membership Fee\"},{\"amount\":169.00,\"description\":\"Club Enrollment Fee\",\"transactionCode\":\"Club Enrollment Fee\",\"payableTo\":\"Club Enrollment Fee\"},{\"amount\":389.00,\"description\":\"Club Registration Fee\",\"transactionCode\":\"Club Registration Fee\",\"payableTo\":\"Club Registration Fee\"},{\"amount\":100.00,\"description\":\"HOA Set Up Fee\",\"transactionCode\":\"HOA Set Up Fee\",\"payableTo\":\"Orange Lake Trust Owners’ Association\"},{\"amount\":130.00,\"description\":\"Document Preparation Fee - Refinance\",\"transactionCode\":\"Document Preparation Fee - Refinance\",\"payableTo\":\"Holiday Inn Club Vacations Incorporated\"},{\"amount\":399.00,\"description\":\"Origination Fee - Refinance\",\"transactionCode\":\"Origination Fee - Refinance\",\"payableTo\":\"Holiday Inn Club Vacations Incorporated\"},{\"amount\":371.00,\"description\":\"Maintenance Fee\",\"transactionCode\":\"Maintenance Fee\",\"payableTo\":\"Maintenance Fee\"},{\"amount\":4.00,\"description\":\"Guarantee Fee-TX\",\"transactionCode\":\"Guarantee Fee-TX\",\"payableTo\":\"Texas Title Guaranty Association\"},{\"amount\":0.00,\"description\":\"Escrow Fee-AZ\",\"transactionCode\":\"Escrow Fee-AZ\",\"payableTo\":\"Wilson Title Agency Services, LLC\"},{\"amount\":37.00,\"description\":\"Deed Of Trust Recording Fee-TX\",\"transactionCode\":\"Deed Of Trust Recording Fee-TX\",\"payableTo\":\"Montogomery County Clerk's Office\"},{\"amount\":29.00,\"description\":\"Deed Of Trust Release Fee-TX\",\"transactionCode\":\"Deed Of Trust Release Fee-TX\",\"payableTo\":\"Montogomery County Clerk's Office\"}],\"grandTotal\":2550.50,\"documentaryStamps\":0.00,\"escrowAgentFee\":0.00,\"intangibleTax\":0.00},\"contractId\":\"FS50MJ9VB5W0I7X6DT\",\"siteId\":\"9999\",\"brand\":\"HICV\"}"))



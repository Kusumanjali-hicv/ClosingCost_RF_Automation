from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword

FEE_NAME = "Deed Of Trust Recording Fee"


@keyword
def compute_deed_of_trust_recording_fee(request_dict, api_response):
    sale_type = request_dict['saleType']
    state = request_dict['state']
    no_of_purchasers = request_dict['numberOfPurchasers']
    
    # Initialize fee details with defaults
    fee = 0
    PAYABLE_TO = ""
    fee_name = ""  
    
    if sale_type in ["Sales Refinance", "Loan Refinance"]:
        if state == "AZ": 
            fee = 30.00
            fee_name = FEE_NAME + "-AZ"
            PAYABLE_TO = "Maricopa County Recorder's Office"
             
        elif state == "GA":
            fee = 25.00
            fee_name = FEE_NAME + "-GA"
            PAYABLE_TO = "Habersham County Recorder's Office"
            
        elif state == "MO":      
            PAGES = 6     
            fee_name = FEE_NAME +"-MO" 
            fee = 24.00 + 3 * (PAGES - 1)  #Calculated fee: $24 for the first page plus $3 for each additional no_of_purchasers.
            PAYABLE_TO = "Taney County Recorder's Office"
            
        elif state == "NV":
            # Expecting a location field in the request.
            location = request_dict['location']
            fee_name = FEE_NAME + "-NV"
            nevada_fee_config = {
                "CLARK COUNTY (DESERT CLUB)": (42.00, "Clark County, Office of the County Recorder"),
                "DOUGLAS COUNTY (WALLY'S)": (40.00, "Clark County, Office of the County Recorder"),
                "DOUGLAS COUNTY (RIDGE)": (40.00, "Clark County, Office of the County Recorder"),
            }

            if location in nevada_fee_config:
                fee, PAYABLE_TO = nevada_fee_config[location]
                logger.info(f"Flat fee of ${fee} for {location} in Nevada.")
            else:
                logger.error(f"Location '{location}' is not recognized for Nevada fees.")
        
        elif state == "SC":
            fee = 25.00
            fee_name = FEE_NAME + "-SC"
            PAYABLE_TO = "Horry County, SC Registry of Deeds"
            
        elif state == "TN":
            PAGES = 3
            fee_name = FEE_NAME + "-TN"
            if PAGES > 2:
                fee = 12.00 + 1 + 5 * (PAGES - 2)
            else:
                fee = 12.00 + 1
            PAYABLE_TO = "Sevier County, Register of Deeds"
            
        elif state == "TX":
            fee_name = FEE_NAME + "-TX"
            base_fee = 25.00
            PAGES = 4
            #page is configured in Pega
            additional_page_fee = 4 * max(0, PAGES - 1)
            extra_name_fee = 0.25 * max(0, no_of_purchasers - 5)
            fee = base_fee + additional_page_fee + extra_name_fee
            PAYABLE_TO = "Montogomery County Clerk's Office"
            
        elif state == "VT":
            PAGES = 1
            fee_name = FEE_NAME + "-VT"
            fee = 10.00 * PAGES
            PAYABLE_TO = "West Windsor Town Clerk"
            
        elif state == "VA":
            fee_name = FEE_NAME + "-VA"
            PAYABLE_TO = "York County Circuit Court"
            fee = 46.00
            
        else:
            logger.info(f"No fee configuration for state: {state}")
            return
    elif sale_type in ["New", "Downgrade", "Reload", "Reload Equity", "Reload New Money", "Rewrite", "Upgrade"]:
        PAGES = 3 #config in pega
        #Assessed on Mortgage accounts only. $10.00 for the 1st page, each additional page will be 8.50 , in addition if there are more than 3 purchasers on the contract an additional $1.00 will be added for each additional purchaser. 
        fee = 10.00 + 8.50 * (PAGES - 1) + 1 * max(0, no_of_purchasers - 3)
        fee_name = FEE_NAME+"-Trust"
        PAYABLE_TO = "Orange County Comptroller"


    else:
        logger.info(f"Fee not applicable for sale type: {sale_type}")
        return

    # Retrieve fee details from response
    amount, description, payableTo = getFeeDetails(fee_name, api_response)
    #assert the fee & list the errors
    errors = assert_doc_stamp_deed_fee(
        amount, description, fee_name, payableTo, sale_type,
        fee, PAYABLE_TO
    )
    if errors:
        for error in errors:
            logger.error(error, html=True)
        raise AssertionError("\n".join(errors))
    else:
        logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)

def  assert_doc_stamp_deed_fee(amount, description, FEE_NAME, payableTo, sale_type, exp_fee, exp_payableTo):
    errors = []

    if amount != exp_fee:
        msg = (f"<span style='color:red'>{FEE_NAME} amount mismatch for {sale_type}: "
               f"Expected {exp_fee}, but got {amount}</span>")
        errors.append(msg)

    if description != FEE_NAME:
        msg = (f"<span style='color:red'>{FEE_NAME} description mismatch for {sale_type}: "
               f"Expected '{FEE_NAME}', but got '{description}'</span>")
        errors.append(msg)

    if payableTo != exp_payableTo:
        msg = (f"<span style='color:red'>{FEE_NAME} payableTo mismatch for {sale_type}: "
               f"Expected '{exp_payableTo}', but got '{payableTo}'</span>")
        errors.append(msg)

    return errors


    



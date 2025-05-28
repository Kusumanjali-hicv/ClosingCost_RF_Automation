from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword

FEE_NAME = "Deed Of Trust Release Fee"

@keyword
def compute_deed_of_trust_release_fee(request_dict, api_response):
    sale_type = request_dict['saleType']
    state = request_dict['state']
    no_of_purchasers = request_dict['numberOfPurchasers']
    location = request_dict.get('location', "").upper()
    

    # Initialize fee details with defaults
    fee = 0
    PAYABLE_TO = ""

    if sale_type in ["Sales Refinance", "Loan Refinance"]:

        # State-specific fee calculations
        state_fee_config = {
            "AZ": (30.00, "Maricopa County Recorder's Office"),
            "GA": (25.00, "Habersham County Recorder's Office"),
            "SC": (10.00, "Horry County, SC Registry of Deeds"),
            "VA": (46.00, "York County Circuit Court"),
        }

        if state in state_fee_config:
            fee, PAYABLE_TO = state_fee_config[state]

        elif state == "MO":
            PAGES = 1
            fee = 24.00 + 3 * (PAGES - 1)# + 5 * (no_of_purchasers - 1)
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

        elif state == "TN":
            PAGES = 2
            fee = 12.00 + 5 * max(0, PAGES - 2)
            PAYABLE_TO = "Sevier County, Register of Deeds"

        elif state == "TX":
            PAGES = 2
            base_fee = 25.00
            additional_page_fee = 4 * max(0, PAGES - 1)
            extra_name_fee = 0.25 * max(0, no_of_purchasers - 5)
            fee = base_fee + additional_page_fee + extra_name_fee
            PAYABLE_TO = "Montogomery County Clerk's Office"

        elif state == "VT":
            PAGES = 1
            fee = 10.00 * PAGES
            PAYABLE_TO = "West Windsor Town Clerk"

        else:
            logger.info(f"No fee configuration for state: {state}")
            return

        fee_name = f"{FEE_NAME}-{state}"
    elif sale_type in ["New", "Downgrade", "Reload", "Reload Equity", "Reload New Money", "Rewrite", "Upgrade"]:
        PAGES = 3 #config in pega
        fee = 10.00 + 8.50 * (PAGES - 1) + 1 * max(0, no_of_purchasers - 3)
        fee_name = FEE_NAME+"-Trust"
        PAYABLE_TO = "Orange County Comptroller"

    
    # Retrieve fee details from response
    amount, description, payableTo = getFeeDetails(fee_name, api_response)

    # Assert the fee and list the errors
    errors = assert_release_fee(
        amount, description, fee_name, payableTo,
        sale_type, fee, PAYABLE_TO
    )
    if errors:
        for error in errors:
            logger.error(error, html=True)
        raise AssertionError("\n".join(errors))
    else:
        logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)


def assert_release_fee(amount, description, FEE_NAME, payableTo, sale_type, exp_fee, exp_payableTo):
    errors = []

    if amount != exp_fee:
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
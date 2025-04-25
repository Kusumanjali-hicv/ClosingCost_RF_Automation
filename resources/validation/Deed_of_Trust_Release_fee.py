from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword

FEE_NAME = "Deed of Trust Release Fee"

@keyword
def compute_deed_of_trust_release_fee(request_dict, api_response):
    sale_type = request_dict['saleType']
    state = request_dict['state']
    pages = request_dict.get('numberOfPages', 1)
    references = request_dict.get('numberOfReferences', 1)
    location = request_dict.get('location', "").upper()

    # Initialize fee details with defaults
    fee = 0
    PAYABLE_TO = ""

    if sale_type in ["Sales refinance", "Loan refinance"]:
        if state == "AZ":
            fee = 30.00  # Flat fee of $30 for Arizona
            PAYABLE_TO = "Maricopa County Recorder's Office"

        elif state == "GA":
            fee = 25.00  # Flat fee of $25 for Georgia
            PAYABLE_TO = "Habersham County Recorder's Office"

        elif state == "MO":
            fee = 24.00 + 3 * (pages - 1) + 5 * (references - 1)  # $24 for the first page, $3 for each additional page, $5 for each additional reference
            PAYABLE_TO = "Taney County Recorder's Office"

        elif state == "NV":
            if "CLARK" in location:
                fee = 42.00  # Flat fee of $42 for Clark County
                PAYABLE_TO = "Clark County, Office of the County Recorder"
            elif "DOUGLAS" in location:
                fee = 40.00  # Flat fee of $40 for Douglas County
                PAYABLE_TO = "Clark County, Office of the County Recorder"
            else:
                logger.error(f"Location '{location}' is not recognized for Nevada fees.")

        elif state == "SC":
            fee = 10.00  # Flat fee of $10 for South Carolina
            PAYABLE_TO = "Horry County, SC Registry of Deeds"

        elif state == "TN":
            fee = 12.00 + 5 * max(0, pages - 2)  # $12 for the first 2 pages, $5 for each additional page
            PAYABLE_TO = "Sevier County, Register of Deeds"

        elif state == "TX":
            base_fee = 25.00
            additional_page_fee = 4 * max(0, pages - 1)
            extra_name_fee = 0.25 * max(0, request_dict.get("names_count", 5) - 5)
            fee = base_fee + additional_page_fee + extra_name_fee
            PAYABLE_TO = "Montogomery County Clerk's Office"

        elif state == "VT":
            fee = 10.00 * pages  # $10 per page
            PAYABLE_TO = "West Windsor Town Clerk"

        elif state == "VA":
            fee = 46.00  # Flat fee of $46 for Virginia
            PAYABLE_TO = "York County Circuit Court"

        else:
            logger.info(f"No fee configuration for state: {state}")
    else:
        logger.info(f"Fee not applicable for sale type: {sale_type}")

    # Retrieve fee details from response
    amount, description, payableTo = getFeeDetails(FEE_NAME, api_response)

    # Assert the fee and list the errors
    errors = assert_release_fee(
        amount, description, FEE_NAME, payableTo,
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
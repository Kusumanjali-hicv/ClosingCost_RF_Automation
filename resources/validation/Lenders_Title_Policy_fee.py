from robot.api import logger
from CC_Fee_Util import getFeeDetails, round_up_to_nearest_100, round_up_to_nearest_1000, get_amount_from_rate_chart
from robot.api.deco import keyword
from datetime import datetime


FEE_NAME = "Lenders Title Policy"
PAYABLE_TO = "Wilson Title Agency Services, LLC"

def compute_lenders_title_policy_fee(request_dict, api_response):
    state = request_dict['state']
    sale_type = request_dict['saleType']
    financed_amount = float(request_dict['financedAmount'])
    purchase_price = float(request_dict['purchasePrice'])
    fee = 0

    if sale_type in ["Sales Refinance", "Loan Refinance"]:
        if state == "AZ":
            fee = 356.00
        
        elif state == "GA":
            if financed_amount <= 100000:
                fee = 200.00
            elif financed_amount <= 500000:
                fee = 200.00 + (2.25 * (financed_amount - 100000) / 1000)
                
        
        elif state == "IL":
            fee = 150.00
        
        elif state == "FL":
            # Florida calculation with reissue/original rate logic
            loan_amt = float(round_up_to_nearest_1000(financed_amount))
            orig_price = float(request_dict.get("previousPolicy", {}).get("orgPurchasePrice", 0))
            if orig_price:
                orig_price = round_up_to_nearest_1000(orig_price)
            else:
                orig_price = 0
            fee = 0
            tsw_deeded_date = request_dict.get("previousPolicy", {}).get("tswDeededDate", None)
            tsw_deeded_date = datetime.strptime(tsw_deeded_date, "%Y-%m-%d")
            today = datetime.today()

            if  orig_price != 0:
                #if (today - tsw_deeded_date).days > 1095:         
                    # --- Reissue Rate Calculation ---
                    if loan_amt <= orig_price:
                        # Case 1: Financed Amount < Original Purchase Price
                        if loan_amt <= 100000:
                            fee = (loan_amt / 1000) * 3.30
                        elif loan_amt > 100000:
                            fee = (100000 / 1000) * 3.30 + ((loan_amt - 100000) / 1000) * 3.00
                    else:
                        # Case 2: Financed Amount > Original Purchase Price
                        # First, apply reissue rate up to original purchase price
                        if orig_price <= 100000:
                            fee = (purchase_price / 1000) * 3.30
                        elif orig_price > 100000:
                            fee = (100000 / 1000) * 3.30 + ((purchase_price - 100000) / 1000) * 5.75
                                              
            # Minimum premium
            fee = max(60, fee)     

        elif state == "MO":
            funding_institution = request_dict.get('fundingInstitution', None)
            if not funding_institution:
                logger.error("fundingInstitution is required for MO state")
                return
            loan_amt = round_up_to_nearest_1000(financed_amount)
            fee = 0

            if funding_institution == "SL":
                logger.info("Funding institution is SL, No prior policy was issued so charge full premium amount.")
                # Calculate fee without prior policy
                if loan_amt <= 50000:
                    fee = (loan_amt / 1000) * 1.00
                elif loan_amt <= 100000:
                    fee = (50000 / 1000) * 1.00 + ((loan_amt - 50000) / 1000) * 0.80
                elif loan_amt <= 5000000:
                    fee = (50000 / 1000) * 1.00 + (50000 / 1000) * 0.80 + ((loan_amt - 100000) / 1000) * 0.70

            elif funding_institution == "OLCC":
                logger.info("Funding institution is OLCC, Prior Policy issue date is the deeded date in TSW.")
                # Calculate fee with prior policy
                if loan_amt <= 50000:
                    fee = (loan_amt / 1000) * 0.60
                elif loan_amt <= 100000:
                    fee = (50000 / 1000) * 0.60 + ((loan_amt - 50000) / 1000) * 0.48
                elif loan_amt <= 5000000:
                    fee = (50000 / 1000) * 0.60 + (50000 / 1000) * 0.48 + ((loan_amt - 100000) / 1000) * 0.42

            # Apply minimum fee
            fee = max(4.00, fee)


        elif state == "SC":
            loan_amt = round_up_to_nearest_100(financed_amount)
            tiers = [
                (50000, 3.60),
                (100000, 3.00),
                (500000, 2.10),
                (5000000, 1.80)
            ]
            fee = 0
            prev_limit = 0
            remaining = loan_amt
            for limit, rate in tiers:
                slab = min(remaining, limit - prev_limit)
                if slab > 0:
                    fee += (slab / 1000) * rate
                    remaining -= slab
                prev_limit = limit
                if remaining <= 0:
                    break
            # Minimum premium
            fee = max(75.00, fee)

        elif state == "TN":
            fee = 150.00

        elif state == "VA":
            loan_amt = round_up_to_nearest_1000(financed_amount)            
            fee = max(60.00, loan_amt * 0.0029)
        
        elif state == "TX":
            loan_amt = financed_amount
            FTP = get_amount_from_rate_chart(request_dict['siteId'], loan_amt)
            if FTP is None:
                logger.error("Failed to get rate chart amount for loan amount")
                return
            principal_balance = request_dict.get("previousPolicy", {}).get("principalBalancePayDown", 0)
            credit = get_amount_from_rate_chart(request_dict['siteId'], principal_balance) or 0
            LTP = FTP - credit
            funding_institution = request_dict.get('fundingInstitution', None)
            if funding_institution != "SL":
                logger.info("Funding institution is {funding_institution}, Prior Policy issue date is the deeded date in TSW.")
                tsw_deeded_date = request_dict.get("previousPolicy", {}).get("tswDeededDate", None)
                tsw_deeded_date = datetime.strptime(tsw_deeded_date, "%Y-%m-%d")
                today = datetime.today()
                # if the deeded date is 0 - 4 years ago – 50% of LTP 
                if tsw_deeded_date and (today - tsw_deeded_date).days <= 1460:
                    fee = LTP * 0.5
                #if the deeded date is 5 - 8 years ago – 25% of LTP
                elif tsw_deeded_date and (today - tsw_deeded_date).days <= 2920:
                    fee = LTP * 0.25
                #Old Policy issued more than 8 years ago? LTP: Take the loan amount and refer to the rate chart; Round down
                elif tsw_deeded_date and (today - tsw_deeded_date).days > 2920:
                    fee = FTP
                # No outstanding loan balance? LTP: Take the loan amount and refer to the rate chart; Round down.
                elif principal_balance == 0:
                    fee = FTP
                else:
                    #OLCC loans: Prior Policy issue date is the deeded date in TSW. No deeded date in TSW? Charge full premium amount.
                    logger.info("OLCC loans: Prior Policy issue date is the deeded date in TSW. No deeded date in TSW? Charge full premium amount.")
                    fee = FTP
            elif funding_institution == "SL":
                #No previous policy was issued so charge full premium amount.
                logger.info("Funding institution is SL, No prior policy was issued so charge full premium amount.")
                fee = FTP
            else:
                logger.error("fundingInstitution is not specified or invalid for TX state", funding_institution)
                return
                
            #  IF THE POLICY CALCULATES TO LESS THAN $328, THEN CHARGE $328 (MINIMUM CHARGE)            
            fee = max(328.00, fee)
                

        else:
            logger.error(f"No Lenders Title Policy fee configuration for state: {state}")
            return

        # Retrieve fee details from response
        fee_name = FEE_NAME # + f"-{state}"
        fee = round(fee, 2)
        amount, description, payableTo = getFeeDetails(fee_name, api_response)

        # Assert the fee and list the errors
        errors = assert_lenders_title_policy_fee(
            amount, description, fee_name, payableTo,
            sale_type, fee, PAYABLE_TO
        )
        if errors:
            for error in errors:
                logger.error(error, html=True)
            raise AssertionError("\n".join(errors))
        else:
            logger.info(f"<span style='color:green'>{FEE_NAME} assertion passed</span>", html=True)


def assert_lenders_title_policy_fee(amount, description, FEE_NAME, payableTo, sale_type, exp_fee, exp_payableTo):
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

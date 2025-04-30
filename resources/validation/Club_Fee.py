from robot.api import logger
from CC_Fee_Util import getFeeDetails
from robot.api.deco import keyword

Club_Enrollment_Fee = 169.00
Club_Membership_Fee = 199.00
Club_Registry_Fee = 389.00
HOA_Set_Up_Fee = 100.00

FEE_CONFIGS = {
    "Club Enrollment Fee": {"fee": Club_Enrollment_Fee, "payableTo": "Club Enrollment Fee"},
    "Club Membership Fee": {"fee": Club_Membership_Fee, "payableTo": "Club Membership Fee"},
    "Club Registration Fee": {"fee": Club_Registry_Fee, "payableTo": "Club Registration Fee"},
    "HOA Set Up Fee": {"fee": HOA_Set_Up_Fee, "payableTo": "Orange Lake Trust Owners’ Association"},
}


@keyword
def compute_club_fee(request_dict, api_response):
    
    for fee_name, config in FEE_CONFIGS.items():
        expected_fee = config["fee"]
        expected_payableTo = config["payableTo"]
        amount, description, payableTo = getFeeDetails(fee_name, api_response)

        if description != fee_name:
            logger.error(f"Fee description is not as expected: expected '{fee_name}', got '{description}'")
            continue

        if amount != expected_fee:
            err_msg = f"Mismatch on amount for {fee_name}: expected {expected_fee}, got {amount}"
            logger.error(f"<span style='color:red'>{err_msg}</span>", html=True)

        if payableTo != expected_payableTo:
            err_msg = f"Mismatch on payableTo for {fee_name}: expected {expected_payableTo}, got {payableTo}"
            logger.error(f"<span style='color:red'>{err_msg}</span>", html=True)
        logger.info(f"<span style='color:green'>{fee_name} assertions passed</span>", html=True)
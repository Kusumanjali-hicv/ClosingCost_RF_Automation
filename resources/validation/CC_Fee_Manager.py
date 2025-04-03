import json
from  Guarantee_Fee import  compute_guarantee_fee
from  Title_Search_Fee import  compute_title_search_fee
from Escrow_Fee import compute_escrow_fee
from Origination_Fee import compute_origination_fee
from Document_Preparation_Fee import compute_document_preparation_fee
from Owner_Title_Fee import compute_owner_title_fee
from Intangiable_Tax_Note import compute_intangible_tax_note
from Mortgage_Recording_Fee import compute_mortgage_recording_fee
from Doc_Stamp_Deed_Trust_fee import compute_doc_stamp_deed_fee
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

@keyword
def  assert_expected_cc_fee(fee_names, request_json, api_response):
    #log purchase price, financed amount, sale type, state & cash from request_json
    # Using ANSI escape codes for bold text
    logger.info("<b>Purchase Price : " + str(request_json['purchasePrice']) +
                "; Financed Amount : " + str(request_json['financedAmount']) + 
                "; Sale Type : " + request_json['saleType'] + 
                "; State : " + request_json['state'] + 
                "; Cash : " + str(request_json['cash']) + "</b>", html=True)

    if isinstance(request_json, dict):
        request_dict = request_json
    else:
        request_dict = json.loads(request_json)
    
    fee_functions = {
        "Guarantee Fee": compute_guarantee_fee,
        "Title Search Fee": compute_title_search_fee,
        "Escrow Fee": compute_escrow_fee,
        "Origination Fee": compute_origination_fee,
        "Document Preparation Fee": compute_document_preparation_fee,
        "Owner's Title Fee": compute_owner_title_fee,
        "Intangible Tax - Note": compute_intangible_tax_note,
        "Mortgage Recording Fee": compute_mortgage_recording_fee,
        "Documentary Stamps - Deed": compute_doc_stamp_deed_fee,
        
    }

    error_messages = []
    for fee in fee_functions:
        if fee in fee_names:
            try:
                fee_functions[fee](request_dict, api_response)
            except Exception as e:
                error_msg = f"{fee}: {e}"
                logger.error(error_msg)
                error_messages.append(error_msg)
    if error_messages:
        BuiltIn().fail("\nErrors encountered: " + "; ".join(error_messages))

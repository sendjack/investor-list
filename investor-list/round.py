"""
    Funding Round
    -------------

    A CrunchBase company's funding round.

"""

import json

from util.decorators import constant


class _Key(object):

    @constant
    def ROUND_CODE(self):
        return "round_code"

    @constant
    def RAISED_AMOUNT(self):
        return "raised_amount"

    @constant
    def RAISED_CURRENCY_CODE(self):
        return "raised_currency_code"

    @constant
    def FUNDED_DAY(self):
        return "funded_day"

    @constant
    def FUNDED_MONTH(self):
        return "funded_month"

    @constant
    def FUNDED_YEAR(self):
        return "funded_year"

    @constant
    def INVESTMENTS(self):
        return "investments"

    @constant
    def PERSON(self):
        return "person"

    @constant
    def FINANCIAL_ORG(self):
        return "financial_org"

    @constant
    def PERMALINK(self):
        return "permalink"

KEY = _Key()


class FundingRound(object):

    """Provide access to a CrunchBase company's FundingRound.

    Attributes:
    -----------
    category : string
    raised_amount : int
    curreny : string
    day : int
    month : int
    year : int
    investor_vc_links : list of strings
    investor_person_links: list of strings

    """

    def __init__(self, funding_round_dict):
        self.category = funding_round_dict.get(KEY.ROUND_CODE)
        self.raised_amount = funding_round_dict.get(KEY.RAISED_AMOUNT)
        self.currency = funding_round_dict.get(KEY.RAISED_CURRENCY_CODE)
        self.day = funding_round_dict.get(KEY.FUNDED_DAY)
        self.month = funding_round_dict.get(KEY.FUNDED_MONTH)
        self.year = funding_round_dict.get(KEY.FUNDED_YEAR)

        (vc_links, person_links) = self._get_permalinks(funding_round_dict)
        self.investor_vc_links = vc_links
        self.investor_person_links = person_links


    def __repr__(self):
        fields = {
                KEY.ROUND_CODE: self.category,
                KEY.RAISED_AMOUNT: self.raised_amount,
                KEY.RAISED_CURRENCY_CODE: self.currency,
                KEY.FUNDED_DAY: self.day,
                KEY.FUNDED_MONTH: self.month,
                KEY.FUNDED_YEAR: self.year,
                KEY.FINANCIAL_ORG: self.investor_vc_links,
                KEY.PERSON: self.investor_person_links
                }

        return json.dumps(fields, indent=4)


    def _get_permalinks(self, funding_round_dict):
        vc_list = []
        person_list = []
        for investor in funding_round_dict.get(KEY.INVESTMENTS):

            org_details = investor.get(KEY.FINANCIAL_ORG)
            if org_details is not None:
                vc_list.append(org_details.get(KEY.PERMALINK))

            person_details = investor.get(KEY.PERSON)
            if person_details is not None:
                person_list.append(person_details.get(KEY.PERMALINK))

        return (list(set(vc_list)), list(set(person_list)))

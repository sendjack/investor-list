"""
    Company
    -------

    A CrunchBase company.

"""

import json

from util.decorators import constant

from round import FundingRound


class _Key(object):

    @constant
    def NAME(self):
        return "name"

    @constant
    def CRUNCHBASE_URL(self):
        return "crunchbase_url"

    @constant
    def PERMALINK(self):
        return "permalink"

    @constant
    def FUNDING_ROUNDS(self):
        return "funding_rounds"

    @constant
    def CATEGORY_CODE(self):
        return "category_code"

KEY = _Key()


class Company(object):

    """Provide access to CrunchBase Company.

    Attributes:
    -----------
    name : string
    crunchbase_url : string
    permalink : string
    funding_rounds : list of FundingRounds
    industry : string

    """

    def __init__(self, company_dict):
        self.name = company_dict.get(KEY.NAME)
        self.crunchbase_url = company_dict.get(KEY.CRUNCHBASE_URL)
        self.permalink = company_dict.get(KEY.PERMALINK)

        self.funding_rounds = [
                FundingRound(funding_round_dict)
                for funding_round_dict in company_dict.get(KEY.FUNDING_ROUNDS)
                ]

        self.industry = company_dict.get(KEY.CATEGORY_CODE)


    def __repr__(self):
        fields = {
                KEY.NAME: self.name,
                KEY.CRUNCHBASE_URL: self.crunchbase_url,
                KEY.PERMALINK: self.permalink,
                KEY.CATEGORY_CODE: self.industry
                # TODO: including the rounds causes an error.
                #KEY.FUNDING_ROUNDS: self.funding_rounds
                }

        return json.dumps(fields, indent=4)


    def get_qualified_rounds(self, starting_year, category_filter):
        """Return a list of FundingRounds that fits the qualifications."""
        qualified_rounds = []

        for f in self.funding_rounds:
            date_cond = f.year >= starting_year
            category_cond = f.category in category_filter
            if date_cond and category_cond:
                qualified_rounds.append(f)

        return qualified_rounds

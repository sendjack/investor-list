#!/usr/bin/env python
"""
    CrunchBase Miner
    ----------------

    Poll CrunchBase using a company names list and then filter by finance round
    type and finance round date.

"""

import requests

from util.decorators import constant
from util import environment
from util.base_type import to_unicode

from company import Company
from investor import Investor


class _CrunchBase(object):

    @constant
    def CRUNCHBASE_API_BASE(self):
        return "http://api.crunchbase.com/v/1/"

    @constant
    def SEARCH_PATH(self):
        return "search.js"

    @constant
    def PERMALINK_EXT(self):
        return ".js"

    @constant
    def PATH_SEPARATOR(self):
        return "/"

    @constant
    def COMPANY(self):
        return "company"

    @constant
    def FINANCIAL_ORG(self):
        return "financial-organization"

    @constant
    def PARAM_API_KEY(self):
        return "api_key"

    @constant
    def PARAM_QUERY(self):
        return "query"

    @constant
    def ERROR(self):
        return "error"

    @constant
    def NAMESPACE(self):
        return "namespace"

    @constant
    def TOTAL(self):
        return "total"

    @constant
    def RESULTS(self):
        return "results"

    @constant
    def PERMALINK(self):
        return "permalink"

CB = _CrunchBase()

API_KEY = environment.get_unicode(u"CRUNCHBASE_API_KEY")
INPUT_DIR = environment.get_unicode(u"INPUT_DIR")
OUTPUT_DIR = environment.get_unicode(u"OUTPUT_DIR")

COMPANY_NAMES_FILE = environment.get_unicode(u"COMPANY_NAMES_FILE")
VC_NAMES_FILE = environment.get_unicode(u"VC_NAMES_FILE")
PERSON_NAMES_FILE = environment.get_unicode(u"PERSON_NAMES_FILE")

STARTUP_OUTPUT_FILE = environment.get_unicode(u"STARTUP_OUTPUT_FILE")
INVESTOR_OUTPUT_FILE = environment.get_unicode(u"INVESTOR_OUTPUT_FILE")

START_YEAR = environment.get_integer(u"START_YEAR")
ROUND_TYPES = environment.get_unicode(u"ROUND_TYPES").lower().split(",")


def generate_startup_list():
    """Filter the startup list by fundraising year and fundraising category,
    and write a csv with the qualified startups and info."""
    company_names_list = read_names_from_file(COMPANY_NAMES_FILE)
    year_filter = START_YEAR
    category_filter = ROUND_TYPES  # e.g., angel, seed

    companies = []
    for company_name in company_names_list:
        # If qualifying, get the Company from its name using CrunchBase.
        company = get_qualified_company(
                company_name,
                year_filter,
                category_filter)
        if company:
            companies.append(company)
        else:
            print "{} did not qualify.".format(company_name.encode('utf8'))

    write_startup_csv(companies, year_filter, category_filter)


def get_qualified_company(company_name, year_filter, category_filter):
    """Search CrunchBase for the company name and fundraising rounds, but only
    return companies whose fundraising rounds fit the year and category
    restrictions."""
    search_results = search_crunchbase(company_name)

    qualified_company = None
    # If search returned results and the first result is a company.
    if search_results and search_results[0].get(CB.NAMESPACE) == CB.COMPANY:
        search_result_dict = search_results[0]
        permalink = search_result_dict.get(CB.PERMALINK)

        # Use the permalink to get a more valuable Company object.
        company_dict = lookup_company_by_permalink(permalink)
        if company_dict:
            company = Company(company_dict)

            if company.get_qualified_rounds(year_filter, category_filter):
                qualified_company = company

    return qualified_company


def generate_investor_list():
    """Use a investor permalink list to generate a file with investor info."""
    investor_permalinks = read_names_from_file(VC_NAMES_FILE)

    investors = []
    for permalink in investor_permalinks:
        investor_dict = lookup_financial_org_by_permalink(permalink)
        investor = Investor(investor_dict)
        investors.append(investor)

    write_investor_csv(investors)


def search_crunchbase(company):
    """Use a company name to search crunchbase."""
    payload = {
            CB.PARAM_QUERY: company
            }

    response = get_from_crunchbase(CB.SEARCH_PATH, payload)
    search_results = None
    if response is not None and response.get(CB.TOTAL) >= 1:
        search_results = response.get(CB.RESULTS)

    return search_results


def lookup_company_by_permalink(permalink):
    """Use a CrunchBase permalink to lookup a company."""
    payload = {}

    path = CB.COMPANY + CB.PATH_SEPARATOR + permalink + CB.PERMALINK_EXT
    return get_from_crunchbase(path, payload)


def lookup_financial_org_by_permalink(permalink):
    """Use a CrunchBase permalink to lookup a financial organization."""
    payload = {}

    path = CB.FINANCIAL_ORG + CB.PATH_SEPARATOR + permalink + CB.PERMALINK_EXT
    return get_from_crunchbase(path, payload)


def get_from_crunchbase(path_extension, payload):
    """GET from CrunchBase."""
    url = CB.CRUNCHBASE_API_BASE + path_extension
    payload[CB.PARAM_API_KEY] = API_KEY

    r = requests.get(url, params=payload)

    response = None
    if r.json is None:
        print "CrunchBase Error: Empty JSON response from CB"
        print r.url
        response = None
    elif CB.ERROR in r.json.keys():
        print "CrunchBase Error: ", r.json.get(CB.ERROR)
        print r.url
        response = None
    else:
        response = r.json
    return response


def read_names_from_file(file_path):
    """Read strings from a file where each string is on a newline."""
    full_input_path = "{}/{}".format(INPUT_DIR, file_path)
    f = open(full_input_path, 'r')
    unique_company_names_dict = {
            unicode(line.strip(), 'utf-8'): None
            for line in f
            }
    return sorted(unique_company_names_dict.keys())


def write_startup_csv(companies, year_filter, category_filter):
    """Write a csv file with company and fundraising information."""
    startup_rows = []
    for company in companies:
        for round in company.get_qualified_rounds(
                year_filter,
                category_filter):
            row = [
                    company.name,
                    company.crunchbase_url,
                    company.permalink,
                    company.industry,
                    to_unicode(round.raised_amount),
                    round.year,
                    round.month,
                    round.category,
                    round.investor_vc_links,
                    round.investor_person_links
                    ]
            startup_rows.append(row)

    write_csv(STARTUP_OUTPUT_FILE, startup_rows)


def write_investor_csv(investors):
    """Write a csv file with investor information."""
    investor_rows = []
    for investor in investors:
        row = [
                investor.name,
                investor.crunchbase_url,
                investor.permalink,
                investor.homepage_url
                ]
        investor_rows.append(row)

    write_csv(INVESTOR_OUTPUT_FILE, investor_rows)


def write_csv(output_path, rows):
    full_output_path = "{}/{}".format(OUTPUT_DIR, output_path)
    f = open(full_output_path, 'w')
    for row in rows:
        # wrap items in quotes and join list items with newline character
        formatted_row = []
        for item in row:
            formatted_item = to_unicode(item)
            if type(item) == list:
                formatted_item = u"\n".join(item)
            formatted_item = u"\"{}\"".format(formatted_item)
            formatted_row.append(formatted_item)
        # join all items into a csv string
        printable_row = ",".join(formatted_row)
        f.write(printable_row.encode('utf8'))
        f.write("\n")

    f.close()


if __name__ == "__main__":
    generate_startup_list()
    #generate_investor_list()

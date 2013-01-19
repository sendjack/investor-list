"""
    Investor
    --------

    A CrunchBase investor.

"""

import json

from util.decorators import constant


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
    def HOMEPAGE_URL(self):
        return "homepage_url"

KEY = _Key()


class Investor(object):

    """Provide access to a CrunchBase Investor.

    Attributes:
    name : string
    crunchbase_url : string
    permalink : string
    homepage_url : string

    """

    def __init__(self, investor_dict):
        self.name = investor_dict.get(KEY.NAME)
        self.crunchbase_url = investor_dict.get(KEY.CRUNCHBASE_URL)
        self.permalink = investor_dict.get(KEY.PERMALINK)
        self.homepage_url = investor_dict.get(KEY.HOMEPAGE_URL)


    def __repr__(self):
        fields = {
                KEY.NAME: self.name,
                KEY.CRUNCHBASE_URL: self.crunchbase_url,
                KEY.PERMALINK: self.permalink,
                KEY.HOMEPAGE_URL: self.homepage_url
                }

        return json.dumps(fields, indent=4)

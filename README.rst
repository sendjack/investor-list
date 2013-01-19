===========================================================
Startup Investors: Investor lists for startups' fundraising
===========================================================

Given a list of company names, output a list of investors for each round of financing for that company.

Overview:
---------
Requires a list of company names, a list of fundraising round types, and a date
range for that financing. It searches CrunchBase for these companies, filters
appropriately, and returns back a file with a list of investors for each
company, by round.

Dependencies:
-------------
General
+++++++
- `Requests <http://docs.python-requests.org>`_: HTTP for Humans

App
+++
- `CrunchBase <http://developer.crunchbase.com>`_

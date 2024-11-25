# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "pricelist_temp",
    "summary": "",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/juanpgarza/sale-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
                "sale",
            ],
    "data": [
        'views/pricelist_temp_views.xml',
        'security/ir.model.access.csv',
        ],
    "installable": False,
}
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


class Requests:
    """
    Get Json from openfoodfacts.org and extracts product info from the json"""

    def __init__(self):
        self.all_products = []

    def get_json(self, category, cat_id):
        self.category = category
        self.cat_id = cat_id

        payload = {'action': 'process',
                   'fields': 'code,brands,product_name,nutrition_grade_fr,\
                              stores,quantity,ingredients_text,url',
                   'tagtype_0': 'categories',
                   'tag_contains_0': 'contains',
                   'tag_0': self.category,
                   'tagtype_1': 'countries',
                   'tag_contains_1': 'contains',
                   'tag_1': 'france',
                   'sort_by': 'unique_scans_n',
                   'page_size': 100,
                   'json': 1}

        address = 'https://fr.openfoodfacts.org/cgi/search.pl'
        r = requests.get(address, params=payload)
        data = r.json()
        # Extract porduct info from list
        products = data['products']

        for item in products:
            item['cat_id'] = self.cat_id
            self.all_products.append(item)

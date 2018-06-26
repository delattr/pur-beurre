#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


class Requests:

    def get_json(self, category):
        self.category = category

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
        return r.json()

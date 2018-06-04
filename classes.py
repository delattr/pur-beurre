#-*- coding: utf-8 -*-

import requests

class Requests:

    def get_json(self, category):
        self.category = category
    
        payload = {'action': 'process',
                   'tagtype_0': 'categories',
                   'tag_contains_0': 'contains',
                   'tag_0': self.category,
                   'tagtype_1': 'countries',
                   'tag_contains_1': 'contains',
                   'tag_1' :'france',
                   'sort_by' : 'unique_scans_n',
                   'page_size':100,
                   'json': 1}



        address = 'https://fr.openfoodfacts.org/cgi/search.pl'
        r = requests.get(address, params=payload)
        return r.json()

class JsonToList:
    _count = 0

    def __init__(self):
        self.data_extracted = []

    def extract_data(self, data):
        JsonToList._count += 1
        self.data = data


        columns = ['code', 'brands', 'product_name',
                   'nutrition_grade_fr','stores',
                   'quantity', 'url']


        #pprint.pprint(sorted(json['products'][0].keys()))

        for item in self.data['products']:

            dict_product = {k:item[k] for k in columns if k in item if item[k] !=''}

            dict_product['cat_id'] = JsonToList._count
            self.data_extracted.append(dict_product)

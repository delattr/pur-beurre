
#-*- coding: utf-8 -*-

import requests
import getpass
import json
import pprint
import pymysql.cursors

class Login:

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host='localhost',
                                     user=self.user,
                                     password=self.password,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def create_db(self):

        try:

            #Create database 'openfoodfacts'
            with self.connection.cursor() as cursor:

                cursor.execute('drop database openfoodfacts')

                sql = ('CREATE DATABASE IF NOT EXISTS Openfoodfacts')
                cursor.execute(sql)
                self.connection.commit()

            #Create talbe 'categories'
            with self.connection.cursor() as cursor:
                sql =('CREATE TABLE IF NOT EXISTS Openfoodfacts.categories ('
                        'id SMALLINT UNSIGNED AUTO_INCREMENT, '
                        'category VARCHAR(50), '
                        'PRIMARY KEY (id)'
                     ') ENGINE=InnoDB')
                cursor.execute(sql)
                self.connection.commit()

            #Create TABLE 'products'
            with self.connection.cursor() as cursor:
                sql =('CREATE TABLE IF NOT EXISTS Openfoodfacts.Products ('
                        'id SMALLINT UNSIGNED AUTO_INCREMENT, '
                        'code BIGINT UNSIGNED NOT NULL, '
                        'brands VARCHAR(100), '
                        'product_name VARCHAR(200), '
                        'nutrition_grade_fr varchar(1), '
                        'stores VARCHAR(90), '
                        'quantity VARCHAR(100), '
                        'url VARCHAR(500), '
                        'cat_id SMALLINT UNSIGNED, '
                        'PRIMARY KEY (id), '
                        'CONSTRAINT fk_cat_id FOREIGN KEY (cat_id) REFERENCES Openfoodfacts.categories(id)'
                     ') ENGINE=InnoDB')

                cursor.execute(sql)
                self.connection.commit()

        finally:
            pass

    def insert_categories(self, category, cat_id):
        self.category = category
        self.cat_id = cat_id

        try:

            with self.connection.cursor() as cursor:

                sql =('INSERT INTO Openfoodfacts.Categories (id, category) VALUES (%s, %s)')
                cursor.execute(sql, (self.cat_id, self.category))

        finally:
            pass



    def insert_products(self, data):

        self.data = data


        try:

            with self.connection.cursor() as cursor:

                for product in self.data:
                    placeholder = ','.join(['%s'] * len(product))
                    columns = ','.join(product.keys())

                    sql =('INSERT INTO Openfoodfacts.Products ({}) VALUES ({})'
                            .format(columns, placeholder))

                    cursor.execute(sql,(list(product.values())))
                    self.connection.commit()

        finally:
            pass

class Request:


    def __init__(self, category, cat_id):

        self.category = category
        self.cat_id = cat_id
        self.data = []


    def get_request(self):

        # url = 'https://fr.openfoodfacts.org/category/{}.json&lc=fr'
        # r = requests.get(url.format(self.category))
        #
        # #load json
        # json = r.json()

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
        json = r.json()

        columns = ['code', 'brands', 'product_name',
                   'nutrition_grade_fr','stores',
                   'quantity', 'url']

        data_category = []
        data_product = []
        #pprint.pprint(sorted(json['products'][0].keys()))


        for item in json['products']:

            mydict = {k:item[k] for k in columns if k in item if item[k] !=''}

            mydict['cat_id'] = self.cat_id
            data_category.append(mydict)
        self.data = data_category


#user = input('user: ')
# password = getpass.getpass()
categories =['pizza','pain']

database = Login('mayfly', 'password')
database.create_db()




for item in categories:
    cat_id = categories.index(item) + 1
    #Request class instance
    cat = Request(item, cat_id)
    cat.get_request()

    #execute class Login methodes
    database.insert_categories(item, cat_id)
    database.insert_products(cat.data)

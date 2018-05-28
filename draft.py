
#-*- coding: utf-8 -*-

import requests
import openfoodfacts
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

            cursor = self.connection.cursor()

            sql_db = ('CREATE DATABASE IF NOT EXISTS `Openfoodfacts`')


            cursor.execute(sql_db)


            self.connection.commit()


            sql_tb = ('CREATE TABLE IF NOT EXISTS Openfoodfacts.Products ('
                      'id smallint UNSIGNED PRIMARY KEY, '
                      'code INT(13) UNSIGNED UNIQUE, '
                      'brands VARCHAR(20), '
                      'product_name VARCHAR(40), '
                      'categories TEXT, '
                      'nutrition_grade_fr VARCHAR(1), '
                      'nutrition_score_fr SMALLINT, '
                      'stores VARCHAR(10), '
                      'quantity VARCHAR(10), '
                      'url TEXT) ENGINE=InnoDB')

            cursor.execute(sql_tb)
            self.connection.commit()


        finally:
            pass

    def insert(self, data):
        self.data = data

        columns = ['code','brands','product_name', 'categories',
                   'nutrition_grade_fr', 'store',
                   'quantity', 'url']

        try:

            cursor = self.connection.cursor()

            for column_name in columns:
                for item in self.data['products']:

                    sql = ('INSERT INTO Openfoodfacts.Products ({}) '.format(column_name) +
                           'VALUES ({})'.format(item[column_name]))


            cursor.execute(sql)
            self.connection.commit()

        finally:
            pass

class Request:

    def __init__(self, category):

        self.category = category
        self.data = []


    def get_request(self):

        url = 'https://fr.openfoodfacts.org/category/{}.json'
        r = requests.get(url.format(self.category))

        #load json
        self.data = r.json()





user = input('user: ')
password = input('password: ')

database = Login(user, password)

print('Initializing...')

database.create_db()

pizza = Request('pizza')
pizza.get_request()

database.insert(pizza.data)

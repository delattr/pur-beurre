#-*- coding: utf-8 -*-

import pymysql.cursors

class MysqlDB:

    def __init__(self, user, password):
        self.user = user
        self.password = password


    def connect(self):

        self.connection = pymysql.connect(host='localhost',
                                         user=self.user,
                                         password=self.password,
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

    def create_db(self):

        self.connect()

        try:

            #Create database 'openfoodfacts'
            with self.connection.cursor() as cursor:

                sql = ('CREATE DATABASE IF NOT EXISTS Openfoodfacts')
                cursor.execute(sql)
                self.connection.commit()

            #Create talbe 'categories'
            with self.connection.cursor() as cursor:
                sql =('CREATE TABLE IF NOT EXISTS Openfoodfacts.cat ('
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
                        'CONSTRAINT fk_cat_id FOREIGN KEY (cat_id) REFERENCES Openfoodfacts.cat(id)'
                     ') ENGINE=InnoDB')

                cursor.execute(sql)
                self.connection.commit()

        finally:
            self.connection.close()

    def insert_categories(self, categories):

        self.categories = categories

        self.connect()

        try:

            with self.connection.cursor() as cursor:

                for category_name in self.categories:

                    sql =('INSERT INTO Openfoodfacts.Cat (category) VALUES (%s)')

                    cursor.execute(sql, (category_name))
                    self.connection.commit()

        finally:
            self.connection.close()



    def insert_products(self, data):

        self.data = data

        self.connect()

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
            self.connection.close()

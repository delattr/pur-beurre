#-*- coding: utf-8 -*-

import getpass
from classes import *
from mysqlclass import *

print('MySql Server Log-in:')

user = input('user: ')
password = getpass.getpass()
mysql = MysqlDB(user, password)

categories =['pizza', 'pain']

r = Requests()
products = JsonToList()




for category in categories:

    # Convert json to an object
    product_data = r.get_json(category)
    # Extract data needed from the object
    products.extract_data(product_data)

all_products = products.data_extracted

mysql.create_db()
mysql.insert_categories(categories)
mysql.insert_products(all_products)

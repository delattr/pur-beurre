#-*- coding: utf-8 -*-

import getpass
import pprint
from classes import *
from mysqlclass import *
from menu import *

print('\nMySql Server Log-in:')



USER = input('user: ')
PASSWORD = getpass.getpass()

mysql = MysqlDB(USER, PASSWORD)

# Check if database exits if not, load json form 'openfoodfacts.org'
if mysql.check_db() == None:
    print('\ndownloading data....')
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
    # Insert list into DB table categories
    mysql.insert_categories(categories)
    #insert dict into DB table products
    mysql.insert_products(all_products)

categ_fetched = mysql.fetch_categoies()

navigate = Menu()
navigate.welcome()

menu = 'welcome'
if  menu == 'welcome':

    if navigate.answer_welcome == 1:
        navigate.categories(categ_fetched)
        menu = 'foods'
    elif navigate.answer_welcome == 2:
        navigate.foods_saved()
    elif anavigate.answer_welcome == 'exit':
        sys.exit('Goodbye')

if menu == 'foods':
    product_list = mysql.fetch_products(navigate.cat_id)
    navigate.foods(product_list)

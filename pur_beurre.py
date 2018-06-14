#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass
from api_requests import *
from mysqlclass import *
from convert import *
from menu import *
import sys

user_answer = None
menu = 'home'

print('\nMySql Server Log-in:')
user = input('user: ')
password = getpass.getpass()

mysql = MysqlDB(user, password)
navigate = Menu()

# Check if database exists, if not, get json form 'openfoodfacts.org'
if mysql.check_db() == None:
    print('\ndownloading data....')

    categories = sorted(['chocolate', 'pizza', 'pain', 'pâte à tartiner',
                         'yaourts', 'Biscuits et gâteaux'])

    r = Requests()
    convert = JsonToList()

    for category in categories:

        # Convert json to an object
        product_data = r.get_json(category)
        # Extract data needed from the object
        convert.extract_data(product_data)

    all_products = convert.data_extracted

    mysql.create_db()
    # Insert list into DB table categories
    mysql.insert_categories(categories)
    # insert dict into DB table products
    mysql.insert_products(all_products)
# asks user for an input


def user_input():

    answer = input('Entrez votre choix >>>')
    answer = answer.lower()
    try:
        answer = int(answer)

    except ValueError:
        pass

    if answer == 'exit':
        sys.exit('Goodbye')

    return answer


while True:
    # Home screen
    if menu == 'home':
        product_id = None
        cat_id = None
        navigate.home()
        print('\n')

        while True:
            user_answer = user_input()

            if type(user_answer) == int:
                if user_answer == 1:
                    menu = 'categories'
                    break
                elif user_answer == 2:
                    menu = 'myfoods'
                    break
                elif user_input == 'home':
                    break
    # Catetory screen
    if menu == 'categories':
        cat_fetched = mysql.fetch_categoies()
        navigate.categories(cat_fetched)
        print('\n')

        while True:
            user_answer = user_input()

            if type(user_answer) == int:
                if user_answer > 0:
                    if user_answer <= len(cat_fetched):
                        menu = 'product_list'
                        cat_id = user_answer
                        break
            elif user_answer == 'home':
                menu = 'home'
                break
    # My food list screen
    if menu == 'myfoods':
        saved_foods = mysql.fetch_saved_foods()
        navigate.my_foods(saved_foods)
        print('\n')

        while True:
            user_answer = user_input()

            if type(user_answer) == int:
                if user_answer > 0:
                    if user_answer <= len(saved_foods):
                        for i in saved_foods:
                            if user_answer == i['id']:
                                product_id = i['product_id']
                                cat_id = i['cat_id']
                                menu = 'product_info'
                        break
            elif user_answer == 'home':
                menu = 'home'
                break
    # Product list screen
    if menu == 'product_list':
        products = mysql.fetch_products(cat_id)
        navigate.product_list(products)
        print('\n')

        while True:
            user_answer = user_input()

            if type(user_answer) == int:
                if user_answer > 0:
                    if user_answer <= len(products):
                        for i in products:
                            if user_answer == i['num']:
                                product_id = i['id']
                                menu = 'product_info'
                        break
            elif user_answer == 'home':
                menu = 'home'
                break
    # Display product info and subsitutes
    if menu == 'product_info':
        info = mysql.fetch_product_info(product_id)
        subs = mysql.fetch_susbstituts(product_id, cat_id)
        navigate.food_info(info, subs)

        print('\nPour enregistrer ce produit, tapez "0"')

        while True:
            user_answer = user_input()

            if type(user_answer) == int:
                if user_answer == 0:
                    save = navigate.save()
                    if save == True:
                        message = mysql.save_product(product_id)
                        print(message)
                elif user_answer > 0:
                    if user_answer <= len(subs):
                        for i in subs:
                            if user_answer == i['num']:
                                product_id = i['id']
                                cat_id = i['cat_id']
                        break
            elif user_answer == 'home':
                menu = 'home'
                break

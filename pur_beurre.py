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
    while True:
        print("Les bases de donées n'existent pas.")
        database = input('Voulez-vous installer les bases de données (y/n) ? >')
        database = database.lower()
        if database == 'y':

            categories = sorted(['chocolate', 'pizza', 'pain', 'pâte à tartiner',
                                 'yaourts', 'Biscuits et gâteaux'])

            r = Requests()
            convert = Extract()

            for category in categories:

                # Convert json to an object
                r.get_json(category, (categories.index(category) + 1))

                all_products = r.all_products

            # Create database and tables
            mysql.create_db()
            # Insert list into DB table categories
            mysql.insert_categories(categories)
            # insert dict into DB table products
            mysql.insert_products(all_products)
            break
        elif database == 'n':
            sys.exit('Goodbye')

# asks user for an input


def user_input():

    answer = input('>>>')
    answer = answer.lower()
    try:
        answer = int(answer)

    except ValueError:
        pass

    if answer == 'exit':
        sys.exit('Goodbye')

    return answer


def cls():

    os.system('cls' if os.name == 'nt' else 'clear')


def instruction():
    print("\nTapez 'exit' pour sortir ou 'home' pour revenir à l'accueil.")


while True:
    # Home screen
    if menu == 'home':
        cls()
        product_id = None
        sub_id = None
        cat_id = None

        navigate.home()
        instruction()
        while True:
            print("\nEntrez un numéro du menu.")
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
        cls()
        cat_fetched = mysql.fetch_categoies()
        navigate.categories(cat_fetched)
        instruction()
        while True:
            print("\nEntrez un muméro d'une categorie")
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
        cls()
        saved_foods = mysql.fetch_saved_foods()
        navigate.my_foods(saved_foods)
        instruction()
        while True:
            print('\nEntrez un numéro de produit.')
            user_answer = user_input()

            if type(user_answer) == int:
                if user_answer > 0:
                    if user_answer <= len(saved_foods):
                        for i in saved_foods:
                            if user_answer == i['id']:
                                product_id = i['product_id']
                                sub_id = i['sub_id']
                                menu = 'new_product_info'
                        break
            elif user_answer == 'home':
                menu = 'home'
                break
    # Product list screen
    if menu == 'product_list':
        cls()
        products = mysql.fetch_products(cat_id)
        navigate.product_list(products)
        instruction()
        while True:
            print('\nEntrez numéro de produit.')
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
        cls()
        info = mysql.fetch_product_info(product_id)
        subs = mysql.fetch_susbstituts(product_id, cat_id)
        navigate.food_info(info)
        navigate.subs(subs)
        instruction()
        while True:
            print('\nEntrez un numéro de substitut.')
            user_answer = user_input()

            if type(user_answer) == int:
                if user_answer > 0:
                    if user_answer <= len(subs):
                        for i in subs:
                            if user_answer == i['num']:
                                sub_id = i['id']
                                menu = 'subsitute'
                        break
            elif user_answer == 'home':
                menu = 'home'
                break

    if menu == 'subsitute':
        cls()
        sub_info = mysql.fetch_product_info(sub_id)
        print('Produit choisi :\n')
        navigate.food_info(info)
        print("\n----------------------------------------------------------\n")
        print('Substitut :\n')
        navigate.food_info(sub_info)
        instruction()
        while True:
            print('\nTapez "0" pour enregistrer le produit '
                  'ou "back" pour revenir en arrière')
            user_answer = user_input()

            if type(user_answer) == int:
                if user_answer == 0:
                    if navigate.save():
                        message = mysql.save_product(sub_id, product_id)
                        print(message)
            elif user_answer == 'back':
                menu = 'product_info'
                break
            elif user_answer == 'home':
                menu = 'home'
                break

    # Display the replaced product and the original product
    if menu == 'new_product_info':
        cls()
        print('Puoduit substitué :\n')
        info = mysql.fetch_product_info(sub_id)
        old_info = mysql.fetch_product_info(product_id)
        navigate.food_info(info)
        print("\n------------------------------------------------------\n")
        print('Produit remplacé :\n')
        navigate.food_info(old_info)
        instruction()
        while True:
            print('\nTapez "back" pour revenir en arrière')
            user_answer = user_input()

            if user_answer == 'back':
                menu = 'myfoods'
                break
            elif user_answer == 'home':
                menu = 'home'
                break

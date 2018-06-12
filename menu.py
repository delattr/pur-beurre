#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import textwrap

wrapper = textwrap.TextWrapper(width = 70, initial_indent = '\t', subsequent_indent = '\t' )



class Menu():

    def __init__(self):
        self.menu = 'home'

    def cls(self):

        os.system('cls' if os.name=='nt' else 'clear')

    def home(self):
        self.cls()
        file = open('main', 'r', encoding='utf8')
        print(file.read())
        file.close()


    def categories(self, cat_fetched):
        self.cls()
        self.cat_fetched = cat_fetched

        print('Chosissez une catégorie :\n')

        for item in self.cat_fetched:
            menu = '. '.join(map(str, item.values()))
            print(menu)


    def my_foods(self, saved_foods):

        self.saved_foods = saved_foods

        self.cls()

        print('my food list:\n')
        for i in self.saved_foods:
            menu = '{}. {} - {}'.format(i['id'], i['brands'], i['product_name'])
            print(menu)


    def product_list(self, products):
        self.cls()
        self.products = products
        print('chosissez un product:\n')

        for item in self.products:
            menu = '{}. {} - {}'.format(item['num'], item['brands'], item['product_name'])
            print(menu)


    def food_info(self, product_info, subs_fetched):
        self.cls()
        self.menu = 'foodinfo'
        self.product_info = product_info
        self.subs_fetched = subs_fetched
        product = self.product_info[0]

        print(product['product_name'],'\n')
        print('Déscription :\n')
        print('Marques :', product['brands'])
        print('Quantités :', product ['quantity'])
        print('Magasins :', product ['stores'],'\n')
        print('Nutrition Score :', product ['nutrition_grade_fr'],'\n')
        print('Ingrédients :\n', wrapper.fill(product ['ingredients_text']),'\n')
        print('URL :', product ['url'])


        print('\n------------------------------------------------------------')

        print('\nSubstituts :\n')


        for item in self.subs_fetched:
            menu = '{}. {} - {}'.format(item['num'], item['brands'], item['product_name'])
            print('{:<45} Score : {}'.format(menu,item['nutrition_grade_fr']))

    def save(self):

            while True:
                user_answer = input("Voulez-vous enregistrer ce produit ('y/n') ? ")
                user_answer = user_answer.lower()
                if user_answer == 'y':
                    return True
                    break
                elif user_answer == 'n':
                    print('Enregistration annulé')
                    return False
                    break

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import textwrap

wrapper = textwrap.TextWrapper(width=70, initial_indent='\t',
                               subsequent_indent='\t')

sub = textwrap.TextWrapper(width=50, subsequent_indent='    ')


class Menu():
    """
    Diplays interface of the application"""

    def __init__(self):
        self.menu = 'home'

    def home(self):

        file = open('main', 'r', encoding='utf8')
        print(file.read())
        file.close()

    def categories(self, cat_fetched):

        self.cat_fetched = cat_fetched

        print('Les catégories :\n')

        for item in self.cat_fetched:
            menu = '. '.join(map(str, item.values()))
            print(menu)

    def my_foods(self, saved_foods):

        self.saved_foods = saved_foods

        print('my food list:\n')
        for i in self.saved_foods:
            menu = '{}. {} - {}'.format(i['id'], i['brands'],
                                        i['product_name'])
            print(menu)

    def product_list(self, products):

        self.products = products
        print('chosissez un product:\n')

        for item in self.products:
            menu = '{}. {} - {}'.format(item['num'], item['brands'],
                                        item['product_name'])
            print(menu)

    def food_info(self, product_info):

        self.menu = 'foodinfo'
        self.product_info = product_info

        product = self.product_info[0]

        print(product['product_name'], '\n')
        print('Déscription :\n')
        print('Marques :', product['brands'])
        print('Quantités :', product['quantity'])
        print('Magasins :', product['stores'], '\n')
        print('Nutrition Score :', product['nutrition_grade_fr'], '\n')
        print('Ingrédients :\n', wrapper.fill(product['ingredients_text']), '\n')
        print('URL :', product['url'])

    def subs(self, subs_fetched):
        self.subs_fetched = subs_fetched
        print('\n------------------------------------------------------------')

        print('\nSubstituts :\n')
        line_length = 50
        for item in self.subs_fetched:
            menu = '{} - {}'.format(item['brands'], item['product_name'])
            menu = sub.fill(menu)
            curr_length = len(menu)
            lastline = sub.wrap(menu)
            space = 0
            if len(lastline) > 1:
                if len(lastline[-1]) < line_length:
                    space = line_length - len(lastline[-1]) + 4
            print('{:>2}. {:<50}{} Score : {}'.format(
                item['num'], menu, " "*space, item['nutrition_grade_fr']))

    def save(self):

        while True:
            user_answer = input("Voulez-vous enregistrer le substitut "
                                "('y/n') ?")
            user_answer = user_answer.lower()
            if user_answer == 'y':
                return True
                break
            elif user_answer == 'n':
                print('Enregistration annulé')
                return False
                break

#-*- coding: utf-8 -*-
from mysqlclass import *


class Menu():

    def __init__(self):
        pass

    def welcome(self):

        file = open('main', 'r', encoding='utf8')
        print(file.read())
        file.close()

        while True:
            print('\n')
            answer =  input('Tapper un unméro>>>')
            answer = int(answer)
            if answer == 1 or answer == 2 or answer == 3:
                break

        self.answer_welcome = answer


    def categories(self, data):


        self.data = data
        print('\n\n\nmenu category: \n\n')

        for item in self.data:

            menu = '. '.join(map(str, item.values()))
            print(menu)

        while True:

            print('\n')
            answer =  input('Tapper un unméro>>>')
            answer = int(answer)
            if answer > 0 and answer <= len(self.data) + 1:
                break

        self.cat_id = answer





    def my_foods(self):

        print('my food list:')


    def foods(self, product_list):
        self.product_list = product_list

        print('\n\n\nchosissez un product:\n\n')


        for item in self.product_list:

            menu = '. '.join(map(str, item.values()))
            print(menu)

        while True:
            print('\n')
            answer =  input('Tapper un unméro>>>')
            answer = int(answer)
            if answer > 0 and answer <= len(self.data) + 1:
                break

        self.id = answer

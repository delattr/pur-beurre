# Pur Beurre

**Pur Beure** helps users to make healthier food choices by
recommending foods with higher nutrition score.

This is a project number 05 of Python developer course from
[OPENCLASSROOMS](https://openclassrooms.com/)

## Geting started

### Prerequisites
- python 3.6.5
- PyMysql 0.8.1
- Requests 2.11.1
- MySQL 5.7

### Installing
Running under a virtual environment is recommended.

1. Connect to MySQL and grant privileges.
   Do not create database yourself. Pur beurre will create one for you.
```Mysql
GRANT ALL ON openfoodfacts.* TO 'user'@'localhost';
```
2. Install requirements.txt using pip install.
```
pip install -r requirements.txt
```
3. Run pur_beurre.py

## API Reference
[API openfoodfacts](https://en.wiki.openfoodfacts.org/API)

## Supported Language
French

## Version
v 0.1.1
- displays the substitut food and the replaced food at the same time when looking up the foods saved.

v 0.1.0

class JsonToList:
    _count = 0

    def __init__(self):
        self.data_extracted = []

    def extract_data(self, data):
        JsonToList._count += 1
        self.data = data

        for item in self.data['products']:

            dict_product = {k:item[k] for k in item}

            dict_product['cat_id'] = JsonToList._count
            self.data_extracted.append(dict_product)

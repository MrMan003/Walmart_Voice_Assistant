store_grid = [
    ['entrance', '_', 'A1', '_', 'A2', '_', 'A3', '_', '_', '_'],
    ['_',       '_', '_',  '_', '_',  '_', '_',  '_', '_', '_'],
    ['_',       '_', 'B1', '_', 'B2', '_', 'B3', '_', '_', '_'],
    ['_',       '_', '_',  '_', '_',  '_', '_',  '_', '_', '_'],
    ['_',       '_', 'C1', '_', 'C2', '_', 'C3', '_', '_', '_'],
    ['_',       '_', '_',  '_', '_',  '_', '_',  '_', '_', '_'],
    ['_',       '_', 'D1', '_', 'D2', '_', 'D3', '_', '_', '_'],
    ['_',       '_', '_',  '_', '_',  '_', '_',  '_', '_', '_'],
]

shelf_and_products = {
    'A1': ['milk', 'eggs'], 'A2': ['yogurt', 'greek yogurt'], 'A3': ['cheese', 'butter'],
    'B1': ['shampoo', 'conditioner'], 'B2': ['soap', 'body wash'], 'B3': ['face wash', 'lotion'],
    'C1': ['bread', 'bagels'], 'C2': ['snacks', 'cookies'], 'C3': ['chips', 'canned vegetables'],
    'D1': ['toothpaste', 'toothbrush'], 'D2': ['mouthwash', 'floss'], 'D3': ['detergent', 'dish soap'],
}

shelf_position = {}
product_position = {}
entrance_position = None

for i, row in enumerate(store_grid):
    for j, cell in enumerate(row):
        if cell == 'entrance':
            entrance_position = (i, j)
        elif cell != '_':
            shelf_position[cell] = (i, j)

for shelf, products in shelf_and_products.items():
    if shelf in shelf_position:
        for product in products:
            product_position[product] = shelf_position[shelf]

def find_product_location(product):
    return product_position.get(product)

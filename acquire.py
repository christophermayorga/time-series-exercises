import pandas as pd
import requests
import os

def new_items():
    # Creating a dataframe that has all of the data for items

    # For loop

    # Empty list
    items_list = []

    # Get our response using the base url
    response = requests.get('https://python.zach.lol/api/v1/items')

    # Save the data into a variable - data is a dictionary
    data = response.json()

    # Last page
    n = data['payload']['max_page']

    # Do this process for each page and add the data to the items_list
    for i in range(1,n+1):
        url = 'https://python.zach.lol/api/v1/items?page='+str(i)
        response = requests.get(url)
        data = response.json()
        page_items = data['payload']['items']
        items_list += page_items
        
    return pd.DataFrame(items_list)

def get_items():
    if os.path.isfile('items.csv'):
        df = pd.read_csv('items.csv', index_col=0)
    else:
        df = new_items()
        df.to_csv('items.csv')
        
    return df
    
def new_stores():
    # Creating a dataframe that has all of the data for stores

    # For loop

    # Empty list
    stores_list = []

    # base url for store
    url = 'https://python.zach.lol/api/v1/stores'

    # Get our response using the base url
    response = requests.get('https://python.zach.lol/api/v1/stores')

    # Save the data into a variable - data is a dictionary
    data = response.json()

    # Last page
    n = data['payload']['max_page']

    # Do this process for each page and add the data to the items_list
    for i in range(1,n+1):
        store_url = url + '?page='+str(i)
        response = requests.get(store_url)
        data = response.json()
        page_stores = data['payload']['stores']
        stores_list += page_stores
    
    return pd.DataFrame(stores_list)
    
def get_stores():
    if os.path.isfile('stores.csv'):
        df = pd.read_csv('stores.csv', index_col=0)
    else:
        df = new_stores()
        df.to_csv('stores.csv')
        
    return df

def get_sales():
    if os.path.isfile('sales.csv'):
        df = pd.read_csv('sales.csv', index_col=0)
        return df
    else:
        sales_list = []
        url = 'https://python.zach.lol/api/v1/sales'
        response = requests.get(url)
        data = response.json()
        n = data['payload']['max_page']
        for i in range(1,n+1):
            sales_url = url + '?page=' +str(i)
            response = requests.get(sales_url)
            data = response.json()
            page_sales = data['payload']['sales']
            sales_list += page_sales
            df = pd.DataFrame(sales_list)
            df.to_csv('sales.csv')
        return df
    
def get_all_sales_data():
    if os.path.isfile('combined.csv'):
        df = pd.read_csv('combined.csv', index_col=0)
        return df
    else:
        items = get_items()
        stores = get_stores()
        sales = get_sales()
        sales['store_id'] = sales['store']
        sales = sales.drop(columns='store')
        sales_plus_stores = pd.merge(sales, stores, on='store_id', how='inner')
        sales_plus_stores['item_id'] = sales_plus_stores['item']
        sales_plus_stores = sales_plus_stores.drop(columns='item')
        df = pd.merge(sales_plus_stores, items, on='item_id', how='inner')
        return df
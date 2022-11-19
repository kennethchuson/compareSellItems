from flask import Flask, render_template, url_for, request, redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from lxml import html
import time 
import openpyxl
import numpy as np


app = Flask(__name__)

path = "/Users/kennethchuson/Desktop/compareSellItems/selenium_driver/chromedriver"

driver = webdriver.Chrome(path)
driver2 = webdriver.Chrome(path) 


workbook = openpyxl.load_workbook("storage/storage_one.xlsx")
sheet = workbook.active 


@app.route('/', methods=['POST', 'GET'])
def home():
    product_img = [] 
    product_title = [] 
    product_cost = []
    if request.method == 'POST':
        result_enter = request.form['content'] 

        driver.get("https://www.amazon.com")
        driver2.get("https://www.ebay.com")



        search = driver.find_element_by_id("twotabsearchtextbox")
        search2 = driver2.find_element_by_name("_nkw")

        search.send_keys(str(result_enter)) 
        search2.send_keys(str(result_enter)) 

        search.send_keys(Keys.RETURN) 
        search2.send_keys(Keys.RETURN) 

        #webscrape
     
        for products in html.fromstring(driver.page_source).xpath('//div[contains(@data-cel-widget, "search_result_")]'): 
            product_title.append(products.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text()')) 
            product_cost.append(products.xpath('.//span[@class="a-price-whole"]/text()'))

        for products_img in driver.find_elements(By.XPATH, '//img[contains(@class, "s-image")]'): 
            product_img.append(products_img.get_attribute('src'))

 
        
        print("images: ", product_img) 
        print("title: ", product_title) 
        print("cost: ", product_cost)




        time.sleep(1)
    
    amazon_info = {
        'name': "Amazon",
        'image': product_img, 
        'title': list(np.array(list(product_title)).flatten()), 
        'cost': list(np.array(list(product_cost)).flatten()) 
    }
    


    print("amazon_info: ", amazon_info)

    #store into excel 
    sheet['B1'] = amazon_info['name'] 
    sheet['B2'] = "Image"
    sheet['C2'] = "Title"
    sheet['D2'] = "Cost"
    
    '''
    for amazon_product in range(3, len(amazon_info['image']) + 3): 
        sheet[f'B{amazon_product}'] = amazon_info['image']
        sheet[f'C{amazon_product}'] = amazon_info['title']
        sheet[f'D{amazon_product}'] = amazon_info['cost']
    '''


    #return render_template('index.html', amazon_info_img=amazon_info['image'], amazon_info_title=amazon_info['title'], amazon_info_cost=amazon_info['cost'])
    return render_template('index.html', context_amazon_info={"data":zip(amazon_info['image'], amazon_info['title'], amazon_info['cost'])})



if __name__ == '__main__':
   app.run()
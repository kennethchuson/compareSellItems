from flask import Flask, render_template, url_for, request, redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from lxml import html
import time 
import openpyxl
import os



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

    product2_img = [] 
    product2_title = [] 
    product2_cost = [] 

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

        #webscrape amazon
        a_test_title = [] 
        b_test_cost = [] 
        for products in html.fromstring(driver.page_source).xpath('//div[contains(@data-cel-widget, "search_result_")]'): 
            a_test_title.append(products.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text()')) 
            b_test_cost.append(products.xpath('.//span[@class="a-price-whole"]/text()'))
        
        aTT = [j for sub in a_test_title for j in sub]
        aTC = [j for sub in b_test_cost for j in sub]

        for elem in aTT: 
            product_title.append(elem) 
        
        for elem in aTC:
            product_cost.append(elem)  
    


        for products_img in driver.find_elements(By.XPATH, '//img[contains(@class, "s-image")]'): 
            product_img.append(products_img.get_attribute('src'))  





        #webscrape ebay 

        '''
        size_driver2_elements = driver2.find_elements(By.XPATH, '//img[contains(@class, "s-item__image-img")]') 

        for i in range(len(size_driver2_elements)):
            a = os.path.splitext(size_driver2_elements[i].get_attribute('src'))[0] + '.png' 
            product2_img.append(a)
        '''
        

        a2_test_title = [] 
        b2_test_cost = []

        for products in html.fromstring(driver2.page_source).xpath('//div[contains(@class, "srp-river srp-layout-inner")]'): 
            a2_test_title.append(products.xpath('//div[@class="s-item__title"]/span[@role="heading"]/text()')) 
            b2_test_cost.append(products.xpath('.//span[@class="s-item__price"]/text()'))

        aTT2 = [j for sub in a2_test_title for j in sub]
        aTC2 = [j for sub in b2_test_cost for j in sub]

        for elem in aTT2: 
            product2_title.append(elem) 
        
        for elem in aTC2:
            product2_cost.append(elem)
        

 
        
        print("images: ", product_img) 
        print("title: ", product_title) 
        print("cost: ", product_cost)




        time.sleep(1)
    
    amazon_info = {
        'name': "Amazon",
        'image': product_img, 
        'title': product_title, 
        'cost': product_cost
    }

    
    ebay_info = {
        'name': "Ebay", 
        'image': product2_img, 
        'title': product2_title[1:], 
        'cost': product2_cost[1:]
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

    return render_template('index.html', context_amazon_info={"data":zip(amazon_info['image'], amazon_info['title'], amazon_info['cost'])}, context_ebay_info={"data": zip(ebay_info['title'], ebay_info['cost'])})



if __name__ == '__main__':
   app.run()

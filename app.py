from flask import Flask, render_template, url_for, request, redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from lxml import html
import spacy
import itertools
from itertools import permutations
import re
import time 
import openpyxl
import xlsxwriter
import os



app = Flask(__name__)

path = "/Users/kennethchuson/Desktop/compareSellItems/selenium_driver/chromedriver"

driver = webdriver.Chrome(path)
driver2 = webdriver.Chrome(path) 

nlp = spacy.load("en_core_web_lg")

regex_ignore_special_chars = re.compile('[,\.!?|()+$"/]')

#workbook = openpyxl.load_workbook("storage/storage_one.xlsx")
workbook_write = xlsxwriter.Workbook("storage/storage_one.xlsx")

#sheet = workbook.active 
sheet_write = workbook_write.add_worksheet()


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



        search = driver.find_element("id", "twotabsearchtextbox")
        search2 = driver2.find_element("name", "_nkw")

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
        






        time.sleep(1)



    amazon_info = {
        'name': "Amazon",
        'image': product_img, 
        'title': product_title[:5], 
        'cost': product_cost
    }

    
    ebay_info = {
        'name': "Ebay", 
        'image': product2_img, 
        'title': product2_title[1:6], 
        'cost': product2_cost[1:]
    } 


    

    #store into excel 


    sheet_write.write('B1', amazon_info['name'])
    sheet_write.write('B2', "Image")
    sheet_write.write('C2', "Title")
    sheet_write.write('D2', "Cost")


    sheet_write.write('F1', ebay_info['name'])
    sheet_write.write('F2', "Image")
    sheet_write.write('G2', "Title")
    sheet_write.write('H2', "Cost")


    

    for amazon_product_img in range(len(amazon_info['image'])): 
        path = 'B' + str(amazon_product_img + 3)
        sheet_write.write(path, str(amazon_info['image'][amazon_product_img])) 


    for amazon_product_title in range(len(amazon_info['title'])):
        path = 'C' + str(amazon_product_title + 3)
        sheet_write.write(path, str(amazon_info['title'][amazon_product_title])) 
    
    for amazon_product_cost in range(len(amazon_info['cost'])):
        path = 'D' + str(amazon_product_cost + 3)
        sheet_write.write(path, str(amazon_info['cost'][amazon_product_cost])) 
    


    for ebay_product_img in range(len(ebay_info['image'])): 
        path = 'F' + str(ebay_product_img + 3)
        sheet_write.write(path, str(ebay_info['image'][ebay_product_img])) 

    for ebay_product_title in range(len(ebay_info['title'])): 
        path = 'G' + str(ebay_product_title + 3)
        sheet_write.write('G' + str(ebay_product_title + 3), str(ebay_info['title'][ebay_product_title])) 
    

    for ebay_product_cost in range(len(ebay_info['cost'])): 
        path = 'H' + str(ebay_product_cost + 3)
        sheet_write.write(path, str(ebay_info['cost'][ebay_product_cost])) 
    
    


    workbook_write.close() 

    total_sum_amazon_cost = str(sum([int(str(i).replace(',','').replace('$','').replace('.','')) for i in amazon_info['cost']]))
    total_sum_ebay_cost = str(sum([int(str(i).replace(',','').replace('$','').replace('.','')) for i in ebay_info['cost']]))


    #Product title similarities 
    
    amazon_title_parse_list = [ regex_ignore_special_chars.sub('', sentence) for sentence in amazon_info['title'] ] 
    ebay_title_parse_list = [ regex_ignore_special_chars.sub('', sentence) for sentence in ebay_info['title'] ]


    permute = itertools.permutations(amazon_title_parse_list, len(ebay_title_parse_list))

    store_similars = [] 
    top_similars_titles = [] 
    result_amazon_list = [] 
    result_ebay_list = [] 

    seen_product = set() 
    new_store_similars = [] 


    for elem in permute: 
        a = list(zip(elem, ebay_title_parse_list))
        for elem2 in a: 
            s1 = nlp(elem2[0]) 
            s2 = nlp(elem2[1]) 
            calc_similar = s1.similarity(s2) 
            store_similars.append([calc_similar, s1, s2]) 
    
    new_list_copy = [set(v) for v in store_similars]
    for elem in new_list_copy: 
        s2 = list(elem)
        b = [str(s2[1]), str(s2[2])]
        t = tuple(b)
        if t not in seen_product:
            new_store_similars.append(s2)
            seen_product.add(t)
    
    
    
    new_store_similars.sort(key=lambda x: x[0])

    print(new_store_similars)

    if len(new_store_similars) > 0: 
        for i in range(len(new_store_similars) - 3, len(new_store_similars)): 
            a = [new_store_similars[i][0], new_store_similars[i][1], new_store_similars[i][2]]
            top_similars_titles.append(a) 
        
        for i in range(len(top_similars_titles)): 
            start = 0 
            end = len(top_similars_titles) - 1

            temp = top_similars_titles[start]
            top_similars_titles[start] = top_similars_titles[end]
            top_similars_titles[end] = temp
        
        for i in range(len(top_similars_titles)): 
            result_amazon_list.append(top_similars_titles[i][1])
        
        for i in range(len(top_similars_titles)): 
            result_ebay_list.append(top_similars_titles[i][2])
    
    
    print("lIST 1: ", result_amazon_list) 
    print("lIST 2: ", result_ebay_list) 



    return render_template('index.html', context_amazon_info={"data":zip(amazon_info['title'], amazon_info['cost'])}, context_ebay_info={"data": zip(ebay_info['title'], ebay_info['cost'])}, total_amazon_cost=total_sum_amazon_cost, total_ebay_cost=total_sum_ebay_cost, context_similar_products={"data": zip(result_amazon_list, result_ebay_list)})

    



if __name__ == '__main__':
   app.run()

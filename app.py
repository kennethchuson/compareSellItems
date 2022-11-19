from flask import Flask, render_template, url_for, request, redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time 
import openpyxl

app = Flask(__name__)

path = "/Users/kennethchuson/Desktop/compareSellItems/selenium_driver/chromedriver"

driver = webdriver.Chrome(path)
driver2 = webdriver.Chrome(path) 


workbook = openpyxl.load_workbook("storage/storage_one.xlsx")


@app.route('/', methods=['POST', 'GET'])
def home():
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

        #store data into excel 




        time.sleep(1)
        

    return render_template('index.html')


if __name__ == '__main__':
   app.run()
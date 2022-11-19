from flask import Flask, render_template, url_for, request, redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time 
import openpyxl

app = Flask(__name__)

path = "/Users/kennethchuson/Desktop/compareSellItems/selenium_driver/chromedriver"

driver = webdriver.Chrome(path)

e_commerce_sites = ["https://www.ebay.com", "https://www.walmart.com", "https://www.amazon.com"]

workbook = openpyxl.load_workbook("storage/storage_one.xlsx")


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        result_enter = request.form['content'] 

        driver.get("https://www.amazon.com")
        get_title = driver.title

        search = driver.find_element_by_id("twotabsearchtextbox")
        search.send_keys(str(result_enter)) 
        search.send_keys(Keys.RETURN) 

        info_search = driver.page_source

        

        time.sleep(1)
        

    return render_template('index.html')


if __name__ == '__main__':
   app.run()
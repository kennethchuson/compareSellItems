from selenium import webdriver

path = "/Users/kennethchuson/Desktop/compareSellItems/selenium_driver/chromedriver"

driver = webdriver.Chrome(path)

e_commerce_sites = ["https://www.ebay.com", "https://www.walmart.com", "https://www.amazon.com"]

driver.get("https://www.ebay.com")


driver.quit() 

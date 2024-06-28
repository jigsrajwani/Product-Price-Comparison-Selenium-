from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import uvicorn

app = FastAPI()

# Initialize WebDriver
driver = webdriver.Chrome()

# Jinja2Templates instance to load HTML templates
templates = Jinja2Templates(directory="templates")

def get_amazon_price(url):
    driver.get(url)
    time.sleep(4)
    price = driver.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
    return price

def get_flipkart_price(url):
    driver.get(url)
    time.sleep(4)
    price = driver.find_element(By.CLASS_NAME, 'Nx9bqj.CxhGGd').text
    return price

# URLs of the product pages
amazon_url = 'https://www.amazon.in/Nike-Mens-Revolution-Black-Running/dp/B0C8TH2TXS/ref=sr_1_2?crid=XEQ13PJ60D6Y&dib=eyJ2IjoiMSJ9.D8DOx6HMRBqHtqq3tHK25NBQcukV2SnTed3h_W3UlV3Fu4Q-kKERXrdxh1sRZhO8NTHiJbB-rqnJSTSBqhKSIRbWMTNv3tYAucB8y7KfuPEKqkuPTMuSwITQe6nPPYAX4BwiZHXX5XWMBUXy3IV5mw0ebtroBmwYyf69BJcKUCEmz-TZI2A8-993qAOogtJOEKDf9J9VgtBJpJBn7trLSno73_MOFm5U5u2vMEfddMp72D2I5cHmfgcIJ-EnwlzQJhro6J-CHxWI6eqd8MNveWurwsu8Ebq9C8vefgcEiqo.TV15rQr95pjQ91PAtUdxO6G_bcaVXRWI37tk53bOUo8&dib_tag=se&keywords=nike+shoes&qid=1719483315&sprefix=nike+sho%2Caps%2C358&sr=8-2'
flipkart_url = 'https://www.flipkart.com/nike-revolution-7-running-shoes-men/p/itm6650567f18765?pid=SHOGTTHJZZYSJ7PD&lid=LSTSHOGTTHJZZYSJ7PDTGXEAA&marketplace=FLIPKART&q=Nike+Mens+Revolution+7Running+Shoe&store=osp%2Fcil%2F1cu&srno=s_1_14&otracker=search&otracker1=search&fm=Search&iid=72faf5e7-d2c8-429a-a8ac-0609838fb728.SHOGTTHJZZYSJ7PD.SEARCH&ppt=sp&ppn=sp&ssid=bqhk5bxark0000001719484446290&qH=583cdda02123c603'

amazon_price = get_amazon_price(amazon_url)
flipkart_price = get_flipkart_price(flipkart_url)
flipkart_price = flipkart_price.split('₹')[1]

prices = {
        'Amazon': amazon_price,
        'Flipkart': flipkart_price
    }

lowest_price_store = min(prices, key=prices.get)
lowest_price = prices[lowest_price_store]

driver.quit()

@app.get("/")
async def read_root(request: Request):

    # Render the HTML template with the data
    return templates.TemplateResponse("index.html", {"request": request, "prices": prices, "lowest_price_store": lowest_price_store, "lowest_price": lowest_price})

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
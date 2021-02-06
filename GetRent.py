from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import regex

def GetCityRent(listOfCities):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--log-level=3");

    driver = webdriver.Chrome(options = chrome_options)
    driver.get('https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+States')

    CitiesAndRent = []
    for city in listOfCities:
        try:
            Select(driver.find_element_by_xpath('/html/body/div[2]/nav[2]/form/select')).select_by_value(city)
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/ul/li[2]')))
            rent =driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]').text
            rent = extractRent(rent)
            CitiesAndRent.append([city,rent])
            driver.back()
        except Exception as e:
            print(e)
            driver.get('https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+States')
    driver.quit()
    return CitiesAndRent

def extractRent(message):
    no=regex.search(r'\(.*\p{Sc}\)',message)
    return no.group()
listOfCities =['Amherst, MA','Boston, MA', 'Los Angeles, CA']

print(GetCityRent(listOfCities))



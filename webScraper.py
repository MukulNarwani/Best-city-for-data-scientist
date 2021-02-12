from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import regex
import pandas
from pandas import ExcelWriter

def GetCityRent(RentAndSalary):
    #TODO: Implement webdriverwait and search for the cities rather than dropdown
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--log-level=3");
    driver = webdriver.Chrome(options = chrome_options)

    driver.get('https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+States')
    for key,value in RentAndSalary.items():
        try:
            Select(driver.find_element_by_xpath('/html/body/div[2]/nav[2]/form/select')).select_by_value(key)
            WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/ul/li[2]')))
            rent =driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]').text
            print(rent)
            rent = extractRent(rent)
            value.append(rent)
            driver.back()
        except Exception as e:
            value.append('Error: Could not find rent'+ str(e))
            driver.get('https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+States')
    driver.quit()



def GetJobSalary(RentAndSalary):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--log-level=3");
    driver = webdriver.Chrome(options = chrome_options)

    for key,value in RentAndSalary.items():
        try:
            cityState = key.split(',')
            WebDriverWait(driver,5).until(EC.url_changes)
            driver.get('https://www.indeed.com/career/data-scientist/salaries/'+cityState[0]+'--'+cityState[1])
            salary =driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div[1]/div[3]/div[1]').text
            value.append(salary)
        except Exception as e:
            value.append("Error: Can't find salary on indeed "+str(e))
    driver.quit()


def extractRent(message):
    no=regex.search(r'\b.*\p{Sc}',message)
    return no.group()



listOfCities =['Amherst, MA','Boston, MA', 'Los Angeles, CA','Phoenix, AZ','Atlanta, GA','Palo Alto, CA',\
                'Nashville, TN','Austin, TX','Boulder, CO','Seattle, WA','San Jose, CA', 'Seoul, South Korea',\
                 'Paris, France', 'Milan, Italy', 'Toronto, Canada', 'Singapore, Singapore','Dublin, Ireland','London, United Kingdom' ]

RentAndSalary={i : [] for i in listOfCities}

GetCityRent(RentAndSalary)
GetJobSalary(RentAndSalary)
df = pandas.DataFrame.from_dict(RentAndSalary, orient='index',columns = ['Rent','Salary'])
try:
    with ExcelWriter('data.xls') as writer:
        df.to_excel(writer)
except PermissionError as e:
    print(e)
    pass
#df.to_csv('filename.csv',index =False)







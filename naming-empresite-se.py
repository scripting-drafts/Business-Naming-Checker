from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import re

concept = input('Check Naming:')
reConcept = re.compile('.*' + '\\b' + concept + '\\b' + '.*', re.IGNORECASE)
pages, matches = [], []
lastPage, delay = 1, 10

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("https://empresite.eleconomista.es")

### INPUT TO EMPRESITE
driver.find_element_by_xpath('//*[@id="search"]').send_keys(concept)
driver.find_element_by_xpath('/html/body/div[1]/div/header/div/div[2]/div/input[2]').click()

try:
    pagesRAW = driver.find_elements_by_css_selector('.mr4 [href]')
    for pageRAW in pagesRAW:
        pages.append(pageRAW.get_attribute('href'))
except NoSuchElementException:
    pass

for page in pages:
    try:
        titles = driver.find_elements_by_css_selector('.title03.text-capitalize')
        for title in titles:
            match = re.findall(reConcept, title.text)
            matches.extend(match)
    except NoSuchElementException:
        break
    finally:
        driver.get(page)

while lastPage > 0:
    try:
        titles = driver.find_elements_by_css_selector('.title03.text-capitalize')
        for title in titles:
            match = re.findall(reConcept, title.text)
            matches.extend(match)
    except NoSuchElementException:
        break
    finally:
        lastPage -= 1

sortedMatches = sorted(matches)

if len(sortedMatches) > 0:
    print('Found ' + str(len(sortedMatches)) + ' results')
    print('\n'.join(map(str, sortedMatches)))
else:
    print('Congratz ur beri original')

driver.close()
exit()

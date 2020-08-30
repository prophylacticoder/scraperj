import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import bs4 as bs

cnpjs = []

# Open the csv file and loads the cnpjs
with open('cnpj.csv', 'rt') as f:
    data = csv.reader(f)
    for row in data:
        cnpjs.append(row[0])
    del cnpjs[0]

data = []

driver = webdriver.Firefox(executable_path="geckodriver")

# Loop through all the cnpj's list
for cnpj in cnpjs:

    driver.get("http://appasp.sefaz.go.gov.br/Sintegra/Consulta/default.asp")

    radio_cnpj = driver.find_element_by_id('rTipoDocCNPJ')
    radio_cnpj.click()

    cnpjField = driver.find_element_by_id('tCNPJ')
    cnpjField.send_keys(cnpj)

    window_before = driver.window_handles[0]

    submitBtn = driver.find_element_by_name('btCGC')
    submitBtn.click()

    window_after = driver.window_handles[1]

    # Change to the data tab
    driver.switch_to_window(window_after)
    time.sleep(2)

    #Get the page's source code
    sc_code = driver.page_source

    beautiful_soup = bs.BeautifulSoup(sc_code, 'lxml')

    has_not_found = beautiful_soup.find('div', {'style':
            'font:bold 12px Arial, Helvetica, sans-serif; margin-top:50px;'})

    # If it hasn't found the data then insert default data
    if has_not_found:
        data.append([cnpj, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
                    'NULL', 'NULL', ])
    else:
        #Othterwise scrape the data
        html_elements = beautiful_soup.find_all('span', {'class', 'label_text'})
        data.append([cnpj, html_elements[1].text.strip(),
        html_elements[2].text.strip(), html_elements[3].text.strip(),
        html_elements[16].text.strip(), html_elements[20].text.strip(),
        html_elements[21].text.strip(), html_elements[22].text.strip()])]



    # Change back to the search tab
    driver.switch_to_window(window_before)

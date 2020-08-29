import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

cnpjs = []

# Open the csv file and loads the cnpjs
with open('cnpj.csv', 'rt') as f:
    data = csv.reader(f)
    for row in data:
        cnpjs.append(row[0])
    del cnpjs[0]

dictData = {'cnpj': ''}
driver = webdriver.Firefox(executable_path="geckodriver")

# Loop through all the cnpj's list
for cnpj in cnpjs:

    driver.get("http://appasp.sefaz.go.gov.br/Sintegra/Consulta/default.asp")

    radio_cnpj = driver.find_element_by_id('rTipoDocCNPJ')
    radio_cnpj.click()

    cnpjField = driver.find_element_by_id('tCNPJ')
    cnpjField.send_keys(cnpj)

    submitBtn = driver.find_element_by_name('btCGC')
    submitBtn.click()

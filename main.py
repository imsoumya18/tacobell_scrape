import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from selenium import webdriver
import time

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)

client = gspread.authorize(creds)

ip = input('Enter input file name(without file extension): ')
op = input('Enter output file name(without file extension): ')

iput = client.open(ip).sheet1
oput = client.open(op).sheet1

driver = webdriver.Chrome('chromedriver.exe')

# If 'htps://tacobell.com/locations' is not censored in your location, comment the 2 following lines(line 23 & 24)
driver.get('https://chrome.google.com/webstore/detail/touch-vpn-secure-and-unli/bihmplhobchoageeokmgbdihknkjbknd')
input('Enter:')

oput.update_cell(1, 1, 'Property Street')
oput.update_cell(1, 2, 'Property City')
oput.update_cell(1, 3, 'Property State')
oput.update_cell(1, 4, 'Property Zip')

i = 2
j = 2
x = 2
while oput.cell(x, 1).value is not None or oput.cell(x+1, 1).value is not None:
    x += 1
    if oput.cell(x, 1).value is None and oput.cell(x+1, 1).value is not None:
        i += 1
        j = x + 1
while iput.cell(i, 1).value is not None:
    driver.get('https://tacobell.com/locations')
    driver.find_element_by_id('id_store').send_keys(iput.cell(i, 1).value)
    driver.find_element_by_xpath('//button[contains(text(), "Go")]').click()
    time.sleep(20)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    x = j
    for k in soup.find_all('div', class_='addr-line1')[1:]:
        oput.update_cell(j, 1, str(k.getText()))
        time.sleep(1.7)
        j += 1
    for l in soup.find_all('div', class_='addr-region')[1:]:
        oput.update_cell(x, 2, str(l.getText()).split(",")[0])
        time.sleep(1.7)
        oput.update_cell(x, 3, str(l.getText()).split(",")[1].split(" ")[1])
        time.sleep(1.7)
        oput.update_cell(x, 4, str(l.getText()).split(",")[1].split(" ")[2])
        time.sleep(1.7)
        x += 1
    j += 1
    i += 1

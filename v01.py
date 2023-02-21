import requests
import openpyxl
import xlsxwriter
from bs4 import BeautifulSoup

proxies = {
    'http': 'http://20.111.54.16:80',
    'http': 'http://152.67.73.106:80',
    'http': 'http://23.227.39.154:80',
    'http': 'http://23.227.39.93:80',
    'http': 'http://141.193.213.96:80',
    'http': 'http://103.21.244.195:80',
    'http': 'http://172.64.149.43:80',
    'http': 'http://172.64.159.235:80',
    'http': 'http://172.67.180.20:80',
    'http': 'http://203.28.8.223:80'
}


def write_headers():
    worksheet.write(0, 0, 'Brand')
    worksheet.write(0, 1, 'Article')
    worksheet.write(0, 2, 'Name')
    worksheet.write(0, 3, "Provider")
    worksheet.write(0, 4, "Date_of_issue")
    worksheet.write(0, 5, "Availability")
    worksheet.write(0, 6, "Price")

location = 'Прайс опт полный прайс1.xlsx'

book = openpyxl.load_workbook(location)
sheet = book.active

workbook = xlsxwriter.Workbook('Expenses03.xlsx')
worksheet = workbook.add_worksheet()
write_headers()

counter = 1
for ar in range(11, 1803):
    article = sheet.cell(row=ar, column=2).value
    print("ARTICLE ----->", article)

    worksheet.write(counter, 0, sheet.cell(row=ar, column=1).value)
    worksheet.write(counter, 1, article)
    worksheet.write(counter, 2, sheet.cell(row=ar, column=3).value)

    responce = requests.get(f'https://v01.ru/auto/search/?q={article}', proxies=proxies)

    soup = BeautifulSoup(responce.text, 'lxml')

    # Находим таблицу
    table = soup.find('table')
    # Делаем массив для хранения информации
    # providers = []; dates_of_issue = []; availabilities = []; prices = []; brands = []; names = []
    # Берем первую строчку
    catalog_product_row = table.find('tr', class_='catalog-product-row')
    try:
        provider = catalog_product_row.find('td', class_='supplier').text
    except:
        print("   ------> EXCEPTION! WE HAVE MUCH PRODUCTS WITH THIS ARTICLE. SKIP ---> ")
        continue
    date_of_issue = catalog_product_row.find('td', class_='delivery_time js-refresh-time').text
    availability = catalog_product_row.find('td', class_='instock text-center').text.replace(' ', '')
    price = catalog_product_row.find('td', class_='price number-cell')['title']

    worksheet.write(counter, 3, provider)
    worksheet.write(counter, 4, date_of_issue)
    worksheet.write(counter, 5, availability)
    worksheet.write(counter, 6, price)

    counter += 1

    # Берем остальные строчки с поставщиками
    rows = table.find_all('tr', class_='hproduct no-hover hlast')


    # Проходимся по ним
    for row in rows:
        provider = row.find('td', class_='supplier').text
        date_of_issue = row.find('td', class_='delivery_time js-refresh-time').text
        availability = row.find('td', class_='instock text-center').text.replace(' ', '')
        price = row.find('td', class_='price number-cell')['title']
        worksheet.write(counter, 3, provider)
        worksheet.write(counter, 4, date_of_issue)
        worksheet.write(counter, 5, availability)
        worksheet.write(counter, 6, price)
        counter += 1

workbook.close()
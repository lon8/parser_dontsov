import requests
from bs4 import BeautifulSoup
#import xlsxwriter
import csv

#workbook = xlsxwriter.Workbook('demo.xlsx')
#worksheet = workbook.add_worksheet()
#worksheet.write(0, 0, 'ID')
with open("rating.csv", 'w', encoding='utf-8') as file:
  writer = csv.writer(file)
  writer.writerow(("ID", ))

for i in range(1, 202):
  req = requests.get(
    f'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_ref_key&mode=detail&page={i}&sort=user_rating,desc'
  )

  soup = BeautifulSoup(req.text, 'lxml')
  items = soup.find_all('h3', class_='lister-item-header')

  for item in items:
    link = item.find('a')['href']
    link = link[7:][:-1]
    print(link)
    with open("rating.csv", 'a', encoding='utf-8') as file:
      writer = csv.writer(file)
      writer.writerow((link, ))
  print('\n\n-----> Спарсили страницу:', i, '\n\n')
#workbook.close()

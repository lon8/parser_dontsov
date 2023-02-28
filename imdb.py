import requests

req =requests.get('https://pro.imdb.com/title/tt0119567/details/_ajax')

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(req.text)
# 40001
print(1)
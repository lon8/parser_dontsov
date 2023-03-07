import random
import requests
from bs4 import BeautifulSoup
import threading
import queue

urls = [
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=',
    "https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=alpha,asc&page=",
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=user_rating,desc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=num_votes,desc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=release_date,desc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=runtime,desc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=year,desc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=year,asc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=runtime,asc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=release_date,asc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=num_votes,asc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=user_rating,asc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=alpha,desc&page=',
    'https://www.imdb.com/search/keyword/?keywords=based-on-novel&ref_=kw_nxt&mode=detail&sort=moviemeter,desc&page='
]

proxies = [
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},
    {"https://": "3afx92:ho4m7x@88.218.72.200:9655"},		
]

def make_request(url):
    for i in range(1, 201):
        req = requests.get(url + str(i), proxies=random.choice(proxies))
        idis = []
        soup = BeautifulSoup(req.text, 'lxml')
        id_list = soup.find_all('h3', class_='lister-item-header')
        for idi in id_list:
            l = idi.find('a')['href'].split('/')[2]
            print('\n\t -> PAGE --->', i, '-> ID ---> ', l, '\n')
            idis.append(l)
        with open('text.txt', 'a', encoding="utf-8") as f:
            for item in idis:
                f.write("%s\n" % item)
    

def worker(q):
    while True:
        url = q.get()
        make_request(url)
        q.task_done()

concurrent_requests = 7
q = queue.Queue()
for url in urls:
    q.put(url)

threads = []
for i in range(concurrent_requests):
    thread = threading.Thread(target=worker, args=(q,))
    threads.append(thread)
    thread.start()

q.join()

for thread in threads:
    thread.join()
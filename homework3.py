import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
db.genie.drop()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for music in musics:

    a_tag = music.select_one('td.info > a.title.ellipsis')

    if a_tag is not None:
        name = a_tag.text
        artist = music.select_one('td.info > a.artist.ellipsis').text
        rank = music.select_one('td.number').text[0:2]
        print(rank.strip(), name.strip(), artist.strip())

        doc = {
            'rank': rank,
            'music': name,
            'artist': artist
        }
        db.genie.insert_one(doc)

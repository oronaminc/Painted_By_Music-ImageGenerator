from module.lyrics import get_lyrics
from module.keywords import get_keywords
from module.download_content import get_content_urls
from module.download_style import get_style_urls
from module.GAN import get_image
from module.playlist_keyword import get_keyword
import json
import urllib.request
import os
import glob

'''
Path = os.getcwd()+'/output/'
Lyrics = get_lyrics("annemarie", "2002")
print(Lyrics)
print("=============Find Lyrics Done================")
Keywords = get_keywords(Lyrics, 3)
print(Keywords)
print(Keywords[1])
print("=============Find Keyword Done================")
'''

keyword_content, keyword_style = get_keyword()
print("============Find Keyword Done================\n")

print("============Start to Find Urls================")
Url_content = get_content_urls(keyword_content[1], 3)
print("content: ", Url_content)
Url_style = get_style_urls(keyword_style[1], 3)
print("style: ", Url_style)
print("=============Find Urls Done================\n")

print("=============Start to Create Image================")
#style = "https://i.pinimg.com/originals/82/0f/c3/820fc362b0e1fdf18f755e498bd34f98.jpg"
Url = get_image(Url_content[1], Url_style[0])
#N = len(glob.glob(Path))
#urllib.request.urlretrieve(Url['output_url'], Path+"output"+str(N+1)+".png")
Path = os.getcwd()+'/output/'
urllib.request.urlretrieve(Url['output_url'], Path+"output.png")
print("=============Create Image Done================")

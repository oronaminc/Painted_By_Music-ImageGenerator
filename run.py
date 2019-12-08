from module.lyrics import get_lyrics
from module.keywords import get_keywords
from module.download import get_urls
from module.GAN import get_image
import json
import urllib.request
import os
import glob

Path = os.getcwd()+'/output/'
Lyrics = get_lyrics("annemarie", "2002")
print(Lyrics)
print("=============Find Lyrics Done================")
Keywords = get_keywords(Lyrics, 3)
print(Keywords)
print(Keywords[1])
print("=============Find Keyword Done================")
Urls = get_urls(Keywords[1], 3)
print(Urls)
print("=============Find Urls Done================")
style = "https://i.pinimg.com/originals/82/0f/c3/820fc362b0e1fdf18f755e498bd34f98.jpg"
Url = get_image(Urls[2], style)
N = len(glob.glob(Path))
urllib.request.urlretrieve(Url['output_url'], Path+"output"+str(N+1)+".png")
print("=============Create Image Done================")

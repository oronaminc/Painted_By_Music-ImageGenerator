import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from .forms import PhotoForm
from .models import Photo
import json
import urllib.request
import os
import glob
import random

#lyrics
import re
import urllib.request
from bs4 import BeautifulSoup
import sys

#keyword
from monkeylearn import MonkeyLearn

#download
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from google_images_download import google_images_download 
import sys

#GAN
import requests

#playlist_keyword
from nltk import *

#image process
import cv2


class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/basic_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

# Drag and Drop을 통한 mp3 파일 업로드
class DragAndDropUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

# 기존의 업로드 된 파일을 삭제하고 초기화 시킴
def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))

# 이미지를 선택할 수 있도록 사진의 크기를 조절
def resizeImage(name):
    pth = os.path.dirname(os.path.dirname(__file__))
    path = pth+'/photos/images/'
    path2 = pth+'/static/images/'
    img = cv2.imread(path+name)
    row = img.shape[0]
    ratio = 148/row
    resize_img = cv2.resize(img, dsize=(0,0), fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)
    cv2.imwrite(path2+name, resize_img)
    cv2.waitKey()

# 작곡가와 노래 제목을 바탕으로 가사를 추출해냄 (가사를 크롤링 해서 가져옴)
def get_lyrics(artist,song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"
    
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('<br/>','').replace('</div>','').strip()
        lyrics = lyrics.replace('\n', ' ')
        return lyrics
    except Exception as e:
        return "Exception occurred \n" +str(e)

# 키워드를 바탕으로 이미지의 주소를 가지고 옴.
def get_urls(keyword, limit, isContent):
    orig_stdout = sys.stdout
    f = open('URLS.txt', 'w')
    sys.stdout = f

    response = google_images_download.googleimagesdownload()

    if not isContent: keyword += ' painting'

    arguments = {"keywords"     : keyword,
                "limit"        : limit,
                "print_urls"   : True,
                #"size"         : ">2MP",
                }
    paths = response.download(arguments)

    sys.stdout = orig_stdout
    f.close()

    with open('URLS.txt') as f:
        content = f.readlines()
    f.close()

    urls = []
    for j in range(len(content)):
        if content[j][:9] == 'Completed':
            url = content[j-1][11:-1]

            try:
                res = urlopen(url)
            except HTTPError:
                continue

            urls.append(url)

            if len(urls) == 3 : break
    
    return urls

# GAN으로 합성된 이미지를 가지고 옴.
def get_image(content, style):
    r = requests.post(
        "https://api.deepai.org/api/fast-style-transfer",
        data={
            'content': content,
            'style': style,
        },
        headers={'api-key': 'bcef51fe-566a-472e-a5da-f9b2b4dbd483'}
    )
    return r.json()

# content url 과  style url의 값을 저장하는 txt 파일을 만드는 함수
def make_txt(url_content, url_style):
    f = open("url_content.txt", "w")

    print(url_content)

    i = random.randint(0, 2)
    tmp_url_content = list()
    while i < len(url_content):
        tmp_url_content.append(url_content[i])
        i += 3

    if len(tmp_url_content) > 5:
        random.shuffle(tmp_url_content)
        tmp_url_content = tmp_url_content[:5]

    for i in range(0, len(tmp_url_content)):
        f.writelines(tmp_url_content[i]+"\n")

    f.close()

    f = open("url_style.txt", "w")
    style_str = url_style[random.randint(0, len(url_style)-1)]
    f.writelines(style_str)
    f.close()

    return tmp_url_content, style_str


# 가사를 기반으로 Content 키워드와 Style 키워드를 각각 추출하여 List 로 반환한다.
def get_keyword():
    # mp3 파일 업로드 경로
    pth = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    print(pth)
    path = pth+'/media/musics'
    # 파일명으로 구성된 리스트 생성
    file_list = os.listdir(path)

    # 파일명에서 .mp3 확장자 제거
    for i in range(len(file_list)):
        file_list[i] = file_list[i].replace(".mp3", "")


    playlist_splited = list()
    for i in range(len(file_list)):
        # '-'를 기준으로 가수와 제목을 구분
        playlist_splited.append(file_list[i].split('-'))

    # 앞에서 가져온 가수와 제목을 바탕으로 az api를 이용해 가사 검색 & 명사, 형용사 키워드 추출
    keyword_content = list()
    keyword_style = list()
    for artist, title in playlist_splited:
        print("=============Start to Find Lyrics================")
        print(artist, '-', title)
        # 가사 검색
        #lyric = Music.getLyrics(artist=artist, title=title)
        lyric = get_lyrics(artist, title)
        print("=============Find Lyrics Done================")

        # 가사를 모두 소문자로 변경
        lyric = lyric.lower()
        # lyric 문자열을 토큰화 한 다음 universal 품사 tagset 적용
        lyric_tokens = pos_tag(word_tokenize(lyric), tagset='universal')

        # 명사, 형용사 태그의 토큰들만 모아 각각 리스트를 만듦
        lyric_noun_list = [word for word,
                           pos in lyric_tokens if pos in ['NOUN']]
        lyric_adj_list = [word for word, pos in lyric_tokens if pos in ['ADJ']]

        # 길이 3 미만의 단어는 제외
        lyric_noun_list = [
            word for word in lyric_noun_list if not len(word) < 3]
        lyric_adj_list = [word for word in lyric_adj_list if not len(word) < 3]

        # (키워드, 빈도수) 튜플을 원소로 가지는 리스트를 생성
        fd_noun = FreqDist(lyric_noun_list)
        fd_adj = FreqDist(lyric_adj_list)

        # 가장 높은 빈도수 3개의 리스트를 생성 후 출력
        a = fd_noun.most_common(3)
        b = fd_adj.most_common(3)

        #print(a, b)
        i = 0
        while i < 3:
            keyword_content.append(a[i][0])
            keyword_style.append(b[i][0])
            i += 3

    print("Content Keywords :",keyword_content)
    print("Style Keywords :", keyword_style)
    return keyword_content, keyword_style

# Main 함수 실행
def run(request):
    pth = os.path.dirname(os.path.dirname(__file__))
    Path = pth+'/photos/output/'
    print("============Start to Find Keyword=============")
    keyword_content, keyword_style = get_keyword()
    print("============Find Keyword Done================\n")

    print("============Start to Find Urls================")
    limit = 5

    i = 0
    playlist_url_content = list()
    while i < len(keyword_content):
        Url_content = get_urls(keyword_content[i], limit, 1)
        while not Url_content:
            Url_content = get_urls(keyword_content[i], limit, 1)
        playlist_url_content += Url_content
        i += 1

    print("content: ", playlist_url_content)

    playlist_url_style = get_urls(keyword_style[random.randint(0, len(keyword_style)-1)], limit, 0)
    while not playlist_url_style :
        playlist_url_style = get_urls(keyword_style[random.randint(0, len(keyword_style)-1)], limit, 0)
    print("style: ", playlist_url_style)

    content_five_list, style_str = make_txt(playlist_url_content, playlist_url_style)
    print("=============Find Urls Done================\n")

    print("=============Start to Select Content Image============")

    temp_path = pth+"/photos/images/"
    temp_N = len(glob.glob(temp_path+'*'))
    print(content_five_list)
    for idx, item in enumerate(content_five_list):
        print(item)
        urllib.request.urlretrieve(item, temp_path+str(idx+1)+".png")
    for i in range(1, 6):
        resizeImage(str(i)+'.png')

    
    return redirect(request.POST.get('next'))

# 첫 번째 사진을 클릭했을 때 불러오는 함수
def make1(request):
    f = open("selected_content_number.txt", "w+")
    f.write("1")
    f.close()
    print("=============Select Content Image Done============")

    pth = os.path.dirname(os.path.dirname(__file__))
    Path_output = pth+'/static/output/'

    print("=============Start to Create Image================")
    selected = int(open("selected_content_number.txt", "r").readlines()[0])
    final_content = str(open("url_content.txt", "r").readlines()[
                        selected-1]).replace("\n", "")
    final_style = str(open("url_style.txt", "r").readlines()[0]).replace("\n", "")

    Url = get_image(final_content, final_style)

    N = len(glob.glob(Path_output+'*'))
    urllib.request.urlretrieve(Url['output_url'], Path_output+"output.png")
    print("=============Create Image Done================")
   
    return redirect(request.POST.get('next1'))

# 두 번째 사진을 클릭했을 때 불러오는 함수
def make2(request):
    f = open("selected_content_number.txt", "w+")
    f.write("2")
    f.close()
    print("=============Select Content Image Done============")

    pth = os.path.dirname(os.path.dirname(__file__))
    Path_output = pth+'/static/output/'

    print("=============Start to Create Image================")
    selected = int(open("selected_content_number.txt", "r").readlines()[0])
    final_content = str(open("url_content.txt", "r").readlines()[
                        selected-1]).replace("\n", "")
    final_style = str(open("url_style.txt", "r").readlines()[0]).replace("\n", "")

    Url = get_image(final_content, final_style)

    N = len(glob.glob(Path_output+'*'))
    urllib.request.urlretrieve(Url['output_url'], Path_output+"output.png")
    print("=============Create Image Done================")
    return redirect(request.POST.get('next1'))

# 세 번째 사진을 클릭했을 때 불러오는 함수
def make3(request):
    f = open("selected_content_number.txt", "w+")
    f.write("3")
    f.close()
    print("=============Select Content Image Done============")

    pth = os.path.dirname(os.path.dirname(__file__))
    Path_output = pth+'/static/output/'

    print("=============Start to Create Image================")
    selected = int(open("selected_content_number.txt", "r").readlines()[0])
    final_content = str(open("url_content.txt", "r").readlines()[
                        selected-1]).replace("\n", "")
    final_style = str(open("url_style.txt", "r").readlines()[0]).replace("\n", "")

    Url = get_image(final_content, final_style)

    N = len(glob.glob(Path_output+'*'))
    urllib.request.urlretrieve(Url['output_url'], Path_output+"output.png")
    print("=============Create Image Done================")
    return redirect(request.POST.get('next1'))

# 네 번째 사진을 클릭했을 때 불러오는 함수
def make4(request):
    f = open("selected_content_number.txt", "w+")
    f.write("4")
    f.close()
    print("=============Select Content Image Done============")

    pth = os.path.dirname(os.path.dirname(__file__))
    Path_output = pth+'/static/output/'

    print("=============Start to Create Image================")
    selected = int(open("selected_content_number.txt", "r").readlines()[0])
    final_content = str(open("url_content.txt", "r").readlines()[
                        selected-1]).replace("\n", "")
    final_style = str(open("url_style.txt", "r").readlines()[0]).replace("\n", "")

    Url = get_image(final_content, final_style)

    N = len(glob.glob(Path_output+'*'))
    urllib.request.urlretrieve(Url['output_url'], Path_output+"output.png")
    print("=============Create Image Done================")
    return redirect(request.POST.get('next1'))

# 다섯 번째 사진을 클릭했을 때 불러오는 함수
def make5(request):
    f = open("selected_content_number.txt", "w+")
    f.write("5")
    f.close()
    print("=============Select Content Image Done============")

    pth = os.path.dirname(os.path.dirname(__file__))
    #Path_unresized = pth+'/photos/images/'
    Path_output = pth+'/static/output/'

    print("=============Start to Create Image================")
    selected = int(open("selected_content_number.txt", "r").readlines()[0])
    final_content = str(open("url_content.txt", "r").readlines()[
                        selected-1]).replace("\n", "")
    final_style = str(open("url_style.txt", "r").readlines()[0]).replace("\n", "")

    Url = get_image(final_content, final_style)

    N = len(glob.glob(Path_output+'*'))
    urllib.request.urlretrieve(Url['output_url'], Path_output+"output.png")
    print("=============Create Image Done================")
    return redirect(request.POST.get('next1'))

from nltk import *
from module.lyrics import get_lyrics
import os
<<<<<<< HEAD

def get_keyword():
    # mp3 파일 업로드 경로 (!!! 경로 수정 필요)
    path = '../../media/musics'
=======
#import azapi


def get_keyword():
    # mp3 파일 업로드 경로 (!!! 경로 수정 필요)
    path = './TEST/mp3'
>>>>>>> origin/master
    # 파일명으로 구성된 리스트 생성
    file_list = os.listdir(path)

    # 파일명에서 .mp3 확장자 제거
    for i in range(len(file_list)):
        file_list[i] = file_list[i].replace(".mp3", "")

    '''
    # playlist.txt 파일에서 가수와 제목을 가져옴
    with open('playlist.txt', 'r') as f:
        playlist = f.readlines()
        # 개행 문자 제거
        playlist = list(map(lambda s:s.strip(), playlist))
<<<<<<< HEAD
=======

>>>>>>> origin/master
    playlist_splited = list()
    for i in range(len(playlist)) :
        # '-'를 기준으로 가수와 제목을 구분
        playlist_splited.append(playlist[i].split(' - '))
    '''

    playlist_splited = list()
    for i in range(len(file_list)):
        # '-'를 기준으로 가수와 제목을 구분
<<<<<<< HEAD
        playlist_splited.append(file_list[i].split('-'))
    
=======
        playlist_splited.append(file_list[i].split(' - '))

>>>>>>> origin/master
    # print(playlist_splited)

    # 앞에서 가져온 가수와 제목을 바탕으로 az api를 이용해 가사 검색 & 명사, 형용사 키워드 추출
    # Music = azapi.AZlyrics()
    keyword_content = list()
    keyword_style = list()
    for artist, title in playlist_splited:
        print("=============Start to Find Lyrics================")
        print(artist, '-', title)
        # 가사 검색
        #lyric = Music.getLyrics(artist=artist, title=title)
        lyric = get_lyrics(artist, title)
        print("=============Find Lyrics Done================\n")

        print("============Start to Find Keyword================")
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

        print(a, b)
        i = 0
        while i < 3:
            keyword_content.append(a[i][0])
            keyword_style.append(b[i][0])
            i += 1

    print(keyword_content, keyword_style)
<<<<<<< HEAD
    return keyword_content, keyword_style
=======
    return keyword_content, keyword_style
>>>>>>> origin/master

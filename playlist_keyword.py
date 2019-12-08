from nltk import *
from module.lyrics import get_lyrics
#import azapi

# playlist.txt 파일에서 가수와 제목을 가져옴
with open('playlist.txt', 'r') as f:
    playlist = f.readlines()
    # 개행 문자 제거
    playlist = list(map(lambda s:s.strip(), playlist))

playlist_splited = list()
for i in range(len(playlist)) :
    # '-'를 기준으로 가수와 제목을 구분
    playlist_splited.append(playlist[i].split(' - '))


# 앞에서 가져온 가수와 제목을 바탕으로 az api를 이용해 가사 검색 & 명사, 형용사 키워드 추출
# Music = azapi.AZlyrics()
for artist, title in playlist_splited :
    print(artist, '-', title)
    # 가사 검색
    #lyric = Music.getLyrics(artist=artist, title=title)
    lyric = get_lyrics(artist, title)
    # 가사를 모두 소문자로 변경
    lyric = lyric.lower()
    # lyric 문자열을 토큰화 한 다음 universal 품사 tagset 적용
    lyric_tokens = pos_tag(word_tokenize(lyric), tagset='universal')

    # 명사, 형용사 태그의 토큰들만 모아 각각 리스트를 만듦
    lyric_noun_list = [word for word, pos in lyric_tokens if pos in ['NOUN']]
    lyric_adj_list = [word for word, pos in lyric_tokens if pos in ['ADJ']]

    # 길이 3 미만의 단어는 제외
    lyric_noun_list = [word for word in lyric_noun_list if not len(word) < 3]
    lyric_adj_list = [word for word in lyric_adj_list if not len(word) < 3]

    # (키워드, 빈도수) 튜플을 원소로 가지는 리스트를 생성
    fd_noun = FreqDist(lyric_noun_list)
    fd_adj = FreqDist(lyric_adj_list)

    # 가장 높은 빈도수 3개의 리스트를 생성 후 출력
    print(fd_noun.most_common(3))
    print(fd_adj.most_common(3))

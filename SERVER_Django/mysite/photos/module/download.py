from google_images_download import google_images_download 
import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

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

    # url 리스트에 삽입, 단 url 검사하여 http 에러 있는 것은 집어넣지 않음
    urls = []
    for j in range(len(content)):
        if content[j][:9] == 'Completed':
            url = content[j-1][11:-1]

            try:
                res = urlopen(url)
            except HTTPError:
                continue

            urls.append(url)

    urls = urls[:3] 
    
    return urls
    #for item in urls:
    #    print(item)

if __name__ == "__main__":
    get_urls()
#URLS("childhood", 3)
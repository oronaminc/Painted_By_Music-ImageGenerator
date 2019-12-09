from google_images_download import google_images_download
import sys


def get_content_urls(keyword, limit):
    orig_stdout = sys.stdout
    f = open('URLS.txt', 'w')
    sys.stdout = f

    response = google_images_download.googleimagesdownload()

    arguments = {"keywords": keyword,
                 "limit": limit,
                 "print_urls": True,
                 # "size"         : ">2MP",
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
            urls.append(content[j-1][11:-1])

    return urls
    # for item in urls:
    #    print(item)


if __name__ == "__main__":
    get_urls()
#URLS("childhood", 3)

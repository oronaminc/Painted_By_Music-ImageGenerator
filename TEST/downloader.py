from google_images_download import google_images_download
def imageCrawling(keyword, directory):
	response = google_images_download.googleimagesdownload()
    
	arguments = {
		"keywords": keyword,
		"limit": 10,
		"print_urls": True,
		"no_directory": True,
		#"output_directory": directory
		}


	paths = response.download(arguments)
	print(paths)
imageCrawling("sick", "C:/Users/SungHyeon/Desktop/google")
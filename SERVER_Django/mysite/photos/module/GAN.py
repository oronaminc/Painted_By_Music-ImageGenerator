import requests

def get_image(content, style):
    r = requests.post(
        "https://api.deepai.org/api/fast-style-transfer",
        data={
            'content': content,
            'style': style,
        },
        headers={'api-key': 'bcef51fe-566a-472e-a5da-f9b2b4dbd483'}
    )
    #print(r.json())
    return r.json()


if __name__ == "__main__":
    get_image()
#content = "https://www.yourtango.com/sites/default/files/styles/header_slider/public/image_blog/bible-marriage-love-scripture-1-corinthians-13.jpg?itok=BXe6JFHT"
#style = "https://i.pinimg.com/originals/82/0f/c3/820fc362b0e1fdf18f755e498bd34f98.jpg"
#get_image(content, style)
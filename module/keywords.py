from monkeylearn import MonkeyLearn

#with open('1.txt', 'r') as file:
#    txt = file.read().replace('\n', ' ')

def get_keywords(txt, num):
    ml = MonkeyLearn('5d0bc1abdddce358f1b7f076ca86b7bcd1bb78a1')
    data = [txt]
    model_id = 'ex_YCya9nrn'
    result = ml.extractors.extract(model_id, data)

    dic = result.body[0]
    n = 0
    keywords = []
    for item in dic['extractions']:
        keywords.append(item['parsed_value'])
        n += 1
        if n == num: break

    return keywords


if __name__ == "__main__":
   get_keywords()
#txt = "I will always remember The day you kissed my lips Light as  On the day we fell in love On the day we fell in love On the day we fell in love On the day we fell in love, love, love"
#Keyword = get_keywords(txt, 3)
#print(Keyword)

import requests


class Translatets():

    def __init__(self):
        self.kor= ''
        self.en = ''
        self.ru = ''

    def  add_kor(self, kor):
        self.kor = kor

    def  add_en(self, en):
        self.en = en

    def  add_ru(self, ru):
        self.ru = ru


def main():
    trans = Translatets()

    #url = input()

    r = requests.get('https://seoji.nl.go.kr/landingPage?isbn=8988131150')
    #r = requests.get(url)
    r = str(r.text)

    title = r.find('<div class="pageTit">')
    trans.add_kor(r[title+32:title+69])

    print(trans.kor)


if __name__ == "__main__":
    main()

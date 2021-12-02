
import requests
import translators as ts

def main():

    url = input()

    r = requests.get(url)
    r = str(r.text)

    title = r.find('<div class="pageTit">')
    h2 = r.find('</h2>',title,title+100)
    kor = (r[title+32:h2])

    print(kor)
    print(ts.google(kor, to_language='en'))
    print(ts.google(kor, to_language='ru'))


if __name__ == "__main__":
    main()
